import typer

from .commands import (
    add,
    remove,
    compile_graph,
    create_class,
    create_node,
    generate,
    install,
    run,
    setup,
    start_ui,
    validate,
)

app = typer.Typer(
    name="typeflow",
    help="TypeFlow CLI tool for workflow automation",
    add_completion=False,
)


@app.callback()
def main():
    """TypeFlow CLI tool for workflow automation."""
    pass


app.command()(setup.setup)
app.command()(create_class.create_class)
app.command()(create_node.create_node)
app.command()(add.add)
app.command()(remove.remove)
app.command()(compile_graph.compile)
app.command()(generate.generate)
app.command()(start_ui.start_ui)
app.command()(run.run)
app.command()(install.install)
app.add_typer(validate.app, name="validate")

if __name__ == "__main__":
    app()
