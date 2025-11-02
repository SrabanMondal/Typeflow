import json
from pathlib import Path

from typeflow.server.utils.class_json import load_all_class_manifests
from typeflow.server.utils.node_json import load_all_node_manifests

WORKFLOW_DIR = Path("workflow")

# def load_manifest():
#     f = WORKFLOW_DIR / "manifest.yaml"
#     return yaml.safe_load(f.read_text()) if f.exists() else {}


def load_dag():
    f = WORKFLOW_DIR / "dag.json"
    return json.loads(f.read_text()) if f.exists() else {}


def load_nodes_classes() -> dict:
    NODES_DIR = Path(".typeflow/nodes")
    CLASS_DIR = Path(".typeflow/classes")
    nodes = load_all_node_manifests(NODES_DIR)
    classes = load_all_class_manifests(CLASS_DIR)
    return {"nodes": nodes, "classes": classes}
