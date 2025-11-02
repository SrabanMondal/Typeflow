import os

import yaml


# ------------------------------
# Adjacency list creator
# ------------------------------
def create_adjacency_lists(workflow_json):
    adj_list = {}
    rev_adj_list = {}

    # Add all nodes and sub-nodes
    for node in workflow_json["nodes"]:
        adj_list[node["id"]] = []
        rev_adj_list[node["id"]] = []
        if node["data"].get("subNodes"):
            for sub_node in node["data"]["subNodes"]:
                adj_list[sub_node["id"]] = []
                rev_adj_list[sub_node["id"]] = []
                adj_list[node["id"]].append((sub_node["id"], "self", "self"))
                rev_adj_list[sub_node["id"]].append((node["id"], "self", "self"))

    # Add edges except internal ones
    for conn in workflow_json["connections"]:
        if conn.get("type") == "internal":
            continue
        source = conn["source"]
        target = conn["target"]
        source_handle = conn["sourceHandle"]
        target_handle = conn["targetHandle"]

        adj_list[source].append((target, source_handle, target_handle))
        rev_adj_list[target].append((source, source_handle, target_handle))

    return adj_list, rev_adj_list


# ------------------------------
# Type validation helpers
# ------------------------------
NODES_DIR = ".typeflow/nodes"
CLASS_DIR = ".typeflow/classes"
CONST_DIR = ".typeflow/consts"

class_yaml, func_yaml, const_yaml = {}, {}, {}


def load_yaml_definitions():
    """Load YAML definitions from nodes and classes dirs."""
    for directory in [NODES_DIR, CLASS_DIR, CONST_DIR]:
        if not os.path.exists(directory):
            continue

        for fname in os.listdir(directory):
            if fname.endswith(".yaml"):
                path = os.path.join(directory, fname)
                with open(path) as f:
                    data = yaml.safe_load(f)
                    if not data:
                        continue
                    if data.get("entity") == "class":
                        class_yaml[data["name"]] = data
                    elif data.get("entity") == "function":
                        func_yaml[data["name"]] = data
                    else:
                        const_yaml[data["name"]] = data


def lookup_port_type(port_str):
    """Get data type for a given port string."""
    node_type, rest = port_str.split(":", 1)
    if node_type == "C":
        parts = rest.split(":")
        cls_name = parts[0].split("@")[0]
        meta = class_yaml[cls_name]
        if len(parts) == 2:  # Field
            field_name = parts[1]
            return meta["fields"][field_name]

        elif len(parts) == 3:  # Method
            method_id, port = parts[1], parts[2]
            method_name = method_id.split("@")[0]
            method_meta = meta["methods"][method_name]

            if port == "returns":
                return method_meta["returns"]
            else:
                return method_meta["input"][port]

        else:
            raise ValueError(f"Invalid class port format: {port_str}")

    elif node_type == "F":
        func_id, port = rest.split(":")
        func_name = func_id.split("@")[0]
        meta = func_yaml[func_name]
        if port == "returns":
            return meta["returns"]
        else:
            return meta["inputs"][port]

    elif node_type == "X":
        const_name = rest.split(":")[0]
        return const_yaml[const_name]["output"]

    else:
        raise ValueError(f"Unknown node prefix: {node_type}")


def validate_edge(src, src_port, tgt_node, tgt_port):
    """Validate a single edge for type matching."""
    src_port_str = f"{src}:{src_port}"
    tgt_port_str = f"{tgt_node}:{tgt_port}"

    try:
        src_type = lookup_port_type(src_port_str)
        tgt_type = lookup_port_type(tgt_port_str)
    except Exception as e:
        print(f"❌ Lookup failed for edge {src_port_str} → {tgt_port_str}: {e}")
        return False

    if src_type != tgt_type:
        print(
            f"⚠️ Type mismatch: {src_port_str} ({src_type}) → {tgt_port_str} ({tgt_type})"
        )
        return False

    print(f"✅ Edge valid: {src_port_str} → {tgt_port_str}")
    return True


def validate_graph(adj_list):
    """Validate all edges in the adjacency list."""
    load_yaml_definitions()

    all_valid = True

    for src, edges in adj_list.items():
        for tgt_node, src_port, tgt_port in edges:
            if not validate_edge(src, src_port, tgt_node, tgt_port):
                all_valid = False

    return all_valid
