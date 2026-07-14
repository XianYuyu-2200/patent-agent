import json
import re
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from codex_patent.cli import app


ROOT = Path(__file__).parents[1]
RUNNER = CliRunner()


ARTIFACT_PATTERN = (
    r"(?<![\w.-])"
    r"([\w-]+(?:\.[A-Za-z0-9][A-Za-z0-9_-]*)+)"
    r"(?![\w.-])"
)


def _artifact_tokens(section: str) -> set[str]:
    tokens = set(re.findall(ARTIFACT_PATTERN, section))
    return {
        token
        for token in tokens
        if re.search(r"[A-Za-z_\-\u4e00-\u9fff]", token.split(".", 1)[0])
    }


def test_artifact_tokens_accept_numeric_extensions_but_reject_numeric_workflow_labels():
    assert _artifact_tokens("Store `archive.7z`, `evidence.2026`, and `证据.2026`.") == {
        "archive.7z",
        "evidence.2026",
        "证据.2026",
    }
    assert _artifact_tokens("3.1. First step. 3.2. Second step.") == set()


ORCHESTRATOR_ROUTES = {
    "cn-patent-case-intake": {
        "intake-vN.json",
        "material-index-vN.json",
        "questions-vN.md",
    },
    "patent-invention-mining": {
        "technical-facts-vN.json",
        "feature-tree-vN.json",
        "interview-vN.md",
    },
    "patent-prior-art-search": {
        "search-plan-vN.md",
        "prior-art-vN.json",
        "search-log-vN.json",
    },
    "patentability-analysis": {
        "feature-matrix-vN.json",
        "patentability-vN.md",
    },
    "cn-claim-strategy": {"protection-strategy-vN.md"},
    "cn-claim-drafting": {"claims-vN.md", "claim-feature-map-vN.json"},
    "cn-specification-drafting": {
        "specification-vN.md",
        "abstract-vN.md",
        "drawing-plan-vN.json",
    },
    "cn-patent-quality-review": {
        "quality-review-vN.json",
        "support-matrix-vN.json",
    },
    "patent-document-export": {
        "application-vN.docx",
        "delivery-checklist-vN.md",
    },
}


def _orchestrator_route_outputs(body: str) -> dict[str, set[str]]:
    routes = {}
    for line in body.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        _, _, skill_cell, outputs_cell, _ = line.split("|")
        skill = skill_cell.strip().strip("`")
        outputs = {
            output.strip().strip("`") for output in outputs_cell.split(",")
        }
        routes[skill] = outputs
    return routes


def test_plugin_manifest_and_skill_roots_exist():
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "codex-patent"
    assert manifest["version"] == "0.1.0"
    assert manifest["skills"] == "./skills/"
    assert manifest["author"]["name"] == "XianYuyu-2200"
    assert manifest["interface"]["displayName"] == "中国专利撰写 Agent"
    assert manifest["interface"]["category"] == "Productivity"


def test_cli_version_subcommand():
    result = RUNNER.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout == "0.1.0\n"


def test_cn_patent_orchestrator_has_required_contract():
    skill_dir = ROOT / "skills" / "cn-patent-orchestrator"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"

    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "cn-patent-orchestrator"
    assert metadata["description"] == (
        "Use when starting, resuming, routing, approving, invalidating, or inspecting "
        "a Chinese patent case for intake, invention mining, prior-art search, "
        "patentability analysis, claim strategy, claim drafting, specification "
        "drafting, quality review, or document export."
    )
    assert "## Inputs" in body
    assert "## Outputs" in body
    assert "## Stop Conditions" in body
    assert "case.json" in body
    assert "exactly one production skill at a time" in body
    gate_contracts = (
        "Require `technical-solution` before entering `SEARCH`.",
        "Require `claim-set` before entering `DRAFTING`.",
        "Require `final-delivery` before external export.",
    )
    assert all(contract in body for contract in gate_contracts)
    assert (
        "Never use `inferred`, `missing`, or `conflicted` facts as final drafting "
        "inputs."
    ) in body
    assert (
        "When claims change materially, mark every `specification`, "
        "`quality-review`, and `DOCX` artifact stale in `case.json`."
    ) in body
    assert _orchestrator_route_outputs(body) == ORCHESTRATOR_ROUTES
    assert "all declared outputs from exactly one selected production skill" in body

    assert metadata_path.exists()
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "中国专利案件编排"
    assert interface["short_description"]
    assert interface["default_prompt"] == (
        "使用 $cn-patent-orchestrator 处理当前案件并生成本阶段规定的结构化产物。"
    )


