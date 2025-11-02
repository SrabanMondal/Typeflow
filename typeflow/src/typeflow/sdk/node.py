import inspect
import os
from functools import wraps
from typing import get_type_hints

import yaml

from typeflow.utils import get_project_root, simplify_type, validate_type


def node():
    """Function decorator for visual editor"""

    def decorator(func):
        type_hints = get_type_hints(func)
        sig = inspect.signature(func)

        for param_name in sig.parameters:
            if param_name not in type_hints:
                raise ValueError(
                    f"Missing type hint for parameter '{param_name}' in function '{func.__name__}'."
                    "Please provide type hints."
                )
        if "return" not in type_hints:
            raise ValueError(
                f"Missing return type hint for function '{func.__name__}'."
                " Please provide type hints."
            )

        for field, field_type in type_hints.items():
            validate_type(field_type)

        metadata = {
            "name": func.__name__,
            "node_type": "private",
            "entity": "function",
            "inputs": {
                param_name: simplify_type(type_hints.get(param_name))
                for param_name in sig.parameters
            },
            "returns": simplify_type(type_hints.get("return")),
            "description": (
                func.__doc__.strip() if func.__doc__ and func.__doc__.strip() else None
            ),
        }

        if not metadata["description"]:
            param_names = ", ".join(sig.parameters.keys())
            metadata["description"] = (
                f"Function '{func.__name__}' takes parameters {param_names or 'none'}"
                f"It returns a value of type {metadata['returns']}."
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
