import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).parents[1]


def test_built_wheel_contains_default_docx_template(tmp_path: Path):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            ".",
            "--no-deps",
            "--wheel-dir",
            str(tmp_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    wheel = next(tmp_path.glob("codex_patent-*.whl"))
    with ZipFile(wheel) as archive:
        members = archive.namelist()

    assert "codex_patent/templates/cn-patent-application.docx" in members
