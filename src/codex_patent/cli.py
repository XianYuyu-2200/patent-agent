from pathlib import Path

import typer

from codex_patent.models import PatentCase
from codex_patent.repository import CaseRepository


app = typer.Typer(no_args_is_help=True)


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
