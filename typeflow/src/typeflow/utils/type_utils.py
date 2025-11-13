import re
from typing import Any, get_args, get_origin


def short_typename(t: Any) -> str:
    """Get short readable typename (no typing. prefix)."""
    if t is None:
        return "NoneType"

    if hasattr(t, "__name__"):
        return t.__name__
    if hasattr(t, "__qualname__"):
        return t.__qualname__

    s = str(t)
    s = re.sub(r"^typing\.|^types\.|^collections\.abc\.", "", s)
    return s


def simplify_type(t: Any) -> str:
    """Helper function to convert type hints to simple string format."""
    if t is None:
        return "NoneType"
    if isinstance(t, type):
        return t.__name__
    origin = get_origin(t)
    args = get_args(t)
    if origin:
        origin_name = (
            origin.__name__ if isinstance(origin, type) else short_typename(origin)
        )
        if args:
            arg_types = ", ".join(simplify_type(arg) for arg in args)
            return f"{origin_name}[{arg_types}]"
        return origin_name
    return short_typename(t)


def validate_type(t: Any):
    """Recursively validate type: must be valid Python type or node_class."""
    try:
        origin = get_origin(t)
        args = get_args(t)
    except Exception as e:
        raise ValueError(f"Invalid type hint: {t!r} ({e})")

    if origin:
        for arg in args:
            validate_type(arg)
        return

    if isinstance(t, type):
        if t.__module__ == "builtins":
            return
        if getattr(t, "__is_node_class__", False):
            return
        return

    if t is Any or t is None:
        return
    if isinstance(t, str):
        raise ValueError(f"Forward reference strings not allowed in strict mode: {t}")

    raise ValueError(f"Unsupported or invalid type: {t!r}")
