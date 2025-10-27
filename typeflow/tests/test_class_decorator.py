import yaml
import os
from pathlib import Path
from typeflow import node_class
import pytest
import json

def test_node_class_creates_yaml(tmp_path):
    # Setup temporary .typeflow/class directory
    class_dir = tmp_path / ".typeflow" / "class"
    class_dir.mkdir(parents=True, exist_ok=True)

    # Save current cwd and switch to tmp_path
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        @node_class
        class MyNode:
            """Example node"""
            x: int
            y: float

            def compute(self, a: int, b: int) -> float:
                """Compute sum"""
                return a + b + self.y

        # YAML file path
        yaml_file = class_dir / "MyNode.yaml"
        assert yaml_file.exists(), "YAML file was not created"

        # Load YAML and validate contents
        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        # Basic metadata
        assert data["name"] == "MyNode"
        assert data["entity"] == "class"
        assert data["description"] == "Example node"

        # Fields
        assert "x" in data["fields"]
        assert "y" in data["fields"]
        assert data["fields"]["x"]["type"] == "int"
        assert data["fields"]["y"]["type"] == "float"

        # Methods
        assert "compute" in data["methods"]
        method_data = data["methods"]["compute"]
        assert method_data["returns"] == "float"
        assert method_data["input"] == {"a": "int", "b": "int"}
        assert method_data["description"] == "Compute sum"
        assert method_data["is_static"] is False

    finally:
        # Restore original cwd
        os.chdir(cwd)

def test_node_class_non_class():
    with pytest.raises(TypeError):
        @node_class
        def not_a_class(): pass

def test_node_class_invalid_field(tmp_path, monkeypatch):
    # Patch get_project_root to tmp_path
    import typeflow.utils
    monkeypatch.setattr(typeflow.utils, "get_project_root", lambda: tmp_path)

    from typeflow.sdk.nodeclass import node_class

    with pytest.raises(Exception):
        class NoNodeClass:
            x:int
        @node_class
        class BadNode:
            x: NoNodeClass

