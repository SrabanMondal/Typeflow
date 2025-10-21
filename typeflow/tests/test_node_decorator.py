import yaml
import os
import tempfile
from pathlib import Path
from typeflow.sdk.node import node

def test_node_decorator_creates_yaml(tmp_path):
    # Setup temporary .typeflow directory
    typeflow_dir = tmp_path / ".typeflow" / "nodes"
    typeflow_dir.mkdir(parents=True)

    # Temporarily change cwd
    cwd = os.getcwd()
    os.chdir(tmp_path)

    @node()
    def add(a: int, b: int) -> int:
        """Add two integers."""
        return a + b

    # Check if YAML created
    yaml_file = typeflow_dir / "add.yaml"
    assert yaml_file.exists()

    # Validate YAML structure
    data = yaml.safe_load(open(yaml_file))
    assert data["name"] == "add"
    assert data["inputs"] == {"a": "int", "b": "int"}
    assert data["output"] == "int"
    assert "Add two integers" in data["description"]

    os.chdir(cwd)
