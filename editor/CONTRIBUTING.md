# Contributing to the Typeflow Editor

Thank you for your interest in contributing to the **Typeflow Editor** — the **visual workflow builder** for the **Typeflow framework**.  
This guide explains how the editor works internally, how to set up your development environment, and how to contribute safely and effectively.

---

## Overview

The **Typeflow Editor** is a **Next.js + React Flow** application that provides a **drag-and-drop interface** for building **Typeflow DAGs**.  
It is bundled with the **Typeflow Python package** and communicates with the backend via a small set of **FastAPI endpoints**.

The editor is intentionally built to be:

- Modular  
- Hook-driven  
- React-idiomatic  
- Cleanly separated between UI & logic  
- Friendly for external contributors  

---

## 1. Project Structure

```
editor/
  app/                 # Next.js App Router pages & server components
  components/
      NodeEditor/      # Wrapper around ReactFlow instance
      nodes/           # Custom Node components: X, F, C, M, O
      ui/              # Shadcn UI components & wrappers
  hooks/
      useNodeCatalogue.ts
      useWorkflowState.ts
      useUpdateNode.ts
      useSubnodeManager.ts
  lib/
      api.ts           # Light API client (fetch helpers)
      utils.ts         # Pure helpers and utilities
      ...
  types/               # Type definitions for Nodes, Edges, DAG schema, Events
  public/              # Static assets and icons
```

**Notes for contributors**:

- The codebase is **intentionally lean** and **convention-driven**  
- Files under `lib/` follow **clear naming conventions**  
- **No global state managers** (e.g., Zustand) — logic is **fully hook-based**  
- Styling uses **Tailwind + Shadcn UI**  
- No custom `styles/` folder exists  

---

## 2. Core Editor Logic (Important for Contributors)

### `useNodeCatalogue`

- Fetches all nodes from backend `/nodes`  
- Normalizes them into a format suitable for the **sidebar**  
- Adds **built-in editor nodes** (X input nodes, output nodes)  
- Controls **sidebar rendering**

### `useWorkflowState`

Manages the **entire visual workflow state**:

- Node creation  
- Node deletion  
- Edge creation/removal  
- Importing DAG JSON  
- Exporting DAG JSON  
- Canvas reset  

This hook wraps **ReactFlow’s internal state** using its Provider.  
The editor does **not maintain its own global provider** yet.

### `useUpdateNode`

Handles **mid-graph node updates**, such as:

- Editing input node values  
- Updating metadata  
- Syncing node data with ReactFlow internals  

Ensures ReactFlow receives updates in an **immutable and stable** way.

### `useSubnodeManager`

Manages **method nodes** for class nodes:

- **Double-clicking** a class node shows a **floating vertical toolbar** under the node  
- Clicking a method in this mini-toolbar **inserts a “method node”** (`M` node type)  
- **Automatically connects** `class.self` → `method.self`  
- This distinction (`C` vs `M`) exists **only in the UI**; backend sees both as class nodes  

---

## 3. Backend API (FastAPI)

The editor interacts with a **minimal backend API set**:

| Method | Endpoint | Purpose |
|-------|----------|--------|
| `GET` | `/nodes` | Returns all validated Typeflow function and class nodes |
| `POST` | `/start` | Starts workflow execution: converts DAG → script, spawns subprocess, creates `session_id` |
| `GET` | `/stream?session_id=...` | SSE endpoint for: `node_started`, `node_finished`, `error`, `logs`, `workflow_complete` |
| `GET` | `/dag` | Load existing DAG if present |
| `POST` | `/save` | Save workflow (`workflow.yaml` and metadata) |
| `POST` | `/upload_file` | Upload files for input node values |

> **Contributors do not need the full Typeflow backend running** — you can **mock these endpoints** during development.

---

## 4. Development Environment

### Prerequisites

- **Node.js 20+**  
- **npm** (used for this project)  
- A running **Typeflow backend**  
  *(start via `typeflow start-ui` from a Typeflow project)*

### Install dependencies

```bash
npm install
```

### Start development server

```bash
npm run dev
```

### Backend for live testing

From a **Typeflow project folder**:

```bash
typeflow start-ui
```

This runs:

- **FastAPI backend**  
- **Next.js editor** on the correct ports automatically  

---

## 5. Coding Standards

We follow **clean and predictable patterns**:

| Rule | Requirement |
|------|-------------|
| **TypeScript everywhere** | Strict mode ON |
| **React functional components** | No class components |
| **Hooks-driven architecture** | All business logic in `/hooks` |
| **Presentational components stay dumb** | No logic in UI components |
| **Use Shadcn UI & Tailwind** | For consistency |
| **Use ReactFlow provider correctly** | Never mutate nodes/edges directly — use updater functions |
| **Modularize logic** | Move complex logic to `/hooks` or `/lib` |
| **Keep nodes consistent** | Custom nodes in `/components/nodes` — named: `XNode`, `FNode`, `CNode`, `MNode`, `ONode` |
| **No unused dependencies** | Editor is intentionally lean |

---

## 6. Contribution Areas

You can contribute to:

### I/O Nodes

- Adding support of more Input nodes and file specific type validation
- Adding support of more Output nodes like markdown/audio for various workflows.

### UI/UX Enhancements

- New sidebar layout  
- Improved drag/drop logic  
- Node inspector improvements  
- Zoom/pan/selection UX  
- Better output rendering  

### Graph Engine Improvements

- Node validation hints  
- Real-time type mismatch warnings  
- Auto-align & auto-layouter  
- Minimap, background grid enhancements  

### Backend Integration

- Better SSE handling  
- Error display  
- File upload improvements  

### Code Quality

- Refactoring hooks  
- Writing utility functions  
- Improving TypeScript typings  

### Architecture Upgrades

- Creating a dedicated `WorkflowProvider`  
- Creating a custom `NodeRegistry` system  
- Extending class-method subnode logic  

---

## 7. How to Contribute

1. **Fork** the repository  
2. Create a new branch:

   ```bash
   git checkout -b feature/my-change
   ```

3. **Make your changes** — follow coding standards & file layout  
4. Run lint (if configured):

   ```bash
   npm run lint
   ```

5. **Commit** with a clear message — use **conventional commits** if possible:

   ```text
   feat: add new inspector panel
   fix: correct method node rendering bug
   refactor: move edge creation logic to hook
   ```

6. **Submit a Pull Request** including:

   - What you changed  
   - Why  
   - Screenshots (if UI)  
   - Testing steps  

A maintainer will review it.

---

## 8. Thank You

Your contributions help make **Typeflow** a **powerful, intuitive, visual programming environment** for **Python & AI workflows**.  
We deeply appreciate **every PR and issue opened**.

If you have **ideas, improvements, or need help** — feel free to **open a discussion**.

---
