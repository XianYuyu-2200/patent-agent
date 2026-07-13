import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from codex_patent.cli import app


ROOT = Path(__file__).parents[1]
RUNNER = CliRunner()


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
