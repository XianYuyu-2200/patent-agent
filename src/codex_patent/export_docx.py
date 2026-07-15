import json
import re
from importlib import resources
from pathlib import Path

from docx import Document
from pydantic import ValidationError

from codex_patent.models import ArtifactRef, PatentCase
from codex_patent.repository import CaseRepository
from codex_patent.validation import ValidationReport


SECTION_ORDER = [
    "技术领域",
    "背景技术",
    "发明内容",
    "附图说明",
    "具体实施方式",
    "摘要",
]
SPECIFICATION_SECTION_ORDER = SECTION_ORDER[:-1]
REQUIRED_ARTIFACT_EXTENSIONS = {
    "claims": ".md",
    "specification": ".md",
    "abstract": ".md",
    "quality-review": ".json",
}
_PACKAGE_TEMPLATE = resources.files("codex_patent").joinpath(
    "templates", "cn-patent-application.docx"
)
_CHECKOUT_TEMPLATE = (
    Path(__file__).resolve().parents[2]
    / "templates"
    / "cn-patent-application.docx"
)
TEMPLATE_PATH = (
    Path(str(_PACKAGE_TEMPLATE))
    if _PACKAGE_TEMPLATE.is_file()
    else _CHECKOUT_TEMPLATE
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


def _load_case(case_dir: Path) -> PatentCase:
    case_dir = Path(case_dir)
    if not case_dir.is_dir():
        raise ValueError(f"case workspace does not exist: {case_dir}")
    try:
        case = CaseRepository(case_dir.parent).load(case_dir.name)
    except (
        FileNotFoundError,
        OSError,
        json.JSONDecodeError,
        ValidationError,
    ) as exc:
        raise ValueError(f"invalid case workspace: {case_dir}") from exc
    if case.case_id != case_dir.name:
        raise ValueError("persisted case ID does not match the case directory")
    return case


def _current_required_artifacts(case: PatentCase) -> dict[str, ArtifactRef]:
    selected: dict[str, ArtifactRef] = {}
    for artifact_type in REQUIRED_ARTIFACT_EXTENSIONS:
        candidates = [
            artifact
            for artifact in case.artifacts
            if artifact.artifact_type.casefold() == artifact_type
        ]
        if not candidates:
            raise ValueError(f"missing required artifact: {artifact_type}")
        current = [artifact for artifact in candidates if not artifact.stale]
        if not current:
            raise ValueError(f"stale {artifact_type} artifact blocks export")
        if len(current) > 1:
            raise ValueError(f"multiple current {artifact_type} artifacts block export")
        selected[artifact_type] = current[0]

    versions = {artifact.version for artifact in selected.values()}
    if len(versions) != 1:
        raise ValueError("required artifacts must share one version")
    return selected


def _read_artifact(
    case_dir: Path,
    artifact_type: str,
    artifact: ArtifactRef,
) -> str:
    relative_path = Path(artifact.path)
    expected_name = (
        f"{artifact_type}-v{artifact.version}"
        f"{REQUIRED_ARTIFACT_EXTENSIONS[artifact_type]}"
    )
    if relative_path.name != expected_name:
        raise ValueError(
            f"{artifact_type} artifact path must name {expected_name}"
        )
    if relative_path.is_absolute():
        raise ValueError(
            f"{artifact_type} artifact must resolve inside the case workspace"
        )

    resolved_case_dir = case_dir.resolve()
    artifact_path = (case_dir / relative_path).resolve()
    if not artifact_path.is_relative_to(resolved_case_dir):
        raise ValueError(
            f"{artifact_type} artifact must resolve inside the case workspace"
        )
    if not artifact_path.is_file():
        raise ValueError(f"missing {artifact_type} artifact file: {artifact.path}")
    try:
        content = artifact_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"unreadable {artifact_type} artifact: {artifact.path}"
        ) from exc
    if not content.strip():
        raise ValueError(f"empty {artifact_type} artifact blocks export")
    return content


def _parse_claims(content: str) -> list[str]:
    claims = [
        block.strip()
        for block in re.split(r"\n\s*\n", content)
        if block.strip()
    ]
    if not claims:
        raise ValueError("at least one claim is required")
    return claims


