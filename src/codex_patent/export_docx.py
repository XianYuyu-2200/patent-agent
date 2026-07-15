from pathlib import Path

from docx import Document

from codex_patent.models import ArtifactRef
from codex_patent.validation import ValidationReport


SECTION_ORDER = [
    "技术领域",
    "背景技术",
    "发明内容",
    "附图说明",
    "具体实施方式",
    "摘要",
]
TEMPLATE_PATH = (
    Path(__file__).resolve().parents[2]
    / "templates"
    / "cn-patent-application.docx"
)


def _validate_content(title: str, claims: list[str], sections: dict[str, str]) -> None:
    if not title.strip():
        raise ValueError("application title must not be blank")
    if not claims or any(not claim.strip() for claim in claims):
        raise ValueError("at least one claim is required and claims must not be blank")
    for heading in SECTION_ORDER:
        if heading not in sections:
            raise ValueError(f"missing required section: {heading}")
        if not sections[heading].strip():
            raise ValueError(f"required section must not be blank: {heading}")


def export_application(
    title: str,
    claims: list[str],
    sections: dict[str, str],
    output_path: Path,
    *,
    final_approval: bool,
    validation_report: ValidationReport,
    artifacts: list[ArtifactRef],
    template_path: Path | None = None,
) -> Path:
    if not final_approval:
        raise ValueError("current final-delivery approval is required")
    if not validation_report.eligible_for_final_delivery:
        raise ValueError("open high-severity validation issues block export")
    for artifact in artifacts:
        artifact_type = artifact.artifact_type.casefold()
        if artifact.stale and artifact_type in {
            "specification",
            "quality-review",
            "docx",
        }:
            raise ValueError(f"stale {artifact_type} artifact blocks export")

    _validate_content(title, claims, sections)
    selected_template = template_path if template_path is not None else TEMPLATE_PATH
    document = Document(selected_template)
    document.add_paragraph(title.strip(), style="Patent Title")
    document.add_paragraph("权利要求书", style="Patent Heading 1")
    for claim in claims:
        document.add_paragraph(claim.strip(), style="Patent Claim")
    for heading in SECTION_ORDER:
        heading_paragraph = document.add_paragraph(heading, style="Patent Heading 1")
        if heading in {"技术领域", "摘要"}:
            heading_paragraph.paragraph_format.page_break_before = True
        for block in sections[heading].strip().split("\n\n"):
            document.add_paragraph(block.strip(), style="Patent Body")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
    return output_path
