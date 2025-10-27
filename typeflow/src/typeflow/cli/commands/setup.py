from pathlib import Path

import typer

from ..template import gitignore, workflow_yaml


def setup(app_name: str):
    """
    Create a new workflow project with the given app name
    """
    root = Path(app_name)

    if root.exists():
        typer.echo(f"Error: {app_name} already exists!")
        raise typer.Exit(code=1)

    # Create main folders
    (root / ".typeflow" / "nodes").mkdir(parents=True)
    (root / ".typeflow" / "class").mkdir(parents=True)
    (root / "workflow").mkdir()
    (root / "nodes").mkdir()
    (root / "class").mkdir()

    # Create __init__.py files
    (root / "nodes" / "__init__.py").touch()
    (root / "class" / "__init__.py").touch()

    # Write templates
    (root / ".gitignore").write_text(gitignore.content)
    (root / "workflow" / "workflow.yaml").write_text(
        workflow_yaml.content.format(workflow_name=app_name)
    )

    typer.echo(f"Workflow project '{app_name}' created successfully!")
