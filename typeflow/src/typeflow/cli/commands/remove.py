import subprocess
from pathlib import Path

import typer
import yaml

WORKFLOW_PATH = Path.cwd() / "workflow" / "workflow.yaml"

def uninstall_packages(packages: list[str]):
    """Uninstall packages using uv."""
    for pkg in packages:
        typer.echo(f"🗑️  Removing {pkg} ...")
        try:
            subprocess.run(["uv", "remove", pkg], check=True)
        except subprocess.CalledProcessError:
            typer.echo(f"❌ Failed to remove {pkg}. Check your environment.")
            raise typer.Exit(1)
    typer.echo("✅ Removal complete!")


def remove_from_workflow_yaml(packages: list[str]):
    """Remove dependencies from workflow/workflow.yaml."""
    if not WORKFLOW_PATH.exists():
        typer.echo("⚠️  first setup project using `typeflow setup <project_name>`")
        raise typer.Exit(1)

    with open(WORKFLOW_PATH, "r") as f:
        data = yaml.safe_load(f) or {}

    deps = set(data.get("dependencies", []))
    removed = []

    for pkg in packages:
        if pkg in deps:
            deps.remove(pkg)
            removed.append(pkg)

    data["dependencies"] = sorted(deps)

    with open(WORKFLOW_PATH, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    if removed:
        typer.echo(f"🧩 Removed dependencies: {', '.join(removed)}")
    else:
        typer.echo("ℹ️  No matching dependencies were found to remove.")


def remove(packages: list[str] = typer.Argument(..., help="Packages to remove")):
    """Remove dependencies from the workflow."""
    uninstall_packages(packages)
    remove_from_workflow_yaml(packages)
