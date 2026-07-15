from pathlib import Path

import typer
from pydantic import BaseModel, ConfigDict, ValidationError

from codex_patent.export_docx import export_application
from codex_patent.models import ArtifactRef, PatentCase
from codex_patent.repository import CaseRepository
from codex_patent.validation import ValidationReport


app = typer.Typer(no_args_is_help=True)


class ExportInputPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    claims: list[str]
    sections: dict[str, str]
    final_approval: bool
    validation_report: ValidationReport
    artifacts: list[ArtifactRef]


@app.callback()
def main() -> None:
    pass


@app.command()
def version() -> None:
    from codex_patent import __version__
    typer.echo(__version__)


@app.command("case-create")
def case_create(case_id: str, title: str, workspace: Path = Path("cases")) -> None:
    repo = CaseRepository(workspace)
    repo.create(PatentCase(case_id=case_id, title=title))
    typer.echo(str(repo.case_dir(case_id)))


@app.command("export")
def export_command(
    input_package: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="UTF-8 JSON export package with explicit approval and guard inputs.",
    ),
    output_path: Path = typer.Argument(..., dir_okay=False),
    template: Path | None = typer.Option(
        None,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional DOCX template override.",
    ),
) -> None:
    try:
        package = ExportInputPackage.model_validate_json(
            input_package.read_text(encoding="utf-8")
        )
        result = export_application(
            title=package.title,
            claims=package.claims,
            sections=package.sections,
            output_path=output_path,
            final_approval=package.final_approval,
            validation_report=package.validation_report,
            artifacts=package.artifacts,
            template_path=template,
        )
    except ValidationError as exc:
        raise typer.BadParameter(
            f"invalid export package: {exc}", param_hint="input-package"
        ) from exc
    except ValueError as exc:
        raise typer.BadParameter(str(exc), param_hint="input-package") from exc
    typer.echo(str(result))
