from pathlib import Path

import typer

from ..template import class_template


def create_class(class_name: str):
    """
    Create a new class under class/ folder.
    """
    cwd = Path.cwd()

    # Check for .typeflow folder
    if not (cwd / ".typeflow").exists():
        typer.echo("Error: Cannot detect .typeflow folder."
                   "Run this command from the root of your typeflow project.")
        raise typer.Exit(code=1)

    class_folder = cwd / "class"
    class_folder.mkdir(exist_ok=True)

    class_file = class_folder / f"{class_name}.py"
    if class_file.exists():
        typer.echo(f"Error: Class '{class_name}' already exists.")
        raise typer.Exit(code=1)

    # Write template to class file
    class_file.write_text(class_template.content.format(class_name=class_name))

    typer.echo(f"Class '{class_name}' created successfully in class/{class_name}.py")
