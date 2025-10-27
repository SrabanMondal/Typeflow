import typer

from typeflow.core.first import greet

from .commands import create_class, create_node, setup, validate

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

app.command()(setup.setup)
app.command()(create_class.create_class)
app.command()(create_node.create_node)
app.add_typer(validate.app, name="validate")

if __name__ == "__main__":
    app()
