"use client";
import React, { useCallback, useEffect, useState } from "react";
import {
  Background,
  Controls,
  useReactFlow,
  ReactFlow,
  ReactFlowProvider,
  Edge,
} from "@xyflow/react";
import nodeTypes from "@/components/nodes";
import { useWorkflowState, WorkflowNode } from "@/hooks/useWorkflowState";
import FileModal from "./utils/FileModal";

function EditorInner() {
  const { screenToFlowPosition } = useReactFlow();
  const {
    addNode,
    nodes,
    edges,
    onEdgesChange,
    onNodesChange,
    addConnection,
    removeNode,
    removeEdge,
    exportWorkflow,
    importWorkflow,
  } = useWorkflowState();

  const [selectedNodes, setSelectedNodes] = useState<WorkflowNode[]>([]);
  const [selectedEdges, setSelectedEdges] = useState<Edge[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const onSelectionChange = useCallback((selection: { nodes: WorkflowNode[]; edges: Edge[] }) => {
    setSelectedNodes(selection.nodes as WorkflowNode[]);
    setSelectedEdges(selection.edges);
  }, []);

  // DELETE key handler
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Delete" || event.key === "Backspace") {
        selectedNodes.forEach((n) => removeNode(n.id));
        selectedEdges.forEach((e) => removeEdge(e.id));
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [selectedNodes, selectedEdges, removeNode, removeEdge]);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const data = event.dataTransfer.getData("application/reactflow");
      if (!data) return;

      const parsed = JSON.parse(data);
      const position = screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      addNode(parsed, position);
    },
    [screenToFlowPosition, addNode]
  );

  const onDragOver = (event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };

  // 🔹 Export handler
  const handleExport = useCallback(() => {
    const json = exportWorkflow("workflow");
    console.log("Exported workflow:", json);

    // download as file
    const blob = new Blob([JSON.stringify(json, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "workflow.json";
    a.click();
    URL.revokeObjectURL(url);
  }, [exportWorkflow]);

  // 🔹 Import handler
  const handleImport = useCallback(
    (data: any) => {
      importWorkflow(data);
    },
    [importWorkflow]
  );

  return (
    <div className="editor relative flex-1 h-full">
      {/* Overlay buttons */}
      <div className="absolute top-4 right-4 flex gap-3 z-50">
        <button
          onClick={handleExport}
          className="px-4 py-2 bg-linear-to-r from-indigo-500 to-purple-500 text-white font-medium rounded-lg shadow-md hover:scale-105 transition-transform"
        >
          Export
        </button>
        <button
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2 bg-linear-to-r from-emerald-500 to-teal-500 text-white font-medium rounded-lg shadow-md hover:scale-105 transition-transform"
        >
          Import
        </button>
      </div>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        onConnect={addConnection}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onSelectionChange={onSelectionChange}
        onDrop={onDrop}
        onDragOver={onDragOver}
        nodeTypes={nodeTypes}
      >
        <Background />
        <Controls />
      </ReactFlow>

      <FileModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onImport={handleImport}
      />
    </div>
  );
}

export default function Editor() {
  return (
    <ReactFlowProvider>
      <EditorInner />
    </ReactFlowProvider>
  );
}
