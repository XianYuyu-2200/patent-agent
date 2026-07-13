import typer


app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    pass


@app.command()
def version() -> None:
    from codex_patent import __version__
    typer.echo(__version__)
