from pathlib import Path

import typer

from ..template import node_template


MAIN_PY_TEMPLATE = node_template.NODE_TEMPLATE

def create_node(node_name: str):
    """
    Create a new node under nodes/ folder.
    """
    cwd = Path.cwd()

    if not (cwd / ".typeflow").exists():
        typer.echo("Error: Cannot detect .typeflow folder."
                   "Run this command from the root of your typeflow project.")
        raise typer.Exit(code=1)

    node_folder = cwd / "nodes" / node_name
    if node_folder.exists():
        typer.echo(f"Error: Node '{node_name}' already exists.")
        raise typer.Exit(code=1)

    node_folder.mkdir(parents=True)

    (node_folder / "__init__.py").touch()

    main_py_content = MAIN_PY_TEMPLATE.format(func_name=node_name)
    (node_folder / "main.py").write_text(main_py_content)

    typer.echo(f"Node '{node_name}' created successfully in nodes/{node_name}")
