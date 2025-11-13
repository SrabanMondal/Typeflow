import ast
from pathlib import Path

import typer
import yaml


def check_decorator(file_path: Path, decorator_name: str) -> bool:
    """
    Check if the file contains a function/class using the given decorator,
    supports both @decorator and @decorator() forms.
    """
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Name) and dec.id == decorator_name:
                    return True
                if (
                    isinstance(dec, ast.Call)
                    and isinstance(dec.func, ast.Name)
                    and dec.func.id == decorator_name
                ):
                    return True
    return False


def update_workflow_yaml(item_name: str, section: str):
    cwd = Path.cwd()
    workflow_file = cwd / "workflow" / "workflow.yaml"
    if not workflow_file.exists():
        typer.echo("Error: workflow.yaml not found!")
        raise typer.Exit(code=1)

    with open(workflow_file) as f:
        data = yaml.safe_load(f) or {}

    if section not in data:
        data[section] = []

    if item_name not in data[section]:
        data[section].append(item_name)

    with open(workflow_file, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
