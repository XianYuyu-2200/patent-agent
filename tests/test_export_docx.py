import inspect
import json
from pathlib import Path

import pytest
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from typer.testing import CliRunner

from codex_patent.cli import app
from codex_patent.export_docx import (
    SECTION_ORDER,
    TEMPLATE_PATH,
    export_application,
)
from codex_patent.models import ArtifactRef, ReviewIssue
from codex_patent.validation import ValidationReport


SECTIONS = {
    "技术领域": "本申请涉及支架技术领域。",
    "背景技术": "现有支架存在稳定性不足的问题。",
    "发明内容": "本申请提供一种折叠支架。",
    "附图说明": "图1为折叠支架的结构示意图。",
    "具体实施方式": "如图1所示，支架包括底座和支撑件。",
    "摘要": "本申请公开一种折叠支架。",
}
RUNNER = CliRunner()


def _export_kwargs(tmp_path: Path) -> dict:
    return {
        "title": "折叠支架",
        "claims": ["1. 一种折叠支架，其特征在于……"],
        "sections": SECTIONS,
        "output_path": tmp_path / "application.docx",
        "final_approval": True,
        "validation_report": ValidationReport(),
        "artifacts": [
            ArtifactRef(
                artifact_type=artifact_type,
                version=2,
                path=f"drafts/{artifact_type}-v2",
            )
            for artifact_type in (
                "claims",
                "specification",
                "abstract",
                "quality-review",
            )
        ],
    }


def test_export_contains_required_sections(tmp_path: Path):
    output = tmp_path / "application.docx"
    export_application(
        title="折叠支架",
        claims=["1. 一种折叠支架，其特征在于……"],
        sections=SECTIONS,
        output_path=output,
        final_approval=True,
        validation_report=ValidationReport(),
        artifacts=[],
    )

    text = "\n".join(paragraph.text for paragraph in Document(output).paragraphs)
    for heading in (
        "权利要求书",
        "技术领域",
        "背景技术",
        "发明内容",
        "附图说明",
        "具体实施方式",
        "摘要",
    ):
        assert heading in text

    paragraphs = Document(output).paragraphs
    observed = [paragraph.text for paragraph in paragraphs]
    assert observed.index("权利要求书") < observed.index("技术领域")
    for previous, following in zip(SECTION_ORDER, SECTION_ORDER[1:]):
        assert observed.index(previous) < observed.index(following)
    assert "1. 一种折叠支架，其特征在于……" in observed


def test_export_refuses_absent_final_approval_before_opening_template(
    tmp_path: Path,
):
    kwargs = _export_kwargs(tmp_path)
    kwargs["final_approval"] = False
    kwargs["template_path"] = tmp_path / "missing-template.docx"

    with pytest.raises(ValueError, match="final-delivery approval"):
        export_application(**kwargs)


def test_export_refuses_open_high_issue_before_opening_template(tmp_path: Path):
    kwargs = _export_kwargs(tmp_path)
    kwargs["validation_report"] = ValidationReport(
        issues=[
            ReviewIssue(
                issue_id="support-gap",
                severity="high",
                message="claim lacks support",
            )
        ]
    )
    kwargs["template_path"] = tmp_path / "missing-template.docx"

    with pytest.raises(ValueError, match="open high-severity"):
        export_application(**kwargs)


@pytest.mark.parametrize("artifact_type", ["specification", "quality-review", "docx"])
def test_export_refuses_stale_guarded_artifact_before_opening_template(
    tmp_path: Path,
    artifact_type: str,
):
    kwargs = _export_kwargs(tmp_path)
    kwargs["artifacts"] = [
        ArtifactRef(
            artifact_type=artifact_type,
            version=2,
            path=f"drafts/{artifact_type}-v2",
            stale=True,
        )
    ]
    kwargs["template_path"] = tmp_path / "missing-template.docx"

    with pytest.raises(ValueError, match=f"stale {artifact_type}"):
        export_application(**kwargs)


def test_delivery_guard_inputs_are_required_public_arguments():
    parameters = inspect.signature(export_application).parameters

    for parameter_name in ("final_approval", "validation_report", "artifacts"):
        assert parameters[parameter_name].default is inspect.Parameter.empty


def test_export_rejects_missing_section(tmp_path: Path):
    kwargs = _export_kwargs(tmp_path)
    kwargs["sections"] = {key: value for key, value in SECTIONS.items() if key != "摘要"}

    with pytest.raises(ValueError, match="missing required section: 摘要"):
        export_application(**kwargs)


