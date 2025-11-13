from collections import deque
from pathlib import Path

from typeflow.utils import format_input_val, get_io_node, load_io_data

# -------------------------------
# Graph utilities
# -------------------------------


def find_parent(vertex, rev_adj_list):
    """Returns a list of (parent_node, source_handle, target_handle) tuples for the given vertex."""
    return rev_adj_list.get(vertex, [])


def topo_kahn(adj_list):
    """Return topological order using Kahn’s algorithm."""
    indegree = {node: 0 for node in adj_list}
    for src, edges in adj_list.items():
        for dest, _, _ in edges:
            indegree[dest] += 1

    queue = deque([n for n, d in indegree.items() if d == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor, _, _ in adj_list.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(adj_list):
        raise ValueError("Cycle detected in DAG")

    return order


# -------------------------------
# Helpers for code generation
# -------------------------------


send_output_def = """
import uuid, os, json
from pathlib import Path
from PIL import Image
from io import BytesIO
import numpy as np

OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
def send_output(value, type_, node):
    if type_ == "text":
        print(json.dumps(
            {"event": "node_output", "outputType": type_, "id" : node, "val": str(value)}
            ))
    elif type_ == "json":
        try:
            json.dumps(value)
            print(json.dumps(
                {"event": "node_output", "outputType": type_, "id": node, "val": value}
                ))
        except Exception:
            print(json.dumps(
                {"event": "node_output", "outputType": type_, "id": node, "val": str(value)}
                ))
    elif type_ == "table":
        if isinstance(value, pd.DataFrame):
            data = value.to_dict(orient="records")
        elif isinstance(value, list) and all(isinstance(x, dict) for x in value):
            data = value
        else:
            data = [{"value": v} for v in value]
        print(json.dumps({"event": "node_output", "outputType": "table", "id": node, "val": data}))
    elif type_ == "image":
        buf = BytesIO()
        if isinstance(value, np.ndarray):
            img = Image.fromarray(value)
            img.save(buf, format="PNG")
        elif isinstance(value, Image.Image):
            value.save(buf, format="PNG")
        else:
            print(json.dumps({
                "event": "node_error",
                "id": node,
                "msg": "Unsupported image type"
            }))
            return

        img_id = f"{uuid.uuid4().hex}.png"
        img_path = OUTPUT_DIR / img_id
        with open(img_path, "wb") as f:
            f.write(buf.getvalue())

        # Send only relative path or accessible URL
        print(json.dumps({
            "event": "node_output",
            "outputType": "image",
            "id": node,
            "val": f"/outputs/{img_id}"
        }))
        return
"""


def instance_name_from_cls_key(cls_key):
    if "@" in cls_key:
        cls, id_ = cls_key.split("@", 1)
        return f"{cls.lower()}_{id_}"
    return cls_key.lower()


def port_to_expr(src_node, src_handle):
    if src_node.startswith("X:"):
        name_id = src_node.split(":")[1]
        name, vid = name_id.split("@")
        return f"{name}_{vid}"
    elif src_node.startswith("C:"):
        parts = src_node.split(":")
        if len(parts) == 2:
            return instance_name_from_cls_key(parts[1])
        elif len(parts) >= 3:
            cls_key = parts[1]
            method = parts[2].split("@")[0]
            return f"{instance_name_from_cls_key(cls_key)}_{method}_out"
    elif src_node.startswith("F:"):
        func_key = src_node.split(":")[1]
        func_name = func_key.split("@")[0]
        return f"{func_name}_out"
    return src_node.replace(":", "_")


def generate_imports(adj_list):
    """Generate import lines based on nodes present in the DAG."""
    imports = set()

    for node in adj_list.keys():
        node_type = node.split(":")[0]
        body = node.split(":")[1]

        # handle nodes like F:console@1
        base_name = body.split("@")[0]

        if node_type == "F":
            imports.add(f"from src.nodes.{base_name}.main import {base_name}")
        elif node_type == "C":
            imports.add(f"from src.classes.{base_name} import {base_name}")
        # X: constants → no imports

    # sort for deterministic output
    return sorted(imports)


# -------------------------------
# Core script generator
# -------------------------------


def generate_script(adj_list, rev_adj_list, live=False, ports=None):
    """
    Generate Python code lines for orchestrator based on adjacency lists.
    """
    if not ports:
        ports = load_io_data()
    # print("ports: ",ports)
    topo_order = topo_kahn(adj_list)
    import_lines = generate_imports(adj_list)
    lines = ["# Auto-generated workflow script\n"]
    lines.extend(import_lines)
    lines.append("\n")
    if live:
        lines.append(send_output_def)
    lines.append("\n")

    def get_parents(node):
        return find_parent(node, rev_adj_list)

    for node in topo_order:
        node_type = node.split(":")[0]

        # ----- Input constants -----
        if node_type == "X":
            name_id = node.split(":")[1]
            name, vid = name_id.split("@")
            val = None
            node_data = get_io_node(node, ports)
            if node_data:
                val = format_input_val(node_data)
            lines.append(f"{name}_{vid} = {val}")
            continue

        # ----- Components -----
        if node_type == "C":
            parts = node.split(":")
            # ---- Base Component ----
            if len(parts) == 2:
                cls_key = parts[1]
                inst_var = instance_name_from_cls_key(cls_key)
                cls_name = cls_key.split("@")[0]
                parents = get_parents(node)

                # detect if any parent gives `self` input
                self_edge = next(
                    ((s, sh, th) for s, sh, th in parents if th == "self"), None
                )

                args = [
                    f"{th}={port_to_expr(s, sh)}"
                    for s, sh, th in parents
                    if th != "self"
                ]
                arg_str = ", ".join(args)
                if live:
                    lines.append(
                        f'print(json.dumps({{"event": "node_start", "id": "{node}"}}))'
                    )
                if self_edge:
                    src_node, src_handle, _ = self_edge
                    src_expr = port_to_expr(src_node, src_handle)
                    if src_handle == "output":
                        lines.append(f"{inst_var} = {src_expr}")
                    else:
                        lines.append(f"{inst_var} = {src_expr}.{cls_name.lower()}")
                else:
                    lines.append(f"{inst_var} = {cls_name}({arg_str})")
                if live:
                    lines.append(
                        f'print(json.dumps({{"event": "node_success", "id": "{node}"}}))'
                    )
                continue

            # ---- Subnode (method) ----
            if len(parts) >= 3:
                cls_key = parts[1]
                method = parts[2].split("@")[0]
                inst_var = instance_name_from_cls_key(cls_key)
                out_var = f"{inst_var}_{method}_out"
                parents = get_parents(node)

                args = [
                    f"{th}={port_to_expr(s, sh)}"
                    for s, sh, th in parents
                    if not (th == "self" and s.startswith(f"C:{cls_key}"))
                ]
                arg_str = ", ".join(args)
                if live:
                    lines.append(
                        f'print(json.dumps({{"event": "node_start", "id": "{node}"}}))'
                    )
                lines.append(f"{out_var} = {inst_var}.{method}({arg_str})")
                if live:
                    lines.append(
                        f'print(json.dumps({{"event": "node_success", "id": "{node}"}}))'
                    )
                continue

        # ----- Functions -----
        if node_type == "F":
            func_key = node.split(":")[1]
            func_name = func_key.split("@")[0]
            parents = get_parents(node)
            args = [f"{th}={port_to_expr(s, sh)}" for s, sh, th in parents]
            arg_str = ", ".join(args)

            if live:
                lines.append(
                    f'print(json.dumps({{"event": "node_start", "id": "{node}"}}))'
                )
            consumers_exist = any(
                node in [dst for dst, _, _ in edges] for edges in adj_list.values()
            )
            if consumers_exist:
                lines.append(f"{func_name}_out = {func_name}({arg_str})")
            else:
                lines.append(f"{func_name}({arg_str})")
            if live:
                lines.append(
                    f'print(json.dumps({{"event": "node_success", "id": "{node}"}}))'
                )
            continue

        if node_type == "O":
            parts = node.split(":")
            out_key = parts[1]  # text_out@3
            out_type = out_key.split("_")[0]  # "text", "json", "table", "image"
            parents = get_parents(node)
            if len(parents) != 1:
                raise ValueError(f"Output node {node} must have exactly one parent")
            src_node, src_handle, _ = parents[0]
            expr = port_to_expr(src_node, src_handle)

            if live:
                lines.append(
                    f'print(json.dumps({{"event": "node_start", "id": "{node}"}}))'
                )
                lines.append(f"send_output({expr}, '{out_type}', '{node}')")
                lines.append(
                    f'print(json.dumps({{"event": "node_success", "id": "{node}"}}))'
                )
            continue
    if live:
        lines.append(
            "\nprint(json.dumps({'event': 'workflow_complete', 'data': None}))"
        )
    lines.append("\n# End of generated workflow\n")
    return "\n".join(lines)


def write_script_to_file(script: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script)
