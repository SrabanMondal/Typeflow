# import ast
# import subprocess
# import sys
# from pathlib import Path

# import typer
# import yaml

# app = typer.Typer(help="Validate nodes or classes")


# def check_decorator(file_path: Path, decorator_name: str) -> bool:
#     """
#     Check if the file contains a function/class using the given decorator,
#     supports both @decorator and @decorator() forms.
#     """
#     with open(file_path, "r") as f:
#         tree = ast.parse(f.read(), filename=str(file_path))

#     for node in ast.walk(tree):
#         if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
#             for dec in node.decorator_list:
#                 if isinstance(dec, ast.Name) and dec.id == decorator_name:
#                     return True
#                 if (
#                     isinstance(dec, ast.Call)
#                     and isinstance(dec.func, ast.Name)
#                     and dec.func.id == decorator_name
#                 ):
#                     return True
#     return False


# def update_workflow_yaml(item_name: str, section: str):
#     cwd = Path.cwd()
#     workflow_file = cwd / "workflow" / "workflow.yaml"
#     if not workflow_file.exists():
#         typer.echo("Error: workflow.yaml not found!")
#         raise typer.Exit(code=1)

#     with open(workflow_file) as f:
#         data = yaml.safe_load(f) or {}

#     if section not in data:
#         data[section] = []

#     if item_name not in data[section]:
#         data[section].append(item_name)

#     with open(workflow_file, "w") as f:
#         yaml.safe_dump(data, f, sort_keys=False)


# # ---------------- NODE SUBCOMMAND ----------------

# @app.command("node")
# def validate_node(node_name: str = typer.Argument(None)):
#     cwd = Path.cwd()
#     if not (cwd / ".typeflow").exists():
#         typer.echo("Error: Cannot detect .typeflow folder. Run from project root.")
#         raise typer.Exit(code=1)
    
#     nodes_dir = cwd / "src" / "nodes"
    
#     if node_name is None:
#         typer.echo("No node name provided — validating all nodes in src/nodes/...")

#         node_dirs = [d for d in nodes_dir.iterdir() if (d / "main.py").exists()]

#         if not node_dirs:
#             typer.echo("No valid nodes found in src/nodes/")
#             raise typer.Exit(code=1)

#         for node_dir in node_dirs:
#             node = node_dir.name
#             typer.echo(f"\n➡ Validating node: {node}")
#             validate_node(node)  # recursively validate each node
#         return
#     node_file = cwd / "src" / "nodes" / node_name / "main.py"
#     if not node_file.exists():
#         typer.echo(f"Error: Node '{node_name}' does not exist.")
#         raise typer.Exit(code=1)
#     module_path = f"src.nodes.{node_name}.main"

#     try:
#         subprocess.run(
#             [sys.executable, "-m", module_path],
#             cwd=cwd,
#             check=True,
#         )
#     except subprocess.CalledProcessError as e:
#         typer.echo(f"Runtime Error in node '{node_name}': {e}")
#         raise typer.Exit(code=1)

#     if not check_decorator(node_file, "node"):
#         typer.echo(f"Error: Node '{node_name}' does not have @node decorator.")
#         raise typer.Exit(code=1)

#     update_workflow_yaml(node_name, "nodes")
#     typer.echo(f"Node '{node_name}' validated and added to workflow.yaml")


# # ---------------- CLASS SUBCOMMAND ----------------
# @app.command("class")
# def validate_class(class_name: str = typer.Argument(None)):
#     cwd = Path.cwd()
#     if not (cwd / ".typeflow").exists():
#         typer.echo("Error: Cannot detect .typeflow folder. Run from project root.")
#         raise typer.Exit(code=1)
#     classes_dir = cwd / "src" / "classes"
    
#     if class_name is None:
#         typer.echo("No class name provided — running validation for all classes...")
#         py_files = [f for f in classes_dir.glob("*.py") if f.name != "__init__.py"]

#         if not py_files:
#             typer.echo("No Python files found in src/classes/")
#             raise typer.Exit(code=1)

#         for file in py_files:
#             cls_name = file.stem
#             typer.echo(f"\n➡ Validating class: {cls_name}")
#             validate_class(cls_name)
#         return
    
#     class_file = cwd / "src" / "classes" / f"{class_name}.py"
#     if not class_file.exists():
#         typer.echo(f"Error: Class '{class_name}' does not exist.")
#         raise typer.Exit(code=1)

#     module_path = f"src.classes.{class_name}"

#     try:
#         subprocess.run(
#             [sys.executable, "-m", module_path],
#             cwd=cwd,
#             check=True,
#         )
#     except subprocess.CalledProcessError as e:
#         typer.echo(f"Runtime Error in node '{class_name}': {e}")
#         raise typer.Exit(code=1)

#     if not check_decorator(class_file, "node_class"):
#         typer.echo(f"Error: Class '{class_name}' does not have @node_class decorator.")
#         raise typer.Exit(code=1)

#     update_workflow_yaml(class_name, "classes")
#     typer.echo(f"Class '{class_name}' validated and added to workflow.yaml")