def test_export_rejects_empty_claims(tmp_path: Path):
    kwargs = _export_kwargs(tmp_path)
    kwargs["claims"] = []

    with pytest.raises(ValueError, match="at least one claim"):
        export_application(**kwargs)


def test_export_creates_output_parent_directory(tmp_path: Path):
    kwargs = _export_kwargs(tmp_path)
    output = tmp_path / "nested" / "delivery" / "application.docx"
    kwargs["output_path"] = output

    assert export_application(**kwargs) == output
    assert output.is_file()


def test_default_template_is_loaded_and_styles_are_applied(tmp_path: Path):
    kwargs = _export_kwargs(tmp_path)
    output = kwargs["output_path"]

    export_application(**kwargs)

    document = Document(output)
    assert TEMPLATE_PATH.is_file()
    assert "Template Sentinel" in [style.name for style in document.styles]
    paragraphs = [paragraph for paragraph in document.paragraphs if paragraph.text]
    assert paragraphs[0].text == "折叠支架"
    assert paragraphs[0].style.name == "Patent Title"
    assert next(p for p in paragraphs if p.text == "权利要求书").style.name == (
        "Patent Heading 1"
    )
    assert next(p for p in paragraphs if p.text.startswith("1.")).style.name == (
        "Patent Claim"
    )
    assert next(p for p in paragraphs if p.text == SECTIONS["技术领域"]).style.name == (
        "Patent Body"
    )
    assert next(
        p for p in paragraphs if p.text == "技术领域"
    ).paragraph_format.page_break_before
    assert next(
        p for p in paragraphs if p.text == "摘要"
    ).paragraph_format.page_break_before


def test_template_encodes_cn_patent_application_style_tokens():
    document = Document(TEMPLATE_PATH)
    section = document.sections[0]

    one_twip = 635
    assert abs(section.page_width - Cm(21.0)) <= one_twip
    assert abs(section.page_height - Cm(29.7)) <= one_twip
    assert section.top_margin == Cm(2.54)
    assert section.right_margin == Cm(2.54)
    assert section.bottom_margin == Cm(2.54)
    assert section.left_margin == Cm(2.54)

    body = document.styles["Patent Body"]
    assert "Patent Figure Caption" in [style.name for style in document.styles]
    body_fonts = body.element.rPr.rFonts
    assert body.font.name == "Times New Roman"
    assert body.font.size == Pt(11)
    assert body_fonts.get(qn("w:eastAsia")) == "SimSun"
    assert body_fonts.get(qn("w:ascii")) == "Times New Roman"
    assert body.paragraph_format.line_spacing == 1.25
    assert body.paragraph_format.space_after == Pt(6)

    title = document.styles["Patent Title"]
    heading = document.styles["Patent Heading 1"]
    assert title.font.color.rgb is not None
    assert str(title.font.color.rgb) == "000000"
    assert str(heading.font.color.rgb) == "000000"
    assert title.paragraph_format.alignment == 1
    assert heading.paragraph_format.alignment == 1

    footer_xml = section.footer._element.xml
    assert 'w:instrText xml:space="preserve">PAGE</w:instrText>' in footer_xml


def test_export_cli_reads_explicit_json_input_package(tmp_path: Path):
    package = tmp_path / "export-package.json"
    output = tmp_path / "deliverables" / "application.docx"
    package.write_text(
        json.dumps(
            {
                "title": "折叠支架",
                "claims": ["1. 一种折叠支架，其特征在于……"],
                "sections": SECTIONS,
                "final_approval": True,
                "validation_report": {"issues": []},
                "artifacts": [
                    {
                        "artifact_type": artifact_type,
                        "version": 2,
                        "path": f"drafts/{artifact_type}-v2",
                        "stale": False,
                    }
                    for artifact_type in (
                        "claims",
                        "specification",
                        "abstract",
                        "quality-review",
                    )
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = RUNNER.invoke(app, ["export", str(package), str(output)])

    assert result.exit_code == 0
    assert result.stdout == f"{output}\n"
    assert output.is_file()


def test_export_cli_does_not_default_missing_final_approval_to_approved(
    tmp_path: Path,
):
    package = tmp_path / "unsafe-export-package.json"
    output = tmp_path / "application.docx"
    package.write_text(
        json.dumps(
            {
                "title": "折叠支架",
                "claims": ["1. 一种折叠支架，其特征在于……"],
                "sections": SECTIONS,
                "validation_report": {"issues": []},
                "artifacts": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = RUNNER.invoke(app, ["export", str(package), str(output)])

    assert result.exit_code != 0
    assert "final_approval" in result.output
    assert not output.exists()
