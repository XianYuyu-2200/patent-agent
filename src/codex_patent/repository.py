import hashlib
import json
from pathlib import Path

from codex_patent.models import PatentCase


class CaseRepository:
    def __init__(self, root: Path):
        self.root = root

    def case_dir(self, case_id: str) -> Path:
        case_path = Path(case_id)
        if not case_id or case_path.is_absolute() or len(case_path.parts) != 1:
            raise ValueError("case_id must be a single path segment")

        case_dir = self.root / case_id
        resolved_root = self.root.resolve()
        resolved_case_dir = case_dir.resolve()
        if (
            resolved_case_dir == resolved_root
            or not resolved_case_dir.is_relative_to(resolved_root)
        ):
            raise ValueError("case_id must resolve inside the workspace")
        return case_dir

    def create(self, case: PatentCase) -> Path:
        case_dir = self.case_dir(case.case_id)
        for name in (
            "source-materials",
            "technical-facts",
            "prior-art",
            "drafts",
            "review-log",
        ):
            (case_dir / name).mkdir(parents=True, exist_ok=True)
        self.save(case)
        return case_dir

    def save(self, case: PatentCase) -> None:
        path = self.case_dir(case.case_id) / "case.json"
        path.write_text(case.model_dump_json(indent=2), encoding="utf-8")

    def load(self, case_id: str) -> PatentCase:
        data = json.loads(
            (self.case_dir(case_id) / "case.json").read_text(encoding="utf-8")
        )
        return PatentCase.model_validate(data)

    def add_source(self, case_id: str, source: Path) -> Path:
        content = source.read_bytes()
        digest = hashlib.sha256(content).hexdigest()[:12]
        destination = (
            self.case_dir(case_id)
            / "source-materials"
            / f"{digest}-{source.name}"
        )
        destination.write_bytes(content)
        destination.chmod(0o444)
        return destination
