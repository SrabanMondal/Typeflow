# ⚙️ Installation

Typeflow is distributed as a single Python package that includes both the **CLI** and the **visual editor UI**.

---

## 🪄 Prerequisites

- Python 3.12+
- Git (optional)

---

## 🚀 Install

```bash
pip install typeflowapp
```

**This installs:**

- The Typeflow CLI

- The FastAPI backend

- The Next.js editor build (served statically)

- All internal dependencies

## 🧱 Project Setup

To scaffold a new project:

```bash
typeflow setup my_app
```

**This:**

- Creates a project folder named my_app

- Initializes a UV project and virtual environment

- Installs typeflow inside that venv

- Sets up the standard folder structure:

```plain
my_app/
├── .typeflow/
├── src/
│   ├── nodes/
│   ├── classes/
│   └── __init__.py
├── workflow/
│   ├── workflow.yaml
│   └── dag.json
├── pyproject.toml
├── .gitignore
└── README.md
```

## 🔁 Existing Projects

If you cloned a Typeflow project from GitHub:

```bash
python -m venv .venv
source .venv/bin/activate
pip install typeflowapp
typeflow install
```

**This will:**

- Install dependencies

- Ensure your environment is isolated

- Guide you to validate, compile, and run workflows

---
