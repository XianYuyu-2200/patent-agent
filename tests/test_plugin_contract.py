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
    r"([A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9][A-Za-z0-9_-]*)+)"
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