def test_cn_patent_case_intake_has_exact_intake_contract():
    skill_dir = ROOT / "skills" / "cn-patent-case-intake"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"

    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "cn-patent-case-intake"
    assert metadata["description"].startswith("Use when ")
    for trigger in (
        "new Chinese patent case",
        "mixed customer materials",
        "transcriptions",
        "images",
        "code",
        "completeness",
        "conflicts",
        "public-disclosure risk",
    ):
        assert trigger in metadata["description"]

    for heading in (
        "## Inputs",
        "## Workflow",
        "## Outputs",
        "## Stop Conditions",
        "## Quality Checks",
    ):
        assert heading in body

    workflow = body.split("## Workflow", 1)[1].split("## Outputs", 1)[0]
    workflow_steps = [
        line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()
    ]
    assert workflow_steps[0].startswith("1. Validate any existing fact statuses")
    assert (
        "If a new case has no recorded facts, explicitly record the fact set as empty"
        in workflow_steps[0]
    )
    assert workflow.index("Validate any existing fact statuses") < workflow.index(
        "Treat every original as read-only"
    )

    required_contracts = (
        "Treat every original as read-only",
        "Record a source anchor for every extracted fact",
        "Never merge conflicting statements",
        "Mark uncertain inventor identity, applicant identity, and public-disclosure dates as `missing` or `conflicted`",
        "Do not infer details from a blurred or ambiguous image",
        "Do not execute unknown code",
        "Do not invoke invention mining or drafting",
        "Stop after saving the three intake artifacts",
    )
    assert all(contract in body for contract in required_contracts)

    output_lines = {
        line.strip()[3:-1]
        for line in body.splitlines()
        if line.strip().startswith("- `") and line.strip().endswith("`")
    }
    assert output_lines == {
        "intake-vN.json",
        "material-index-vN.json",
        "questions-vN.md",
    }
    assert "technical-facts-vN.json" not in body
    assert "feature-tree-vN.json" not in body
    assert "claims-vN.md" not in body
    assert "specification-vN.md" not in body

    assert metadata_path.exists()
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "专利案件受理"
    assert interface["short_description"]
    assert interface["default_prompt"] == "请处理当前案件并生成本阶段规定的结构化产物。"


def test_patent_invention_mining_has_exact_contract():
    skill_dir = ROOT / "skills" / "patent-invention-mining"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"

    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "patent-invention-mining"
    assert metadata["description"].startswith("Use when ")
    for trigger in (
        "invention mining",
        "intake",
        "technical facts",
        "technical problems",
        "technical means",
        "technical effects",
        "implementation variants",
        "inventor interview",
    ):
        assert trigger in metadata["description"]

    for heading in (
        "## Inputs",
        "## Workflow",
        "## Outputs",
        "## Stop Conditions",
        "## Quality Checks",
    ):
        assert heading in body

    inputs = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
    input_lines = [
        line.strip() for line in inputs.splitlines() if line.strip().startswith("- ")
    ]
    assert len(input_lines) == 2
    assert _artifact_tokens(inputs) == {"intake-vN.json"}
    assert "source anchors" in input_lines[1]

    workflow = body.split("## Workflow", 1)[1].split("## Outputs", 1)[0]
    workflow_steps = [
        line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()
    ]
    assert workflow_steps[0].startswith("1. Validate fact statuses")
    assert all(
        status in workflow_steps[0]
        for status in (
            "`confirmed`",
            "`source-backed`",
            "`inferred`",
            "`missing`",
            "`conflicted`",
        )
    )
    assert "reject unknown values" in workflow_steps[0]

    required_contracts = (
        "Do not invent technical facts",
        "Do not merge conflicting technical effects",
        "Never promote `inferred`, `missing`, or `conflicted` content into a final technical fact",
        "Keep each technical fact linked to its source anchors",
        "Convert missing connections, parameters, and algorithm steps into interview questions",
        "Do not fill gaps with common practice",
        "Do not invoke prior-art search, claim strategy, claim drafting, or specification drafting",
        "Stop after saving the three declared invention-mining artifacts",
    )
    assert all(contract in body for contract in required_contracts)

    outputs = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
    output_lines = [
        line.strip() for line in outputs.splitlines() if line.strip().startswith("- ")
    ]
    assert output_lines == [
        "- `technical-facts-vN.json`",
        "- `feature-tree-vN.json`",
        "- `interview-vN.md`",
    ]
    assert [line[3:-1] for line in output_lines] == [
        "technical-facts-vN.json",
        "feature-tree-vN.json",
        "interview-vN.md",
    ]
    assert _artifact_tokens(outputs) == {
        "technical-facts-vN.json",
        "feature-tree-vN.json",
        "interview-vN.md",
    }
    for forbidden_output in (
        "search-plan-vN.md",
        "prior-art-vN.json",
        "claims-vN.md",
        "specification-vN.md",
    ):
        assert forbidden_output not in body

    assert metadata_path.exists()
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "发明挖掘"
    assert interface["short_description"]
    assert interface["default_prompt"] == "请处理当前案件并生成本阶段规定的结构化产物。"


