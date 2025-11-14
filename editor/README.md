# Typeflow Visual Editor  

**A Visual Programming Interface for Building & Running Workflows**

The **Typeflow Editor** is a **Next.js + React Flow–powered visual builder** that lets you **design, edit, and execute** workflows created using the **Typeflow framework**.  
It provides a **drag-and-drop interface** for composing **function nodes**, **class nodes**, and **input/output nodes** into **executable DAGs**.

The editor is **packaged with the Typeflow CLI** and launches using a **single command**.

---

## Getting Started

### Start the Editor

From any Typeflow project root:

```bash
typeflow start-ui
```

This runs the **Next.js static UI** and the **FastAPI backend** together.

- **UI**: [http://localhost:3001](http://localhost:3001)  
- **Backend**: Automatically started (FastAPI)

You’ll see the **visual workflow canvas** open immediately in your browser.

---

## Editor Overview

The editor UI consists of **three main sections**:

### 1. Sidebar (Nodes Panel)

The left sidebar contains **all available node types**, organized into **four tabs**:

#### **Inputs**

Built-in input nodes such as:

- `string`  
- `int`  
- `float`  
- `bool`  
- `tuple`  
- `file input`

These allow you to **pass runtime values** when executing workflows.

#### **Functions**

All validated `@node()` function nodes in your project appear here.  
Dragging a function node onto the canvas creates a reusable step with:

- **Typed input ports**  
- A single `returns` output port  
- Description shown in **hover/inspector**

#### **Classes**

All `@node_class` definitions appear here.  
Dragging a class node onto the canvas creates an instance with:

- Input ports for each **field (typed)**  
- `self` input/output port  
- A **method selector** (see below)

#### **Outputs**

Built-in output nodes to **view results directly** in the editor:

- Text output  
- Image display  
- File output

---

### 2. Canvas (Main Workspace)

This is the **drag-and-drop area** where you **assemble workflows**.

**Supported interactions**:

- Drag nodes from the sidebar  
- Reposition freely  
- Connect **output → input** ports  
- Inspect node details on selection  
- Delete/reconnect edges  
- Zoom/pan on large workflows

**Connection Rules**:

- Ports must be **type-compatible**  
- Ports must match by **name**  
- The editor **prevents invalid edges**

Nodes update visually based on **execution status** (when running live).

---

### 3. Toolbar (Actions)

The top toolbar contains **three core actions**:

| Action | Description |
|-------|-------------|
| **Import** | Load an existing workflow (`dag.json`) into the editor. Useful for editing previously created workflows. |
| **Export** | Save the current graph to `dag.json` representing the DAG. Includes: node list, connections, positions, metadata. Can be committed or shared. |
| **Start** | Run the workflow **inside the editor**. Triggers: 1. Compile DAG, 2. Generate orchestrator, 3. Execute in background, 4. Stream live updates via SSE |

**Node statuses update in real-time**:

- **Running**  
- **Success**  
- **Error**

**Output nodes show**:

- Text results  
- Images  
- File downloads

---

## Class Nodes & Method Nodes

Class nodes represent Python classes decorated with `@node_class`.  
Each class appears as:

```
+----------------------+
|     MyClass          |
+----------------------+
| field1: str          |
| field2: int          |
| field3: tuple        |
+----------------------+
|   self (in/out)      |
+----------------------+
```

**To use a class method**:

1. **Double-click** the class node  
2. Sidebar shows **available methods**  
3. **Drag** the method node onto the canvas  
4. Connect `class.self` → `method.self`

This creates a node chain like:

```
[MyClass] → [MyClass.apply()]
```

The method behaves like a **function node** and can receive additional inputs.

---

## Backend Integration

The editor communicates with a **FastAPI backend** (started automatically).

**Backend responsibilities**:

- Validate DAG types  
- Compile adjacency lists  
- Generate orchestrator script  
- Execute workflow in **async subprocess**  
- Send **live streaming updates (SSE)**  
- Serve static editor build

**Important Endpoints**:

| Method | Endpoint |
|--------|----------|
| `POST` | `/api/compile` |
| `POST` | `/api/generate` |
| `POST` | `/api/run` |
| `GET`  | `/api/events` (SSE) |
| `GET`  | `/api/editor` (static UI) |

This tight integration enables **seamless edit → run → debug cycles**.

---

## Workflow File Format (`dag.json`)

Exported DAG JSON contains:

### `nodes[]`

Each node includes:

- `id` (`F:name@1`, `C:Class@2`, `M:Class@2:method`, `X:input@1`)  
- `type` (`F`, `C`, `M`, `X`)  
- `position` (`{x, y}`)  
- `data`:  
  - `name`  
  - `description`  
  - `inputPorts[]`  
  - `outputPorts[]`  
  - `class methods` (if class node)  
  - `status` (after run)

### `connections[]`

Each connection:

```json
{
  "source": "F:resize_image@2",
  "sourceHandle": "returns",
  "target": "F:grayscale@3",
  "targetHandle": "img"
}
```

## Live Execution in Editor

When running inside the editor:

**The backend**:

- Compiles graph  
- Validates types  
- Generates orchestrator  
- Runs Python sync flow  
- Streams events

**The editor**:

- Highlights **running nodes**  
- Marks **completed nodes**  
- Shows **errors inline**  
- Updates **output nodes**

**Example output node behaviors**:

- **Text** → show result instantly  
- **Image** → render preview  
- **File** → download button

This gives a **“visual debugging” experience** rarely found in workflow tools.

---

## Working With Class-Based AI Nodes

Nodes like `LLMEngine`, `SkillReasoner`, and `CareerPlanner` appear as **class nodes** with **typed fields**.

**Typical workflow inside editor**:

1. Drag `LLMEngine`  
2. Fill parameters:  
   - API key  
   - Model  
   - Temperature  
3. Connect to analysis nodes  
4. Build skill pipelines **visually**  
5. Start execution and observe reasoning  
6. Outputs appear **directly in viewer nodes**

This makes **complex AI agent workflows completely visual**.

---

## Summary

The **Typeflow Editor** transforms your Typeflow project into a **fully visual programming environment**:

- Drag-and-drop nodes  
- Configure parameters visually  
- Build DAGs interactively  
- Import/export workflows  
- Run with live updates  
- Debug visually  

It is the **front-end UI** that completes the **Typeflow ecosystem**, bridging **Python logic** with an **intuitive visual interface**.

---
