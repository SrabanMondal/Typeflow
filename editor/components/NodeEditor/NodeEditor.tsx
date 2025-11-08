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
import { getDag, saveWorkflow, startWorkflow } from "@/lib/workflow";
import { nodeStateStyles } from "@/lib/nodestyle";
import api from "@/lib/api";
import toast from "react-hot-toast";

function EditorInner() {
  const { screenToFlowPosition, setNodes } = useReactFlow();
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
  const [running, setRunning] = useState(false);

  const onSelectionChange = useCallback((selection: { nodes: WorkflowNode[]; edges: Edge[] }) => {
    setSelectedNodes(selection.nodes as WorkflowNode[]);
    setSelectedEdges(selection.edges);
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Delete") {
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

  const handleExport = async () => {
    const json = exportWorkflow("workflow");
    const save = await saveWorkflow(json);
    console.log(save.status);
  };

  const handleImportButton = async () => {
    const workflow = await getDag();
    if (workflow) {
      importWorkflow(workflow);
    } else {
      console.log("Workflow import failed");
    }
  };

  // 🔹 Add this: run workflow and listen to events
  const handleStart = async () => {

    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        style: nodeStateStyles.reset,
        data: { ...node.data, status: null },
      }))
    );
    setRunning(true);
    const json = exportWorkflow("workflow");
    const data = await startWorkflow(json);
    if (!data || !data.session_id){
      toast.error("Start failed"); return;
    }
    const { session_id } = data
    const eventSource = new EventSource(`http://localhost:3001/api/stream?session_id=${session_id}`);
    eventSource.onmessage = (event) => {
      console.log(event)
      const msg = JSON.parse(event.data);
      const { event: type, id, val } = msg;
      console.log("Event:", type, id);
     
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id !== id) return node;
              switch (type) {
                case "node_start":
                  return { ...node, data: { ...node.data, status: "start" }, style: nodeStateStyles.start };
                case "node_success":
                  return { ...node, data: { ...node.data, status: "success" }, style: nodeStateStyles.success };
                case "node_error":
                  return { ...node, data: { ...node.data, status: "error" }, style: nodeStateStyles.error };
                case "node_output":
                  return { ...node, data: { ...node.data, value: val } };
                default:
                  return node;
              }
        })
      );

      if (type == "workflow_complete") {
        eventSource.close();
        setRunning(false);
      }
      if (type == "workflow_error" || type=="node_error") {
        eventSource.close();
        setRunning(false);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE Error", err);
      eventSource.close();
      setRunning(false);
    };
  };

  return (
    <div className="editor relative flex-1 h-full">
      <div className="absolute top-4 right-4 flex gap-3 z-50">
        <button
          onClick={handleExport}
          className="px-4 py-2 bg-linear-to-r from-indigo-500 to-purple-500 text-white font-medium rounded-lg shadow-md hover:scale-105 transition-transform"
        >
          Export
        </button>
        <button
          onClick={handleImportButton}
          className="px-4 py-2 bg-linear-to-r from-emerald-500 to-teal-500 text-white font-medium rounded-lg shadow-md hover:scale-105 transition-transform"
        >
          Import
        </button>
        <button
          onClick={handleStart}
          disabled={running}
          className={`px-4 py-2 font-medium rounded-lg shadow-md transition-transform ${
            running
              ? "bg-gray-400 text-white"
              : "bg-linear-to-r from-pink-500 to-red-500 text-white hover:scale-105"
          }`}
        >
          {running ? "Running..." : "Start"}
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
