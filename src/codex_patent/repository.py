import hashlib
import json
import shutil
from pathlib import Path

from codex_patent.models import PatentCase


class CaseRepository:
    def __init__(self, root: Path):
        self.root = root

    def case_dir(self, case_id: str) -> Path:
        return self.root / case_id

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
        digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
        destination = (
            self.case_dir(case_id)
            / "source-materials"
            / f"{digest}-{source.name}"
        )
        shutil.copy2(source, destination)
        destination.chmod(0o444)
        return destination
