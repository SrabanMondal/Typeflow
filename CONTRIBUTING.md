# Contributing to Typeflow

Thank you for your interest in contributing to **Typeflow** — a **visual programming engine** built for the next era of **AI-driven development**.

---

## Vision & Philosophy

Typeflow is more than a workflow builder — it’s a **bridge between traditional programming and visual, explainable, AI-assisted system design**.

### The long-term vision

- **Functions and classes** → become **abstract nodes**  
- **Nodes connect** → into **explainable DAGs**  
- **AI agents assist** → by writing nodes and composing systems  
- **Humans act as architects** → using **reusable, validated "black boxes"** to build **reliable "white box" systems**

> **Typeflow is shaping the core of AI-driven programming** — blending **static typing**, **visual orchestration**, and **runtime validation** into one cohesive language paradigm.

---

## Repository Structure

```text
typeflow/
│
├── editor/                    # Next.js + React Flow editor (UI)
│
└── typeflow/                  # Poetry-managed Python package
    ├── src/typeflow/
    │   ├── cli/               # Typer CLI (init, create-node, etc.)
    │   ├── core/              # Restricted: Orchestrator & script generator
    │   ├── sdk/               # @node and @node_class decorators
    │   ├── server/            # FastAPI backend serving UI & APIs
    │   └── utils/             # Shared utility functions
    └── tests/                 # pytest test suite
```

---

## Current Features

### CLI Commands

| Command | Description |
|--------|-------------|
| `typeflow setup` | Create a new project |
| `typeflow create-node` | Scaffold a node |
| `typeflow create-class` | Scaffold a class |
| `typeflow compile` | Compiles the DAG and validates types |
| `typeflow generate` | Generate orchestrator script |
| `typeflow validate` | Validate nodes/classes |
| `typeflow start-ui` | Start FastAPI + serve React Flow editor |
| `typeflow run` | Execute `src/orchestrator.py` |
| `typeflow install` | Installs all dependenies mentioned in `workflow.yaml` and Sets up typeflow env |
| `typeflow add` | Adds dependencies in typeflow |

### Core Systems

- **Node & Class decorators** with metadata extraction  
- **DAG compiler → orchestrator generator**  
- **Validation pipeline** with type checking  
- **FastAPI server** (static UI + live SSE updates)  
- **React Flow visual editor** (drag & drop, import/export, live run)

---

## Areas Open for Contribution

| Area | Description |
|------|-------------|
| **CLI (Typer)** | Improve modularity, add flags, enhance UX |
| **SDK (`node.py`, `nodeclass.py`)** | Extend decorator logic, improve validation |
| **Server (FastAPI)** | Improve UI-CLI communication, extend SSE |
| **Utils** | Add helper modules or improve existing ones |
| **Tests** | Add `pytest` coverage for CLI, SDK, core |
| **Editor (Next.js + React Flow)** | Enhance UX, add inspector panels, visual polish |
| **Documentation** | Improve or localize docs, write usage guides |
| **Core (Restricted)** | Compiler, generator, execution — **coordinate via issue first** |

---

## Local Setup Guide

### Requirements

- **Python 3.10+**  
- **Poetry** (for dependency & virtualenv management)  
- **Node.js + npm** *(only if working on editor)*

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/<your-username>/typeflow.git
cd typeflow

# Install dependencies
poetry install

# Activate Poetry virtual environment
poetry shell
```

#### Run CLI locally

```bash
poetry run typeflow --help
```

#### Test editor (optional)

```bash
cd editor
npm install
npm run dev
```

> The CLI automatically serves the **built static editor** when you run:
>
> ```bash
> typeflow start-ui
> ```

---

## Code Style & Testing Standards

We use:

| Tool | Purpose |
|------|--------|
| `ruff` | Linting & code consistency |
| `black` | Code formatting |
| `isort` | Import sorting |
| `mypy` | Type checking |
| `pytest` | Unit testing |

### Guidelines

- **Always** use **type hints** and **docstrings**  
- Run `ruff check .` and `black .` before commits  
- **Write or update** `pytest` tests for every PR  
- Keep commits **clean, descriptive, and scoped**  
- PRs must include **explanation, motivation, and test coverage**

---

## Compass Development Workflow

1. **Fork and clone** the repository  
2. Create a branch:

   ```bash
   git checkout -b feature/add-cli-help
   ```

3. Implement changes following style rules  
4. Run validation & tests:

   ```bash
   pytest
   mypy src/typeflow
   ```

5. Commit & push:

   ```bash
   git add .
   git commit -m "feat(cli): improved node validation output"
   git push origin feature/add-cli-help
   ```

6. **Submit a Pull Request** with:
   - Clear description  
   - Motivation  
   - Test coverage  

---

## Future Roadmap

| Feature | Status | Description |
|-------|--------|-----------|
| Node parameter control | Implemented | Real-time node parameter UI |
| Live execution updates | Implemented | SSE-based DAG runtime events |
| Public Node Registry | Planned | Community-managed reusable nodes |
| Community Server | Planned | Host, version, publish public nodes |
| Server-side Execution | Planned | Deploy and execute workflows remotely |
| Production-ready Deployment | Planned | Containerized runtime & orchestration APIs |
| Expanded Python Support | Planned | Deeper language integration & introspection |

---

## Testing and Evaluation

We encourage contributors to **test Typeflow** on real-world projects:

- ML pipelines  
- Data ETL  
- Image processing  
- Automation  

Your feedback helps improve **scalability, reliability, and ecosystem adaptability**.

**Open issues, raise PRs, or share experiments** demonstrating:

- Edge cases or scalability limits  
- Compatibility with `Pandas`, `Torch`, `FastAPI`, etc.  
- Real-world workflow use cases  

---

## 💖 Join the Community

We welcome:

- **Contributors** improving core or editor  
- **Testers** exploring limits  
- **Researchers** experimenting with **AI-assisted workflow generation**

> **Let’s build the future of visual programming — one node at a time.**

---
