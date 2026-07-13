import json
from pathlib import Path

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