def _parse_specification(content: str) -> dict[str, str]:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    positions: dict[str, int] = {}
    for index, line in enumerate(lines):
        heading = line.strip()
        if heading not in SPECIFICATION_SECTION_ORDER:
            continue
        if heading in positions:
            raise ValueError(f"duplicate required section: {heading}")
        positions[heading] = index

    for heading in SPECIFICATION_SECTION_ORDER:
        if heading not in positions:
            raise ValueError(f"missing required section: {heading}")
    observed_positions = [
        positions[heading] for heading in SPECIFICATION_SECTION_ORDER
    ]
    if observed_positions != sorted(observed_positions):
        raise ValueError("specification sections are not in the required order")

    sections: dict[str, str] = {}
    for index, heading in enumerate(SPECIFICATION_SECTION_ORDER):
        start = positions[heading] + 1
        end = (
            positions[SPECIFICATION_SECTION_ORDER[index + 1]]
            if index + 1 < len(SPECIFICATION_SECTION_ORDER)
            else len(lines)
        )
        sections[heading] = "\n".join(lines[start:end]).strip()
    return sections


def _quality_review_report(content: str, version: int) -> ValidationReport:
    try:
        value = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "quality-review artifact must contain a valid JSON object"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError("quality-review artifact must contain a valid JSON object")
    if "issues" in value:
        try:
            return ValidationReport.model_validate(value)
        except ValidationError as exc:
            raise ValueError(
                "quality-review artifact must contain valid review issues"
            ) from exc

    expected_version = f"v{version}"
    covered_versions = value.get("covered_versions")
    ready_skill_review = (
        value.get("review_status") == "completed"
        and value.get("current") is True
        and isinstance(covered_versions, dict)
        and all(
            covered_versions.get(artifact_type) == expected_version
            for artifact_type in ("claims", "specification", "abstract")
        )
        and value.get("delivery_recommendation") == "ready-for-human-review"
        and value.get("open_critical") == 0
        and value.get("open_high") == 0
        and value.get("delivery_blocking_issues") == []
        and value.get("delivery_critical_not_assessable") == []
    )
    if not ready_skill_review:
        raise ValueError("quality-review artifact is not eligible for export")
    return ValidationReport()


def _open_template(template_path: Path | None) -> Document:
    if template_path is not None:
        return Document(template_path)
    if _PACKAGE_TEMPLATE.is_file():
        with resources.as_file(_PACKAGE_TEMPLATE) as resolved_template:
            return Document(resolved_template)
    return Document(_CHECKOUT_TEMPLATE)


def export_application(
    case_dir: Path,
    output_path: Path,
    *,
    final_approval: bool,
    template_path: Path | None = None,
) -> Path:
    if type(final_approval) is not bool:
        raise ValueError("explicit final approval must be an actual boolean")
    if final_approval is not True:
        raise ValueError("explicit final approval is required")

    case_dir = Path(case_dir)
    case = _load_case(case_dir)
    if "final-delivery" not in case.approvals:
        raise ValueError("persisted final-delivery approval is required")
    validation_report = ValidationReport(issues=case.issues)
    if not validation_report.eligible_for_final_delivery:
        raise ValueError("open high-severity validation issues block export")
    if any(
        artifact.artifact_type.casefold() == "docx" and artifact.stale
        for artifact in case.artifacts
    ):
        raise ValueError("stale docx artifact blocks export")

    artifacts = _current_required_artifacts(case)
    contents = {
        artifact_type: _read_artifact(case_dir, artifact_type, artifact)
        for artifact_type, artifact in artifacts.items()
    }
    review_report = _quality_review_report(
        contents["quality-review"], artifacts["quality-review"].version
    )
    if not review_report.eligible_for_final_delivery:
        raise ValueError("open high-severity validation issues block export")
    claims = _parse_claims(contents["claims"])
    sections = _parse_specification(contents["specification"])
    sections["摘要"] = contents["abstract"].strip()
    _validate_content(case.title, claims, sections)

    document = _open_template(template_path)
    document.add_paragraph(case.title.strip(), style="Patent Title")
    document.add_paragraph("权利要求书", style="Patent Heading 1")
    for claim in claims:
        document.add_paragraph(claim, style="Patent Claim")
    for heading in SECTION_ORDER:
        heading_paragraph = document.add_paragraph(heading, style="Patent Heading 1")
        if heading in {"技术领域", "摘要"}:
            heading_paragraph.paragraph_format.page_break_before = True
        for block in re.split(r"\n\s*\n", sections[heading]):
            if block.strip():
                document.add_paragraph(block.strip(), style="Patent Body")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
    return output_path
