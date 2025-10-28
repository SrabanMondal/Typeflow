import subprocess
from pathlib import Path

import typer
import yaml

WORKFLOW_PATH = Path.cwd() / "workflow" / "workflow.yaml"


def install_packages(packages: list[str]):
    """Install packages using uv."""
    for pkg in packages:
        typer.echo(f"📦 Installing {pkg} ...")
        try:
            subprocess.run(["uv", "add", pkg], check=True)
        except subprocess.CalledProcessError:
            typer.echo(f"❌ Failed to install {pkg}. Check your environment.")
            raise typer.Exit(1)
    typer.echo("✅ Installation complete!")


def update_workflow_yaml(packages: list[str]):
    """Update dependencies in workflow/workflow.yaml."""
    if not WORKFLOW_PATH.exists():
        typer.echo("⚠️  first setup project using `typeflow setup <project_name>`")
        raise typer.Exit(1)

    with open(WORKFLOW_PATH, "r") as f:
        data = yaml.safe_load(f) or {}

    # Ensure the YAML has a dependencies key
    deps = set(data.get("dependencies", []))
    deps.update(packages)
    data["dependencies"] = sorted(deps)

    with open(WORKFLOW_PATH, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    typer.echo(f"🧩 Updated dependencies: {', '.join(packages)}")


def add(packages: list[str] = typer.Argument(..., help="Packages to add")):
    """Add dependencies to the workflow."""
    install_packages(packages)
    update_workflow_yaml(packages)
