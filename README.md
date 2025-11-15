# Typeflow

<p align="center">
  <a href="https://pypi.org/project/typeflowapp/">
    <img src="https://img.shields.io/pypi/v/typeflowapp?color=4c1&label=PyPI&style=flat-square" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/typeflowapp/">
    <img src="https://img.shields.io/pypi/dm/typeflowapp?style=flat-square&color=blue" alt="PyPI downloads">
  </a>
  <a href="https://pypi.org/project/typeflowapp/">
    <img src="https://img.shields.io/pypi/pyversions/typeflowapp?style=flat-square" alt="Python versions">
  </a>
  <br>
  <a href="https://github.com/SrabanMondal/typeflow/blob/main/typeflow/LICENSE">
    <img src="https://img.shields.io/github/license/SrabanMondal/typeflow?style=flat-square&color=brightgreen" alt="GitHub license">
  </a>
  <a href="https://github.com/SrabanMondal/typeflow/issues">
    <img src="https://img.shields.io/github/issues/SrabanMondal/typeflow?style=flat-square" alt="GitHub issues">
  </a>
  <a href="https://github.com/SrabanMondal/typeflow/pulls">
    <img src="https://img.shields.io/github/issues-pr/SrabanMondal/typeflow?style=flat-square" alt="GitHub pull requests">
  </a>
  <a href="https://github.com/SrabanMondal/typeflow/stargazers">
    <img src="https://img.shields.io/github/stars/SrabanMondal/typeflow?style=flat-square&color=yellow" alt="GitHub stars">
  </a>
  <br>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000?style=flat-square" alt="Code style: black">
  </a>
  <a href="https://www.mkdocs.org/">
    <img src="https://img.shields.io/badge/docs-mkdocs-green?style=flat-square" alt="Docs: mkdocs">
  </a>
</p>


**Typeflow is a modern visual workflow engine for Python**, enabling developers to design, validate, and execute **fully type-safe workflows** using a clean **drag-and-drop editor**.

Typeflow brings together:

- A **Python-first workflow compiler**  
- A **React Flow–powered visual editor**  
- A **modular, deterministic execution engine**

This allows you to build **complex, reliable systems** using **Python functions**, **classes**, and **AI-assisted logic** — all represented **visually as nodes**.

This repository contains **both**:

1. The `typeflow` Python package  
2. The **Next.js-based visual editor** shipped with it  

For documentation, click on this link: **[Typeflow](https://srabanmondal.github.io/Typeflow/)**

---

## Features

### Visual Python Workflows

Design pipelines using a **friendly React Flow UI** — **fully offline, local, secure**.

### Type-Safe Node System

Every node input/output uses **Python type hints**, validated at **compile-time**.

### Function & Class Nodes

Use plain Python:

- `@node()` for **function nodes**  
- `@node_class` for **full object-oriented visual programming**

### Automatic Orchestrator Generation

Typeflow **compiles the DAG** → **generates Python code** → **executes deterministically**.

### Live Execution (SSE)

Watch every node execute in **real-time** inside the editor.

### AI Ready

Typeflow is built with **modular LLM integration** in mind — ideal for **agents**, **ETL/ML pipelines**, **decision graphs**, and **reasoning flows**.

---

## Repository Structure

```plain
root/
│
├── editor/                     # Next.js (React Flow) visual editor
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   └── public/
│
└── typeflow/                   # Python package
    ├── src/typeflow/
    │   ├── cli/               # Typer CLI commands (setup, create-node, validate…)
    │   ├── core/              # Compiler & script generator
    │   ├── sdk/               # Node + node_class decorators
    │   ├── server/            # FastAPI backend for editor
    │   └── utils/             # Internal utilities
    ├── tests/
    ├── pyproject.toml
    └── README.md
```

---

## Installation

Install Typeflow from PyPI:

```bash
pip install typeflowapp
```

Create a new Typeflow project:

```bash
typeflow setup my_app
cd my_app
source .venv/bin/activate    # macOS/Linux
# or
.\.venv\Scripts\activate     # Windows
```

Start the visual editor:

```bash
typeflow start-ui
```

---

## Development (For Contributors)

Clone this repo:

```bash
git clone https://github.com/<your-name>/typeflow.git
cd typeflow
```

### Developing the Python Package

```bash
cd typeflow
poetry install
```

Run CLI in dev mode:

```bash
poetry run typeflow --help
```

Run tests:

```bash
pytest
```

### Developing the Editor (Next.js)

```bash
cd editor
npm install
npm run dev
```

You should also have a **Typeflow backend** running from a project:

```bash
typeflow start-ui
```

The editor will **automatically connect** to the backend via its **FastAPI routes**.

---

## Core Concepts

| Concept | Description |
|--------|-------------|
| **Function Nodes** | Simple Python functions wrapped in `@node()` |
| **Class Nodes** | True visual OOP: instantiate objects, access fields, call methods, pass objects through graph |
| **DAG Compiler** | Reads `workflow.json` → validates & type-checks → generates Python executor |
| **Editor** | Drag nodes, connect edges, inspect values, run workflows live |
| **Pure Local Execution** | No cloud, no telemetry — fully offline and transparent |

---

## Documentation

Documentation is generated using **MkDocs**.

After cloning:

```bash
cd typeflow
poetry install
poetry run mkdocs serve
```

Docs include:

- Getting started  
- Function/class node guides  
- Workflow building  
- Editor usage  
- Advanced examples  
- Contribution standards  

---

## Examples

You can view this repository to see a real example of Ai agent created using typeflow framework, which you can install using typeflow and run it.

**[Skill AI](https://github.com/SrabanMondal/SkillAI)**

## Contributing

We welcome contributions for:

- Node system enhancements  
- Editor UI/UX improvements  
- New CLI commands  
- Compiler improvements  
- AI/LLM integrations  
- Tests & typing improvements  
- Workflow execution optimizations  

See:

- [`typeflow/CONTRIBUTING.md`](typeflow/docs/contributing.md)  
- [`editor/CONTRIBUTING.md`](editor/CONTRIBUTING.md)  

---

## License

Licensed under **GNU General Public License**.

See [`LICENSE`](LICENSE) for details.

---

## Acknowledgements

**Typeflow combines**:

- The **power & simplicity** of Python  
- The **clarity** of type-safe architecture  
- The **expressiveness** of visual programming  
- The **modularity** of AI-driven development  

Together forming a **new direction** for **AI-ready workflow systems**.

---
