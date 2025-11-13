# commands/validate/validate_workflow.py

from pathlib import Path

import typer
import yaml

from .validate_class import validate_class
from .validate_node import validate_node


def validate_workflow():
    cwd = Path.cwd()
    workflow_file = cwd / "workflow" / "workflow.yaml"

    if not workflow_file.exists():
        typer.echo("Error: workflow.yaml not found!")
        raise typer.Exit(code=1)

    with open(workflow_file) as f:
        data = yaml.safe_load(f) or {}

    nodes = data.get("nodes", [])
    classes = data.get("classes", [])

    typer.echo("\n=== Validating Workflow Defined Elements ===")

    if nodes:
        typer.echo(f"\n🧩 Validating {len(nodes)} nodes:")
        for node in nodes:
            typer.echo(f" -> Node: {node}")
            validate_node(node)

    if classes:
        typer.echo(f"\n🏗️ Validating {len(classes)} classes:")
        for cls in classes:
            typer.echo(f" -> Class: {cls}")
            validate_class(cls)

    typer.echo("\n✅ Workflow validation complete!")