@pytest.mark.parametrize(
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Inputs", "case_v1.json", "prefix"),
        ("Inputs", "evidence-v1.pdf", "suffix"),
        ("Outputs", "appendix_v1.json", "prefix"),
        ("Outputs", "appendix-v1.txt", "suffix"),
    ),
)
def test_invention_mining_artifact_token_detection_rejects_mutations(
    section_name: str,
    unexpected_artifact: str,
    placement: str,
):
    body = (
        ROOT / "skills" / "patent-invention-mining" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    if section_name == "Inputs":
        section = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
        allowed = {"intake-vN.json"}
    else:
        section = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
        allowed = {
            "technical-facts-vN.json",
            "feature-tree-vN.json",
            "interview-vN.md",
        }

    mutation = f"An additional artifact is `{unexpected_artifact}`."
    mutated_section = (
        f"{mutation}\n{section}" if placement == "prefix" else f"{section}\n{mutation}"
    )

    tokens = _artifact_tokens(mutated_section)
    assert unexpected_artifact in tokens
    assert tokens != allowed


def test_patent_prior_art_search_has_exact_contract():
    skill_dir = ROOT / "skills" / "patent-prior-art-search"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"

    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "patent-prior-art-search"
    assert metadata["description"].startswith("Use when ")
    for trigger in (
        "prior-art search",
        "novelty search",
        "classification search",
        "comparison evidence",
        "feature tree",
    ):
        assert trigger in metadata["description"]

    for heading in (
        "## Inputs",
        "## Workflow",
        "## Outputs",
        "## Stop Conditions",
        "## Quality Checks",
    ):
        assert heading in body

    inputs = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
    input_lines = [
        line.strip() for line in inputs.splitlines() if line.strip().startswith("- ")
    ]
    assert input_lines == ["- `feature-tree-vN.json`"]
    assert _artifact_tokens(inputs) == {"feature-tree-vN.json"}

    workflow = body.split("## Workflow", 1)[1].split("## Outputs", 1)[0]
    workflow_steps = [
        line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()
    ]
    assert workflow_steps[0].startswith(
        "1. Validate fact statuses separately from feature statuses"
    )
    assert all(
        status in workflow_steps[0]
        for status in (
            "`confirmed`",
            "`source-backed`",
            "`inferred`",
            "`missing`",
            "`conflicted`",
        )
    )
    assert "Only `confirmed` and `source-backed` facts may enter formal searches" in workflow_steps[0]
    assert "Only `confirmed` and `source-backed` features may enter formal searches" in workflow_steps[0]
    assert "Block and stop on `inferred`, `missing`, `conflicted`, or unknown fact statuses" in workflow_steps[0]
    assert "Block and stop on `inferred`, `missing`, `conflicted`, or unknown feature statuses" in workflow_steps[0]
    assert "Treat `core` and `core-combination` as roles, not statuses" in workflow_steps[0]
    assert "reject unknown values" in workflow_steps[0]
    assert "`unresolved_questions` and `source_anchors`" in workflow_steps[-1]
    assert "inside each of the three declared artifacts" in workflow_steps[-1]

    required_contracts = (
        "core features and feature combinations",
        "Create one independent search branch for each `core` feature",
        "one combination branch for each `core-combination` role",
        "A combination branch never replaces the independent core-feature branches",
        "keywords, synonyms, IPC/CPC classifications, applicants, inventors, and combined queries",
        "Record every database, complete query, search date, and screening process",
        "Every executable query record requires `database`, `collection`, `fields`, `verified_dialect`, and `query`",
        "Do not label a generic concept expression as executable database syntax",
        "blocked-missing-verified-dialect",
        "Keep generic concept expressions in the search plan only",
        "blocked-missing-verified-classification",
        "blocked-missing-identity",
        "`query` = `null`",
        "publication number, publication date, priority date",
        "claim, paragraph, page, or figure anchor",
        "verbatim quotation",
        "Do not fabricate a publication number, document, date, result, quotation, or anchor",
        "Do not treat a result without a source anchor as formal evidence",
        "Do not give a final novelty or inventive-step conclusion",
        "Do not invoke claim strategy, claim drafting, or specification drafting",
        "Stop after saving the three declared prior-art-search artifacts",
    )
    assert all(contract in body for contract in required_contracts)

    outputs = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
    output_lines = [
        line.strip() for line in outputs.splitlines() if line.strip().startswith("- ")
    ]
    assert output_lines == [
        "- `search-plan-vN.md`",
        "- `prior-art-vN.json`",
        "- `search-log-vN.json`",
    ]
    assert _artifact_tokens(outputs) == {
        "search-plan-vN.md",
        "prior-art-vN.json",
        "search-log-vN.json",
    }
    for forbidden_output in (
        "feature-matrix-vN.json",
        "patentability-vN.md",
        "protection-strategy-vN.md",
        "claims-vN.md",
        "specification-vN.md",
    ):
        assert forbidden_output not in body

    assert metadata_path.exists()
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "现有技术检索"
    assert interface["short_description"]
    assert interface["default_prompt"] == "请处理当前案件并生成本阶段规定的结构化产物。"


@pytest.mark.parametrize(
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Inputs", "case_v3.json", "prefix"),
        ("Inputs", "search-brief-v3.md", "suffix"),
        ("Outputs", "citations_v3.json", "prefix"),
        ("Outputs", "novelty-opinion-v3.md", "suffix"),
    ),
)
def test_prior_art_search_artifact_token_detection_rejects_mutations(
    section_name: str,
    unexpected_artifact: str,
    placement: str,
):
    body = (
        ROOT / "skills" / "patent-prior-art-search" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    if section_name == "Inputs":
        section = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
        allowed = {"feature-tree-vN.json"}
    else:
        section = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
        allowed = {
            "search-plan-vN.md",
            "prior-art-vN.json",
            "search-log-vN.json",
        }

    mutation = f"An additional artifact is `{unexpected_artifact}`."
    mutated_section = (
        f"{mutation}\n{section}" if placement == "prefix" else f"{section}\n{mutation}"
    )

    tokens = _artifact_tokens(mutated_section)
    assert unexpected_artifact in tokens
    assert tokens != allowed


def _assert_patentability_body_contract(body: str) -> None:
    assert _artifact_tokens(body) == {
        "feature-tree-vN.json",
        "prior-art-vN.json",
        "feature-matrix-vN.json",
        "patentability-vN.md",
    }

    workflow = body.split("## Workflow", 1)[1].split("## Outputs", 1)[0]
    workflow_steps = [
        line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()
    ]
    novelty_step = workflow_steps[1]
    assert (
        "A novelty rejection requires one prior-art document that directly and "
        "unambiguously discloses every necessary feature."
    ) in novelty_step
    assert "Never combine multiple documents to deny novelty." in novelty_step

    inventive_intro = workflow_steps[2]
    assert inventive_intro == (
        "3. Assess inventive step only after completing the following fixed sequence. "
        "Inventive step may consider multiple documents. Do not supply combination "
        "motivation from common knowledge. Anchor each step separately to verified evidence. "
        "If no document passes Step 1, set all five records to `value: null`, "
        "`source_anchor: null`, and `status: evidence-insufficient`; do not provisionally "
        "select closest prior art or distinguishing features."
    )
    inventive_chain = workflow_steps[3:8]
    assert [step.split(". ", 1)[0] for step in inventive_chain] == [
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
    ]
    required_steps = (
        "Record the closest prior art.",
        "Record the distinguishing features.",
        "Record the actual technical problem.",
        "Record the combination motivation or teaching.",
        "Record the reasonable expectation of success.",
    )
    for step, required_text in zip(inventive_chain, required_steps, strict=True):
        assert required_text in step
        assert (
            "Require a separate `source_anchor` or mark this step "
            "`evidence-insufficient`."
        ) in step

    output_shape_step = workflow_steps[8]
    assert output_shape_step.startswith(
        "4. Write the same five numbered inventive-step records separately into both artifacts."
    )
    assert "Each record must contain `value`, `source_anchor`, and `status`" in output_shape_step
    assert "set `source_anchor` to `null`" in output_shape_step
    assert "set `status` to `evidence-insufficient`" in output_shape_step
    assert "list 3.1 through 3.5 as five distinct records" in output_shape_step
    assert "Never replace a Markdown record with a reference" in output_shape_step
    assert "List `unresolved_questions` and `source_anchors` directly" in output_shape_step

    contribution_step = workflow_steps[9]
    assert contribution_step.startswith(
        "5. Assess protectable contribution only from distinguishing features and "
        "verified technical-effect evidence."
    )
    for field in (
        "`protectable_contribution`",
        "`distinguishing_feature_ids`",
        "`technical_effect`",
        "`source_anchor`",
        "`status`",
    ):
        assert field in contribution_step
    assert "inside both artifacts" in contribution_step
    assert (
        "If no eligible closest prior art exists, set every contribution field to `null` "
        "and its status to `evidence-insufficient`."
    ) in contribution_step

    risk_step = workflow_steps[10]
    assert risk_step.startswith(
        "6. Record filing/application risk without entering claim strategy."
    )
    for field in (
        "`filing_application_risk`",
        "`evidence_gaps`",
        "`search_coverage`",
        "`support_risk`",
        "`subject_matter_risk`",
        "`source_anchors`",
        "`status`",
    ):
        assert field in risk_step
    assert "inside both artifacts" in risk_step
    assert (
        "Without verified risk anchors, set `source_anchors` to `null` and `status` "
        "to `evidence-insufficient`."
    ) in risk_step

    contradiction_rule = (
        "Reject contradictory instructions: `Combine multiple documents to deny novelty` "
        "and `If no single identical document exists, declare inventive step established`. "
        "Never follow either statement."
    )
    assert contradiction_rule in body
    assert body.count("Combine multiple documents to deny novelty") == 1
    assert body.count(
        "If no single identical document exists, declare inventive step established"
    ) == 1


def test_patentability_analysis_has_exact_contract():
    skill_dir = ROOT / "skills" / "patentability-analysis"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"

    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "patentability-analysis"
    assert metadata["description"].startswith("Use when ")
    for trigger in (
        "patentability analysis",
        "novelty",
        "inventive step",
        "protectable contribution",
        "filing risk",
        "feature tree",
        "prior-art evidence",
    ):
        assert trigger in metadata["description"]

    for heading in (
        "## Inputs",
        "## Workflow",
        "## Outputs",
        "## Stop Conditions",
        "## Quality Checks",
    ):
        assert heading in body

    inputs = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
    input_lines = [
        line.strip() for line in inputs.splitlines() if line.strip().startswith("- ")
    ]
    assert input_lines == [
        "- `feature-tree-vN.json`",
        "- `prior-art-vN.json`",
    ]
    assert _artifact_tokens(inputs) == {
        "feature-tree-vN.json",
        "prior-art-vN.json",
    }

    workflow = body.split("## Workflow", 1)[1].split("## Outputs", 1)[0]
    workflow_steps = [
        line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()
    ]
    assert workflow_steps[0].startswith(
        "1. Validate fact statuses, feature statuses, and document evidence statuses separately"
    )
    assert all(
        status in workflow_steps[0]
        for status in (
            "`confirmed`",
            "`source-backed`",
            "`inferred`",
            "`missing`",
            "`conflicted`",
            "`verified`",
        )
    )
    assert "Only `confirmed` and `source-backed` facts may enter formal analysis" in workflow_steps[0]
    assert "Only `confirmed` and `source-backed` features may enter formal analysis" in workflow_steps[0]
    assert "Only `verified` documents with a publication date" in workflow_steps[0]
    assert "verbatim quotation" in workflow_steps[0]
    assert "claim, paragraph, page, or figure anchor" in workflow_steps[0]
    assert (
        "Treat an absent fact, feature, or document evidence status as `missing`"
        in workflow_steps[0]
    )
    assert (
        "Treat an absent publication date, verbatim quotation, or source anchor as `missing`"
        in workflow_steps[0]
    )
    assert (
        "Never infer `confirmed`, `source-backed`, or `verified` from a summary"
        in workflow_steps[0]
    )
    assert (
        "A filename, document ID, statement that a document discloses a feature, or "
        "placeholder reference to an input anchor does not satisfy the evidence gate"
        in workflow_steps[0]
    )
    assert (
        "The current context must contain the actual status, publication date, verbatim "
        "quotation, and concrete anchor values"
        in workflow_steps[0]
    )
    assert (
        "Otherwise set document eligibility to `false` and every related `source_anchor` "
        "to `null`"
        in workflow_steps[0]
    )
    assert "reject unknown values" in workflow_steps[0]
    assert "`unresolved_questions` and `source_anchors`" in workflow_steps[-1]
    assert "inside each of the two declared artifacts" in workflow_steps[-1]

    required_contracts = (
        "A novelty rejection requires one prior-art document",
        "directly and unambiguously discloses every necessary feature",
        "Never combine multiple documents to deny novelty",
        "Inventive step may consider multiple documents",
        "closest prior art",
        "distinguishing features",
        "actual technical problem",
        "combination motivation or teaching",
        "reasonable expectation of success",
        "Anchor each step separately to verified evidence",
        "Do not supply combination motivation from common knowledge",
        "search is incomplete",
        "publication date or source anchor is missing",
        "core fact is conflicted",
        "`evidence-insufficient`",
        "do not give an affirmative legal conclusion",
        "Do not invoke claim strategy or claim drafting",
        "Stop after saving the two declared patentability-analysis artifacts",
        "protectable contribution",
        "filing/application risk",
    )
    assert all(contract in body for contract in required_contracts)
    _assert_patentability_body_contract(body)

    outputs = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
    output_lines = [
        line.strip() for line in outputs.splitlines() if line.strip().startswith("- ")
    ]
    assert output_lines == [
        "- `feature-matrix-vN.json`",
        "- `patentability-vN.md`",
    ]
    assert _artifact_tokens(outputs) == {
        "feature-matrix-vN.json",
        "patentability-vN.md",
    }
    for forbidden_output in (
        "evidence-gap-vN.json",
        "novelty-opinion-vN.md",
        "protection-strategy-vN.md",
        "claims-vN.md",
        "specification-vN.md",
    ):
        assert forbidden_output not in body

    assert metadata_path.exists()
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "可专利性分析"
    assert interface["short_description"]
    assert interface["default_prompt"] == "请处理当前案件并生成本阶段规定的结构化产物。"


@pytest.mark.parametrize(
    ("original", "replacement"),
    (
        (
            "## Quality Checks",
            "## Quality Checks\n\n- Save `risk-register-vN.md` for management review.",
        ),
        (
            "3.2. Record the distinguishing features.",
            "3.3. Record the distinguishing features.",
        ),
        (
            "Require a separate `source_anchor` or mark this step `evidence-insufficient`.",
            "Anchor only the overall inventive-step result.",
        ),
        (
            "3.4. Record the combination motivation or teaching.",
            "3.4. Do not require combination motivation or teaching.",
        ),
    ),
)
def test_patentability_body_contract_rejects_scope_and_reasoning_mutations(
    original: str,
    replacement: str,
):
    body = (
        ROOT / "skills" / "patentability-analysis" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    mutated_body = body.replace(original, replacement, 1)

    assert mutated_body != body
    with pytest.raises(AssertionError):
        _assert_patentability_body_contract(mutated_body)


@pytest.mark.parametrize(
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Workflow", "risk-register-vN.md", "prefix"),
        ("Stop Conditions", "analysis-notes-vN.json", "suffix"),
        ("Quality Checks", "management-summary-vN.md", "suffix"),
        ("Workflow", "archive.7z", "prefix"),
        ("Quality Checks", "evidence.2026", "suffix"),
    ),
)
def test_patentability_global_artifact_scope_rejects_elsewhere_mutations(
    section_name: str,
    unexpected_artifact: str,
    placement: str,
):
    body = (
        ROOT / "skills" / "patentability-analysis" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    heading = f"## {section_name}"
    mutation = f"An additional artifact is `{unexpected_artifact}`."
    replacement = (
        f"{heading}\n{mutation}"
        if placement == "prefix"
        else f"{heading}\n\n{mutation}"
    )
    mutated_body = body.replace(heading, replacement, 1)

    assert mutated_body != body
    with pytest.raises(AssertionError):
        _assert_patentability_body_contract(mutated_body)


@pytest.mark.parametrize(
    "contradictory_instruction",
    (
        "Combine multiple documents to deny novelty",
        "If no single identical document exists, declare inventive step established",
    ),
)
def test_patentability_semantic_contract_rejects_appended_contradictions(
    contradictory_instruction: str,
):
    body = (
        ROOT / "skills" / "patentability-analysis" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    mutated_body = f"{body}\n{contradictory_instruction}.\n"

    with pytest.raises(AssertionError):
        _assert_patentability_body_contract(mutated_body)


@pytest.mark.parametrize(
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Inputs", "case_v4.json", "prefix"),
        ("Inputs", "search-log-v4.json", "suffix"),
        ("Outputs", "evidence-gap_v4.json", "prefix"),
        ("Outputs", "claim-strategy-v4.md", "suffix"),
        ("Inputs", "archive.7z", "prefix"),
        ("Outputs", "evidence.2026", "suffix"),
    ),
)
def test_patentability_artifact_token_detection_rejects_mutations(
    section_name: str,
    unexpected_artifact: str,
    placement: str,
):
    body = (
        ROOT / "skills" / "patentability-analysis" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    if section_name == "Inputs":
        section = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
        allowed = {"feature-tree-vN.json", "prior-art-vN.json"}
    else:
        section = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
        allowed = {"feature-matrix-vN.json", "patentability-vN.md"}

    mutation = f"An additional artifact is `{unexpected_artifact}`."
    mutated_section = (
        f"{mutation}\n{section}" if placement == "prefix" else f"{section}\n{mutation}"
    )

    tokens = _artifact_tokens(mutated_section)
    assert unexpected_artifact in tokens
    assert tokens != allowed


def _assert_claim_strategy_body_contract(body: str) -> None:
    assert _artifact_tokens(body) == {
        "feature-tree-vN.json",
        "patentability-vN.md",
        "protection-strategy-vN.md",
    }
    workflow = body.split("## Workflow", 1)[1].split("## Outputs", 1)[0]
    steps = [line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()]
    gate = steps[0]
    assert gate.startswith("1. Apply a value-based status and evidence gate")
    for phrase in (
        "Only features whose actual status value is `confirmed` or `source-backed`",
        "concrete `source_anchors`",
        "protectable contribution or risk values",
        "A filename or a statement that the input should contain evidence is not evidence",
        "Treat `inferred`, `missing`, `conflicted`, and `evidence-insufficient` features as provisional",
        "must not enter the formal core, secondary, or fallback strategy",
    ):
        assert phrase in gate
    for phrase in (
        "protection subjects",
        "Chinese invention patent and utility model",
        "proposed independent-claim subjects and counts",
        "core, secondary, and fallback feature tiers",
        "commercial value",
        "design-around paths",
        "unity, support, and subject-matter risks",
        "Necessary features must not be removed merely to broaden scope",
        "Do not invent substitute structures or implementation variants",
        "Do not write claim sentences or claim text",
        "Do not invoke claim drafting or specification drafting",
        "A utility model may cover a product's shape, structure, or combination",
        "software or AI methods and software itself must not be repackaged as utility models",
        "`formal_strategy_status: evidence-insufficient` or `blocked`",
        "`unresolved_questions` and `source_anchors`",
    ):
        assert phrase in body
    invariant_section = body.split("## Safety Invariants", 1)[1].split("## Outputs", 1)[0]
    invariant_rows = {}
    for line in invariant_section.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        _, invariant, decision, _ = line.split("|")
        invariant_rows[invariant.strip().strip("`")] = decision.strip().strip("`")
    assert invariant_rows == {
        "essential_feature_removal": "forbidden",
        "unanchored_alternative_inclusion": "forbidden",
        "blocked_mode_claim_text": "forbidden",
        "utility_model_method_software_object": "forbidden",
    }
    contradictory_phrases = (
        "允许为商业宽度删除必要特征",
        "必要特征可为扩大商业范围而省略",
        "Allow removing essential features for commercial breadth",
        "Essential features may be omitted to broaden commercial scope",
        "无锚点也补普通替代结构",
        "未锚定的常见替代方案也可以加入",
        "Include ordinary alternatives even without source anchors",
        "Unanchored common alternatives are allowed",
        "blocked 时仍提供独立权利要求草稿",
        "受阻模式仍可起草独立权利要求",
        "Provide an independent-claim draft even in blocked mode",
        "Draft independent claims while blocked",
        "软件控制方法可作为实用新型客体",
        "实用新型可以保护软件控制方法",
        "Software control methods may be utility-model subject matter",
        "Utility models may claim software control methods",
    )
    assert not any(phrase in body for phrase in contradictory_phrases)


def test_cn_claim_strategy_has_exact_contract():
    skill_dir = ROOT / "skills" / "cn-claim-strategy"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"
    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)
    assert metadata["name"] == "cn-claim-strategy"
    assert metadata["description"].startswith("Use when ")
    for trigger in ("Chinese patent protection strategy", "claim strategy", "invention patent", "utility model", "design-around", "feature tree", "patentability"):
        assert trigger in metadata["description"]
    for heading in ("## Inputs", "## Workflow", "## Outputs", "## Stop Conditions", "## Quality Checks"):
        assert heading in body
    inputs = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
    assert [line.strip() for line in inputs.splitlines() if line.strip().startswith("- ")] == [
        "- `feature-tree-vN.json`",
        "- `patentability-vN.md`",
    ]
    outputs = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
    assert [line.strip() for line in outputs.splitlines() if line.strip().startswith("- ")] == ["- `protection-strategy-vN.md`"]
    _assert_claim_strategy_body_contract(body)
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "权利要求策略"
    assert interface["short_description"]
    assert interface["default_prompt"] == "请处理当前案件并生成本阶段规定的结构化产物。"


@pytest.mark.parametrize(
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Inputs", "case-v6.json", "prefix"),
        ("Outputs", "claims-v6.md", "suffix"),
        ("Workflow", "strategy-notes-v6.txt", "prefix"),
        ("Stop Conditions", "archive.7z", "suffix"),
        ("Quality Checks", "evidence.2026", "suffix"),
        ("Quality Checks", "璇佹嵁.2026", "prefix"),
    ),
)
def test_claim_strategy_global_artifact_scope_rejects_mutations(section_name, unexpected_artifact, placement):
    body = (ROOT / "skills" / "cn-claim-strategy" / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[2]
    heading = f"## {section_name}"
    following_headings = {
        "Inputs": "## Workflow",
        "Workflow": "## Outputs",
        "Outputs": "## Stop Conditions",
        "Stop Conditions": "## Quality Checks",
        "Quality Checks": None,
    }
    section_start = body.index(heading) + len(heading)
    next_heading = following_headings[section_name]
    section_end = body.index(next_heading, section_start) if next_heading else len(body)
    mutation = f"An additional artifact is `{unexpected_artifact}`."
    insertion = f"\n{mutation}\n"
    offset = section_start if placement == "prefix" else section_end
    mutated = f"{body[:offset]}{insertion}{body[offset:]}"
    assert unexpected_artifact in _artifact_tokens(mutated)
    with pytest.raises(AssertionError):
        _assert_claim_strategy_body_contract(mutated)


@pytest.mark.parametrize(
    "contradictory_instruction",
    (
        "允许为商业宽度删除必要特征",
        "必要特征可为扩大商业范围而省略",
        "Allow removing essential features for commercial breadth",
        "Essential features may be omitted to broaden commercial scope",
        "无锚点也补普通替代结构",
        "未锚定的常见替代方案也可以加入",
        "Include ordinary alternatives even without source anchors",
        "Unanchored common alternatives are allowed",
        "blocked 时仍提供独立权利要求草稿",
        "受阻模式仍可起草独立权利要求",
        "Provide an independent-claim draft even in blocked mode",
        "Draft independent claims while blocked",
        "软件控制方法可作为实用新型客体",
        "实用新型可以保护软件控制方法",
        "Software control methods may be utility-model subject matter",
        "Utility models may claim software control methods",
    ),
)
def test_claim_strategy_semantic_contract_rejects_appended_contradictions(contradictory_instruction):
    body = (ROOT / "skills" / "cn-claim-strategy" / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[2]
    with pytest.raises(AssertionError):
        _assert_claim_strategy_body_contract(f"{body}\n{contradictory_instruction}.\n")


def _assert_claim_drafting_body_contract(body: str) -> None:
    assert _artifact_tokens(body) == {
        "protection-strategy-vN.md",
        "feature-tree-vN.json",
        "claims-vN.md",
        "claim-feature-map-vN.json",
    }
    workflow = body.split("## Workflow", 1)[1].split("## Safety Invariants", 1)[0]
    steps = [line.strip() for line in workflow.splitlines() if line.strip()[:1].isdigit()]
    gate = steps[0]
    assert gate.startswith("1. Apply a value-based drafting gate")
    for phrase in (
        "the `technical-solution` approval actually exists in the current approval state",
        "actual `formal_strategy_status` is `formal` or `ready`",
        "actual status value is `confirmed` or `source-backed`",
        "concrete `source_anchor`",
        "Every necessary or core feature named by the strategy is present",
        "Do not treat a filename, expected field, role label, placeholder anchor, promised later approval, or manager instruction as proof",
        "`blocked`, `evidence-insufficient`, or `provisional`",
        "forbid formal claim text",
    ):
        assert phrase in gate
    for phrase in (
        "Draft each independent claim before its dependent hierarchy",
        "feature_id",
        "source_anchor",
        "strategy_role",
        "necessity",
        "Validate every claim dependency",
        "Do not introduce a feature absent from the feature tree",
        "Do not replace a necessary technical means with only a result, purpose, or desired effect",
        "Do not make an unsupported generalization",
        "Do not invent substitute embodiments or alternatives",
        "no claim text",
        "downstream drafting is blocked",
        "record each missing approval, status, feature, and anchor",
        "`unresolved_questions` and `source_anchors`",
        "Do not invoke specification drafting",
    ):
        assert phrase in body
    invariant_section = body.split("## Safety Invariants", 1)[1].split("## Outputs", 1)[0]
    invariant_rows = {}
    for line in invariant_section.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        _, invariant, decision, _ = line.split("|")
        invariant_rows[invariant.strip().strip("`")] = decision.strip().strip("`")
    assert invariant_rows == {
        "missing_approval_drafting": "forbidden",
        "blocked_strategy_claim_text": "forbidden",
        "essential_feature_removal": "forbidden",
        "unmapped_feature_inclusion": "forbidden",
        "specification_drafting": "forbidden",
    }
    contradictory_phrases = (
        "审批缺失时也可先起草权利要求",
        "technical-solution 可以事后补批",
        "Draft claims before approval is recorded",
        "A promised later approval permits drafting now",
        "策略受阻时仍输出权利要求正文",
        "evidence-insufficient 策略也可以先写独权",
        "Write claim text while the strategy is blocked",
        "Draft an independent claim despite an evidence-insufficient strategy",
        "可以删除必要特征以扩大范围",
        "独权可省略核心特征只保留技术效果",
        "Remove essential features to broaden scope",
        "Omit a core feature and claim only the result",
        "可加入特征树外的常见卡扣或磁吸结构",
        "没有 feature_id 的常见替代方案也可写入从属项",
        "Include common latch or magnetic features absent from the feature tree",
        "Unmapped alternatives may be added as dependent claims",
        "权利要求完成后继续起草说明书",
        "本阶段可顺便生成说明书正文",
        "Continue into specification drafting after the claims",
        "Generate specification text in this stage",
    )
    assert not any(phrase in body for phrase in contradictory_phrases)


def test_cn_claim_drafting_has_exact_contract():
    skill_dir = ROOT / "skills" / "cn-claim-drafting"
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"
    assert skill_path.exists()
    text = skill_path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)
    assert metadata["name"] == "cn-claim-drafting"
    assert metadata["description"].startswith("Use when ")
    for trigger in (
        "Chinese patent claims",
        "claim revision",
        "protection strategy",
        "feature tree",
        "feature-source mapping",
    ):
        assert trigger in metadata["description"]
    for heading in (
        "## Inputs",
        "## Workflow",
        "## Safety Invariants",
        "## Outputs",
        "## Stop Conditions",
        "## Quality Checks",
    ):
        assert heading in body
    inputs = body.split("## Inputs", 1)[1].split("## Workflow", 1)[0]
    assert [line.strip() for line in inputs.splitlines() if line.strip().startswith("- ")] == [
        "- `protection-strategy-vN.md`",
        "- `feature-tree-vN.json`",
    ]
    outputs = body.split("## Outputs", 1)[1].split("## Stop Conditions", 1)[0]
    assert [line.strip() for line in outputs.splitlines() if line.strip().startswith("- ")] == [
        "- `claims-vN.md`",
        "- `claim-feature-map-vN.json`",
    ]
    _assert_claim_drafting_body_contract(body)
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "权利要求撰写"
    assert interface["short_description"]
    assert interface["default_prompt"] == "请处理当前案件并生成本阶段规定的结构化产物。"


@pytest.mark.parametrize(
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Inputs", "technical-solution-v1.json", "prefix"),
        ("Workflow", "claim-notes-v1.txt", "suffix"),
        ("Outputs", "specification-v1.md", "prefix"),
        ("Stop Conditions", "approval-request-v1.md", "suffix"),
        ("Quality Checks", "archive.7z", "prefix"),
        ("Quality Checks", "evidence.2026", "suffix"),
        ("Quality Checks", "证据.2026", "prefix"),
    ),
)
def test_claim_drafting_global_artifact_scope_rejects_mutations(
    section_name, unexpected_artifact, placement
):
    body = (
        ROOT / "skills" / "cn-claim-drafting" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    heading = f"## {section_name}"
    following_headings = {
        "Inputs": "## Workflow",
        "Workflow": "## Safety Invariants",
        "Outputs": "## Stop Conditions",
        "Stop Conditions": "## Quality Checks",
        "Quality Checks": None,
    }
    section_start = body.index(heading) + len(heading)
    next_heading = following_headings[section_name]
    section_end = body.index(next_heading, section_start) if next_heading else len(body)
    mutation = f"An additional artifact is `{unexpected_artifact}`."
    insertion = f"\n{mutation}\n"
    offset = section_start if placement == "prefix" else section_end
    mutated = f"{body[:offset]}{insertion}{body[offset:]}"
    assert unexpected_artifact in _artifact_tokens(mutated)
    with pytest.raises(AssertionError):
        _assert_claim_drafting_body_contract(mutated)


@pytest.mark.parametrize(
    "contradictory_instruction",
    (
        "审批缺失时也可先起草权利要求",
        "technical-solution 可以事后补批",
        "Draft claims before approval is recorded",
        "A promised later approval permits drafting now",
        "策略受阻时仍输出权利要求正文",
        "evidence-insufficient 策略也可以先写独权",
        "Write claim text while the strategy is blocked",
        "Draft an independent claim despite an evidence-insufficient strategy",
        "可以删除必要特征以扩大范围",
        "独权可省略核心特征只保留技术效果",
        "Remove essential features to broaden scope",
        "Omit a core feature and claim only the result",
        "可加入特征树外的常见卡扣或磁吸结构",
        "没有 feature_id 的常见替代方案也可写入从属项",
        "Include common latch or magnetic features absent from the feature tree",
        "Unmapped alternatives may be added as dependent claims",
        "权利要求完成后继续起草说明书",
        "本阶段可顺便生成说明书正文",
        "Continue into specification drafting after the claims",
        "Generate specification text in this stage",
    ),
)
def test_claim_drafting_semantic_contract_rejects_appended_contradictions(
    contradictory_instruction,
):
    body = (
        ROOT / "skills" / "cn-claim-drafting" / "SKILL.md"
    ).read_text(encoding="utf-8").split("---", 2)[2]
    with pytest.raises(AssertionError):
        _assert_claim_drafting_body_contract(f"{body}\n{contradictory_instruction}.\n")
