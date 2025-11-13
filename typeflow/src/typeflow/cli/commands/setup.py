import subprocess
from pathlib import Path
import typer
import sys
from ..template import gitignore, workflow_yaml
import os

def setup(app_name: str):
    """
    Create a new workflow project with the given app name.
    """
    root = Path(app_name)

    if root.exists():
        typer.echo(f"Error: {app_name} already exists!")
        raise typer.Exit(code=1)

    # Create internal folders
    (root / ".typeflow" / "nodes").mkdir(parents=True)
    (root / ".typeflow" / "classes").mkdir(parents=True)
    (root / ".typeflow" / "compiled").mkdir(parents=True)
    # (root / ".typeflow" / "consts").mkdir(parents=True)
    (root / "workflow").mkdir()

    # Create src structure
    src = root / "src"
    (src / "nodes").mkdir(parents=True)
    (src / "classes").mkdir(parents=True)

    # Create __init__.py files
    (src / "__init__.py").touch()
    (src / "nodes" / "__init__.py").touch()
    (src / "classes" / "__init__.py").touch()

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    typer.echo(f"🐍 Detected Python version: {python_version}")

    # Write templates
    (root / ".gitignore").write_text(gitignore.content)
    (root / "README.md").touch()
    (root / "workflow" / "workflow.yaml").write_text(
        workflow_yaml.content.format(workflow_name=app_name, python_version=python_version)
    )


    # Initialize uv project
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
        raise typer.Exit(code=1)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ uv init failed: {e}")
        raise typer.Exit(code=1)

    # Install typeflow inside project venv
    typer.echo("Installing typeflow inside project .venv...")
    try:
        subprocess.run(
            ["uv", "add", "typeflow"],
            cwd=root,
            check=True,
        )
        typer.echo("✅ typeflow installed in project .venv!")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to install typeflow in project .venv: {e}")

    # Instruction for user
    typer.echo("\n⚡ Project setup complete!")
    target_path = os.path.join(os.getcwd(), app_name)
    typer.echo(f"\nRun the following command:\n  cd {target_path}")
    typer.echo(f"👉 To activate the project environment, run:")
    if sys.platform.startswith("win"):
        typer.echo(f"    .venv\\Scripts\\Activate.ps1  # PowerShell")
    else:
        typer.echo(f"    source .venv/bin/activate  # Linux/macOS")
    typer.echo("After activation, you can run `typeflow` commands inside this environment. Play Around!")

    typer.echo(f"\nWorkflow project '{app_name}' created successfully!")
