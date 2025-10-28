from collections import deque
from pathlib import Path
from typeflow.utils import load_const, format_yaml_val
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


def instance_name_from_cls_key(cls_key):
    if "@" in cls_key:
        cls, id_ = cls_key.split("@", 1)
        return f"{cls.lower()}_{id_}"
    return cls_key.lower()


def port_to_expr(src_node, src_handle):
    if src_node.startswith("X:"):
        return src_node.split(":")[1]
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


def generate_script(adj_list, rev_adj_list):
    """
    Generate Python code lines for orchestrator based on adjacency lists.
    """
    ports = load_const()
    print(ports)
    topo_order = topo_kahn(adj_list)
    import_lines = generate_imports(adj_list)
    lines = ["# Auto-generated workflow script\n"]
    lines.extend(import_lines)
    lines.append("\n")
    
    def get_parents(node):
        return find_parent(node, rev_adj_list)

    for node in topo_order:
        node_type = node.split(":")[0]

        # ----- Input constants -----
        if node_type == "X":
            name = node.split(":")[1]
            val = None
            node_data = ports.get(name, None)
            if node_data:
                val = format_yaml_val(node_data)
            lines.append(f"{name} = {val}")
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

                if self_edge:
                    src_node, src_handle, _ = self_edge
                    src_expr = port_to_expr(src_node, src_handle)
                    if src_handle == "output":
                        lines.append(f"{inst_var} = {src_expr}")
                    else:
                        lines.append(f"{inst_var} = {src_expr}.{cls_name.lower()}")
                else:
                    lines.append(f"{inst_var} = {cls_name}({arg_str})")
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
                lines.append(f"{out_var} = {inst_var}.{method}({arg_str})")
                continue

        # ----- Functions -----
        if node_type == "F":
            func_key = node.split(":")[1]
            func_name = func_key.split("@")[0]
            parents = get_parents(node)
            args = [f"{th}={port_to_expr(s, sh)}" for s, sh, th in parents]
            arg_str = ", ".join(args)

            # assign only if has consumers
            consumers_exist = any(
                node in [dst for dst, _, _ in edges] for edges in adj_list.values()
            )
            if consumers_exist:
                lines.append(f"{func_name}_out = {func_name}({arg_str})")
            else:
                lines.append(f"{func_name}({arg_str})")
            continue

    lines.append("\n# End of generated workflow\n")
    return "\n".join(lines)


def write_script_to_file(script: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script)
