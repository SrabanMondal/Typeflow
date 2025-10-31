// src/hooks/useWorkflowState.ts
"use client";

import { useCallback } from "react";
import {
  Node,
  Edge as RFEdge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";
import { generateId } from "@/lib/idGenerator";
import type {
  ClassNodeDef,
  FunctionNodeDef,
  InputNodeDef,
  MethodDef,
} from "@/types/node";
import { deserializeWorkflow, SerializedWorkflow, serializeWorkflow } from "@/lib/serializer";

export type WorkflowNodeData = ClassNodeDef | FunctionNodeDef | InputNodeDef | MethodDef;


export type WorkflowNode = Node<WorkflowNodeData, string>;


export function useWorkflowState() {
  const [nodes, setNodes, onNodesChange] = useNodesState<WorkflowNode>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<RFEdge>([]);

  const addNode = useCallback(
    (nodeDef: WorkflowNodeData, position = { x: 0, y: 0 }) => {
      const id = `${nodeDef.entity}:${nodeDef.name}@${generateId(nodeDef.entity)}`;

      const newNode: WorkflowNode = {
        id,
        type: nodeDef.entity,
        position,
        data: nodeDef,
      };
      console.log("new node: ",newNode)
      setNodes((nds) => [...nds, newNode]);
      return newNode;
    },
    [setNodes]
  );

  // Remove a node by ID (and optionally remove connected edges)
  const removeNode = useCallback(
    (id: string) => {
      console.log("deleting")
      setNodes((nds) => nds.filter((n) => n.id !== id));
      setEdges((eds) => eds.filter((e) => e.source !== id && e.target !== id));
    },
    [setNodes, setEdges]
  );

  const updateNodeData = useCallback((id: string, updates: Partial<InputNodeDef>) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === id && node.data.entity=="X"? { ...node, data: { ...node.data, ...updates } } : node
      )
    );
  }, [setNodes]);

  const addConnection = useCallback(
    (conn: Connection) => {
      if (!conn.source || !conn.target) return;
      setEdges((eds) => addEdge(conn, eds));
    },
    [setEdges]
  );

  const removeEdge = useCallback(
  (idOrPredicate: string | ((e: RFEdge) => boolean)) => {
    setEdges((eds) =>
      typeof idOrPredicate === "string"
        ? eds.filter((e) => e.id !== idOrPredicate)
        : eds.filter((e) => !idOrPredicate(e))
    );
  },
  [setEdges]
);


  const resetWorkflow = useCallback(() => {
    setNodes([]);
    setEdges([]);
  }, [setNodes, setEdges]);

  const exportWorkflow = useCallback(
  (name?: string) => serializeWorkflow(nodes, edges, name),
  [nodes, edges]
);

const importWorkflow = useCallback(
  (payload: SerializedWorkflow | string) => {
    try {
      const parsed: SerializedWorkflow =
        typeof payload === "string" ? JSON.parse(payload) : payload;
      const { nodes: importedNodes, edges: importedEdges } =
        deserializeWorkflow(parsed);
      setNodes(importedNodes);
      setEdges(importedEdges);
    } catch (err) {
      console.error("Invalid workflow payload:", err);
    }
  },
  [setNodes, setEdges]
);

  return {
    // state
    nodes,
    edges,
    // reactflow handlers
    onNodesChange,
    onEdgesChange,
    // actions
    addNode,
    removeNode,
    updateNodeData,
    addConnection,
    removeEdge,
    resetWorkflow,
    exportWorkflow,
    importWorkflow,
  } as const;
}
