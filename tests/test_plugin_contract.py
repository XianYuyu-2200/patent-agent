import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from codex_patent.cli import app


ROOT = Path(__file__).parents[1]
RUNNER = CliRunner()


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
    assert metadata["description"].startswith("Use when")
    assert "## Inputs" in body
    assert "## Outputs" in body
    assert "## Stop Conditions" in body
    assert "case.json" in body
    assert "exactly one production skill at a time" in body
    approvals = ("technical-solution", "claim-set", "final-delivery")
    assert all(f"`{approval}`" in body for approval in approvals)
    stale_terms = ("specification", "quality-review", "DOCX", "stale")
    assert all(term in body for term in stale_terms)
    assert all(status in body for status in ("inferred", "missing", "conflicted"))
    expected_artifacts = (
        "intake-vN.json",
        "technical-facts-vN.json",
        "prior-art-vN.json",
        "patentability-vN.md",
        "protection-strategy-vN.md",
        "claims-vN.md",
        "specification-vN.md",
        "quality-review-vN.json",
        "application-vN.docx",
    )
    assert all(f"`{artifact}`" in body for artifact in expected_artifacts)
    assert "all declared outputs from exactly one selected production skill" in body

    assert metadata_path.exists()
    interface = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))["interface"]
    assert interface["display_name"] == "中国专利案件编排"
    assert interface["short_description"]
    assert interface["default_prompt"] == (
        "使用 $cn-patent-orchestrator 处理当前案件并生成本阶段规定的结构化产物。"
    )
