import json
from pathlib import Path

import tomllib

import codex_patent


ROOT = Path(__file__).parents[1]


def test_release_contains_required_components():
    assert (ROOT / ".codex-plugin/plugin.json").exists()
    assert (ROOT / "skills/cn-patent-orchestrator/SKILL.md").exists()
    assert len(list((ROOT / "skills").glob("*/SKILL.md"))) == 12
    assert (ROOT / "templates/cn-patent-application.docx").exists()


def test_release_version_is_consistent():
    manifest = json.loads(
        (ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert manifest["version"] == project["project"]["version"]
    assert manifest["version"] == codex_patent.__version__


def test_acceptance_record_preserves_release_and_human_gates():
    acceptance = (ROOT / "docs/phase-1-acceptance.md").read_text(encoding="utf-8")

    for required_text in (
        "0.1.0",
        "technical-solution",
        "claim-set",
        "final-delivery",
        "NO-GO",
        "Phase 2",
    ):
        assert required_text in acceptance
