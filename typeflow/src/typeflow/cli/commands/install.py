import subprocess
import yaml
from pathlib import Path
import sys

def run_cmd(cmd: list[str]):
    """Run a subprocess and stream output live."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Command failed: {' '.join(cmd)}", file=sys.stderr)

def install():
    root = Path(".")
    typeflow_dir = root / ".typeflow"
    workflow_file = root / "workflow" / "workflow.yaml"

    if not typeflow_dir.exists():
        print("⚠️  .typeflow folder not found in root.")
        return
    if not workflow_file.exists():
        print("⚠️  workflow/workflow.yaml file not found.")
        return

    with open(workflow_file, "r") as f:
        config = yaml.safe_load(f)

    name = config.get("name", "Unnamed Workflow")
    print(f"🚀 Installing workflow: {name}")

    deps = config.get("dependencies", [])
    nodes = config.get("nodes", [])
    classes = config.get("classes", [])

    if deps:
        print("\n📦 Installing dependencies via uv...")
        for dep in deps:
            print(f"   → {dep}")
            run_cmd(["uv", "add", dep])
    else:
        print("\n📦 No dependencies listed.")

    if nodes:
        print("\n🧩 Validating nodes...")
        for node in nodes:
            print(f"   → {node}")
            run_cmd(["typeflow", "validate", "node", node])
    else:
        print("\n🧩 No nodes found in workflow.yaml.")

    if classes:
        print("\n🏗️  Validating classes...")
        for cls in classes:
            print(f"   → {cls}")
            run_cmd(["typeflow", "validate", "class", cls])
    else:
        print("\n🏗️  No classes found in workflow.yaml.")

    print("\n✅ Installation and validation completed successfully!")

