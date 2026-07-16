import hashlib
import os
import stat
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codex_patent.cli import app
from codex_patent.models import PatentCase
from codex_patent.repository import CaseRepository


RUNNER = CliRunner()
ARTIFACT_DIRECTORIES = {
    "source-materials",
    "technical-facts",
    "prior-art",
    "drafts",
    "review-log",
}


def test_repository_rejects_parent_traversal_without_writing_outside_workspace(
    tmp_path: Path,
):
    workspace = tmp_path / "workspace"
    repo = CaseRepository(workspace)

    with pytest.raises(ValueError, match="case_id"):
        repo.create(PatentCase(case_id="../escaped", title="Traversal"))

    assert not (tmp_path / "escaped").exists()


def test_repository_rejects_absolute_case_id_without_writing_outside_workspace(
    tmp_path: Path,
):
    workspace = tmp_path / "workspace"
    absolute_case_dir = tmp_path / "absolute-case"
    repo = CaseRepository(workspace)

    with pytest.raises(ValueError, match="case_id"):
        repo.create(PatentCase(case_id=str(absolute_case_dir), title="Absolute"))

    assert not absolute_case_dir.exists()


def test_repository_round_trip_and_source_copy(tmp_path: Path):
    repo = CaseRepository(tmp_path)
    case = PatentCase(case_id="CN-2026-0001", title="折叠支架")
    repo.create(case)
    source = tmp_path / "客户说明.txt"
    source.write_text("支架通过转轴折叠", encoding="utf-8")
    stored = repo.add_source(case.case_id, source)

    loaded = repo.load(case.case_id)
    assert loaded == case
    assert stored.read_text(encoding="utf-8") == "支架通过转轴折叠"
    assert stored.parent.name == "source-materials"


def test_create_builds_case_layout_and_source_is_content_addressed_read_only(
    tmp_path: Path,
):
    repo = CaseRepository(tmp_path)
    case = PatentCase(case_id="CN-2026-0002", title="锁止结构")
    case_dir = repo.create(case)
    source = tmp_path / "说明.txt"
    source.write_text("锁止销限制支架转动", encoding="utf-8")

    stored = repo.add_source(case.case_id, source)

    assert {path.name for path in case_dir.iterdir() if path.is_dir()} == ARTIFACT_DIRECTORIES
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    assert stored.name == f"{digest}-{source.name}"
    write_bits = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    assert stored.stat().st_mode & write_bits == 0


def test_source_digest_matches_saved_bytes_when_source_changes_after_read(
    tmp_path: Path,
):
    class ChangingSourcePath(type(Path())):
        def read_bytes(self) -> bytes:
            content = super().read_bytes()
            super().write_bytes(b"changed-after-read")
            return content

    repo = CaseRepository(tmp_path)
    case = PatentCase(case_id="CN-2026-0003", title="Race")
    repo.create(case)
    source = tmp_path / "race.txt"
    source.write_bytes(b"original")

    stored = repo.add_source(case.case_id, ChangingSourcePath(source))

    stored_bytes = stored.read_bytes()
    stored_digest = stored.name.partition("-")[0]
    assert stored_digest == hashlib.sha256(stored_bytes).hexdigest()[:12]


def test_stored_source_rejects_overwrite(tmp_path: Path):
    repo = CaseRepository(tmp_path)
    case = PatentCase(case_id="CN-2026-0004", title="Immutable")
    repo.create(case)
    source = tmp_path / "immutable.txt"
    source.write_bytes(b"original")
    stored = repo.add_source(case.case_id, source)

    if os.name == "posix" and os.geteuid() == 0:
        pytest.skip("POSIX root can bypass read-only mode bits")

    with pytest.raises(PermissionError):
        stored.write_bytes(b"tampered")
    assert stored.read_bytes() == b"original"


def test_case_create_cli_creates_workspace_layout(tmp_path: Path):
    workspace = tmp_path / "cases"

    result = RUNNER.invoke(
        app,
        [
            "case-create",
            "CN-TEST-001",
            "测试案件",
            "--workspace",
            str(workspace),
        ],
    )

    case_dir = workspace / "CN-TEST-001"
    assert result.exit_code == 0
    assert result.stdout == f"{case_dir}\n"
    assert (case_dir / "case.json").is_file()
    assert {path.name for path in case_dir.iterdir() if path.is_dir()} == ARTIFACT_DIRECTORIES
