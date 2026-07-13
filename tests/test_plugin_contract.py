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
    r"([A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z][A-Za-z0-9_-]*)+)"
    r"(?![\w.-])"
)


def _artifact_tokens(section: str) -> set[str]:
    return set(re.findall(ARTIFACT_PATTERN, section))


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
        "motivation from common knowledge. Anchor each step separately to verified evidence."
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
        "4. Write the same five numbered inventive-step records into both artifacts."
    )
    assert "Each record must contain `source_anchor` and `status`" in output_shape_step
    assert "set `source_anchor` to `null`" in output_shape_step
    assert "set `status` to `evidence-insufficient`" in output_shape_step


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
    ("section_name", "unexpected_artifact", "placement"),
    (
        ("Inputs", "case_v4.json", "prefix"),
        ("Inputs", "search-log-v4.json", "suffix"),
        ("Outputs", "evidence-gap_v4.json", "prefix"),
        ("Outputs", "claim-strategy-v4.md", "suffix"),
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
