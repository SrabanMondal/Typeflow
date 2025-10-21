import inspect
import os
from functools import wraps
from pathlib import Path
from typing import get_args, get_origin, get_type_hints

import yaml


def simplify_type(t):
    """Helper function to convert type hints to simple string format."""
    if t is None or t == "No type hint":
        return t
    if isinstance(t, type):
        return t.__name__
    origin = get_origin(t)
    args = get_args(t)
    if origin:
        origin_name = origin.__name__ if isinstance(origin, type) else str(origin)
        if args:
            arg_types = ", ".join(simplify_type(arg) for arg in args)
            return f"{origin_name}[{arg_types}]"
        return origin_name
    return t.__name__ if hasattr(t, "__name__") else str(t)


def get_project_root():
    """Find the project root by looking for .typeflow folder in current, parent, or parent-parent directory."""
    current_dir = Path.cwd()
    for directory in [current_dir, current_dir.parent, current_dir.parent.parent]:
        typeflow_dir = directory / ".typeflow"
        if typeflow_dir.exists() and typeflow_dir.is_dir():
            return str(directory)
    raise FileNotFoundError(
        "Could not find .typeflow folder in current directory, parent, or parent-parent directory. Please run from a directory containing .typeflow."
    )


def node():
    """Decorator to inspect function metadata, print it, and save to YAML file in .typeflow/nodes/."""

    def decorator(func):
        type_hints = get_type_hints(func)
        sig = inspect.signature(func)

        for param_name in sig.parameters:
            if param_name not in type_hints:
                raise ValueError(
                    f"Missing type hint for parameter '{param_name}' in function '{func.__name__}'. Please provide type hints."
                )
        if "return" not in type_hints:
            raise ValueError(
                f"Missing return type hint for function '{func.__name__}'. Please provide type hints."
            )

        metadata = {
            "name": func.__name__,
            "node_type":"private",
            "inputs": {
                param_name: simplify_type(type_hints.get(param_name))
                for param_name in sig.parameters
            },
            "output": simplify_type(type_hints.get("return")),
            "description": (
                func.__doc__.strip() if func.__doc__ and func.__doc__.strip() else None
            ),
        }

        if not metadata["description"]:
            param_names = ", ".join(sig.parameters.keys())
            metadata["description"] = (
                f"Function '{func.__name__}' takes parameters {param_names or 'none'} and returns a value of type {metadata["output"]}."
            )

        project_root = get_project_root()
        nodes_dir = os.path.join(project_root, ".typeflow", "nodes")
        try:
            os.makedirs(nodes_dir, exist_ok=True)
        except PermissionError:
            raise PermissionError(
                f"Cannot create directory '{nodes_dir}'. Please check permissions."
            )

        yaml_file_path = os.path.join(nodes_dir, f"{func.__name__}.yaml")
        try:
            with open(yaml_file_path, "w") as yaml_file:
                yaml.dump(
                    metadata, yaml_file, default_flow_style=False, sort_keys=False
                )
            print(f"Node manifest saved to: {yaml_file_path}")
        except PermissionError:
            raise PermissionError(
                f"Cannot write to '{yaml_file_path}'. Please check permissions."
            )

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
