# 🎨 TypeFlow Editor (UI)

**Visual Workflow Builder for TypeFlow**

TypeFlow Editor is a **React Flow–powered visual DAG builder**, built with **Next.js**, that connects to the **TypeFlow backend (FastAPI)** to visualize, create, and manage **type-safe Python workflows**.

It provides an **intuitive, drag-and-drop interface** to:

- Browse available function/class nodes (from YAML manifests)  
- Drag & drop nodes into the canvas  
- Connect ports **with type safety**  
- Export DAGs as JSON  
- Save and load workflows via REST API  

---

## 🧩 Overview

| Component | Role |
|---------|------|
| 🎨 **React Flow Canvas** | Interactive visual DAG editor |
| 🧠 **Node Inspector Panel** | Displays metadata, inputs/outputs, and type hints |
| 🗂 **Node Library Sidebar** | Loads available nodes from backend `/api` |
| 📡 **API Integration** | Communicates with FastAPI for import/save |
| 💾 **Persistent Storage** | Saves DAGs into `workflow/dag.json` |
| ⚙️ **Build Integration** | Exported as static site for `typeflow start ui` |

---

## 🧰 Tech Stack

- ⚛️ **Next.js 14** (App Router)  
- 🌀 **React Flow** – Interactive node-based graphs  
- 🎨 **Tailwind CSS + Shadcn/UI** – Beautiful, accessible components  
- 🔗 **Axios** – REST communication with FastAPI backend  

---

## 🚀 Getting Started

### 1. Start the TypeFlow backend
```bash
typeflow start ui
```
Launches FastAPI at [`http://localhost:3000`](http://localhost:3000)

> This serves both the **UI (static Next.js export)** and **API endpoints**

### 2. Open the Editor
Navigate to: [`http://localhost:3000`](http://localhost:3000)

---

## 🎯 Key Features

### **Node Library**
- Fetches all registered nodes from `/api`
- Shows name, description, input/output ports with **type annotations**

### **Drag & Drop Workflow Design**
- Pull nodes from sidebar → drop on canvas
- Auto-generated input/output handles based on type hints

### **Type-Safe Connections**
- Only allows edges between **compatible types**
- Visual feedback on invalid connections

### **DAG Persistence**
- Save workflow → `POST /api/save` → writes to `dag.json`
- Load on startup → `GET /api/dag`

---

## 💡 Future Roadmap

| Feature | Status |
|-------|--------|
| Type-aware edge validation (client-side preview) | Planned |
| Multi-workflow project support | Planned |
| Searchable & categorized node library | Planned |
| Auto-layout engine (Dagre) | Planned |
| Inline node code viewer | Planned |
| Realtime collaboration (WebSocket sync) | Planned |

---

## 🤝 Contributing

Contributions are **welcome** — the UI is modular and easy to extend!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

### Ideas to Contribute
- Add new custom node types
- Improve editor layout and UX
- Enhance DAG validation or animations
- Add keyboard shortcuts
- Implement undo/redo
- Support dark mode toggle

---

## 🧾 License

**MIT License** © 2025 TypeFlow

---

**TypeFlow Editor** — *Design workflows visually. Run them reliably.*  

Built for developers who believe **type safety shouldn’t end at code**.