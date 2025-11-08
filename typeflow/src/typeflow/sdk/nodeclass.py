import inspect
import os
from typing import get_type_hints

import yaml

from typeflow.utils import get_project_root, simplify_type, validate_type


def node_class(cls):
    """Function decorator for visual editor"""
    if not inspect.isclass(cls):
        raise TypeError(
            f"@node_class can only decorate classes, not {type(cls).__name__}"
        )

    cls.__is_node_class__ = True

    type_hints = get_type_hints(cls)
    defaults = {k: getattr(cls, k) for k in type_hints.keys() if hasattr(cls, k)}

    if "__init__" in cls.__dict__:
        delattr(cls, "__init__")

    def __init__(self, **kwargs):
        for field_name, field_type in type_hints.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            elif field_name in defaults:
                setattr(self, field_name, defaults[field_name])
            else:
                raise TypeError(f"Missing required field: {field_name}")

    setattr(cls, "__init__", __init__)

    for field_name, field_type in type_hints.items():
        validate_type(field_type)

    metadata = {
        "entity": "class",
        "name": cls.__name__,
        "description": inspect.getdoc(cls) or "",
        "fields": {},
        "methods": {},
    }

    # Fields → ports
        
    for field_name, field_type in type_hints.items():
        metadata["fields"][field_name] = simplify_type(field_type)
    metadata["fields"]["self"] = cls.__name__

    # Methods → callable ports
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name.startswith("__"):
            continue

        sig = inspect.signature(method)
        
        for p in sig.parameters.values():
            if p.name != "self":
                validate_type(p.annotation)
                
        params = {
            p.name: simplify_type(p.annotation)
            for p in sig.parameters.values()
            if p.name != "self"
        }
        params["self"] = cls.__name__
        validate_type(sig.return_annotation)
        ret_type = simplify_type(sig.return_annotation)

        metadata["methods"][name] = {
            "input": params,
            "returns": ret_type,
            "description": inspect.getdoc(method) or "",
            "is_static": isinstance(cls.__dict__.get(name), staticmethod),
        }

    # ---------- Save YAML ----------
    project_root = get_project_root()
    class_dir = os.path.join(project_root, ".typeflow", "classes")
    try:
        os.makedirs(class_dir, exist_ok=True)
    except PermissionError:
        raise PermissionError(
            f"Cannot create directory '{class_dir}'. Please check permissions."
        )
    yaml_file_path = os.path.join(class_dir, f"{cls.__name__}.yaml")
    try:
        with open(yaml_file_path, "w") as f:
            yaml.dump(metadata, f, sort_keys=False, default_flow_style=False)

        # print(f"Manifest for: {cls.__name__} -> {yaml_file_path}")
    except PermissionError:
        raise PermissionError(
            f"Cannot write to '{yaml_file_path}'. Please check permissions."
        )

    return cls
