import typer
import subprocess
import sys
from pathlib import Path
from .utils import check_decorator, update_workflow_yaml


def validate_node(node_name: str = typer.Argument(None)):
    cwd = Path.cwd()

    if not (cwd / ".typeflow").exists():
        typer.echo("Error: Cannot detect .typeflow folder. Run from project root.")
        raise typer.Exit(code=1)

    nodes_dir = cwd / "src" / "nodes"

    if node_name is None:
        typer.echo("No node name provided — validating all nodes...")
        node_dirs = [d for d in nodes_dir.iterdir() if (d / "main.py").exists()]

        for node_dir in node_dirs:
            validate_node(node_dir.name)
        return

    node_file = nodes_dir / node_name / "main.py"

    if not node_file.exists():
        typer.echo(f"Error: Node '{node_name}' does not exist.")
        raise typer.Exit(code=1)

    module_path = f"src.nodes.{node_name}.main"

    try:
        subprocess.run([sys.executable, "-m", module_path], cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Runtime Error in node '{node_name}': {e}")
        raise typer.Exit(code=1)

    if not check_decorator(node_file, "node"):
        typer.echo(f"Error: Node '{node_name}' does not have @node decorator.")
        raise typer.Exit(code=1)

    update_workflow_yaml(node_name, "nodes")
    typer.echo(f"Node '{node_name}' validated and added to workflow.yaml")
