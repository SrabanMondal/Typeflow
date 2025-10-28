from pathlib import Path
import subprocess
import typer

from ..template import gitignore, workflow_yaml


def setup(app_name: str):
    """
    Create a new workflow project with the given app name.
    Structure:
    app_name/
        src/
            __init__.py
            nodes/
                __init__.py
            classes/
                __init__.py
        .typeflow/
            nodes/
            classes/
        workflow/
            workflow.yaml
        .gitignore
        README.md
    """
    root = Path(app_name)

    if root.exists():
        typer.echo(f"Error: {app_name} already exists!")
        raise typer.Exit(code=1)

    # Create internal folders
    (root / ".typeflow" / "nodes").mkdir(parents=True)
    (root / ".typeflow" / "classes").mkdir(parents=True)
    (root / ".typeflow" / "compiled").mkdir(parents=True)
    (root / ".typeflow" / "consts").mkdir(parents=True)
    (root / "workflow").mkdir()

    # Create src structure
    src = root / "src"
    (src / "nodes").mkdir(parents=True)
    (src / "classes").mkdir(parents=True)

    # Create __init__.py files
    (src / "__init__.py").touch()
    (src / "nodes" / "__init__.py").touch()
    (src / "classes" / "__init__.py").touch()

    # Write templates
    (root / ".gitignore").write_text(gitignore.content)
    (root / "README.md").touch()
    (root / "workflow" / "workflow.yaml").write_text(
        workflow_yaml.content.format(workflow_name=app_name)
    )
    typer.echo("Initializing uv project...")
    try:
        subprocess.run(
            ["uv", "init"],
            cwd=root,
            check=True,
        )
        typer.echo("✅ uv project initialized successfully!")
    except FileNotFoundError:
        typer.echo("⚠️  'uv' not found! Please install it with `pip install uv`.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ uv init failed: {e}")


    typer.echo(f"Workflow project '{app_name}' created successfully!")
