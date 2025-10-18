import typer

from typeflow.core.first import greet

app = typer.Typer(
    name="typeflow",
    help="TypeFlow CLI tool for workflow automation",
    add_completion=False,
)


@app.callback()
def main():
    """TypeFlow CLI tool for workflow automation."""
    pass


@app.command()
def hello(name: str) -> None:
    """Simple CLI command to greet someone."""
    typer.echo(greet(name))


if __name__ == "__main__":
    app()
