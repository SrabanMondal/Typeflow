// src/utils/workflowSerializer.ts
import { WorkflowNode, WorkflowNodeData } from "@/hooks/useWorkflowState";
import { Edge } from "@xyflow/react";

export interface SerializedWorkflow {
  id: string;
  name: string;
  version: string;
  nodes: {
    id: string;
    type: string;
    position: { x: number; y: number };
    data: WorkflowNodeData;
  }[];
  connections: {
    source: string;
    sourceHandle?: string;
    target: string;
    targetHandle?: string;
  }[];
}

export function serializeWorkflow(
  nodes: WorkflowNode[],
  edges: Edge[],
  name = "Untitled Workflow"
): SerializedWorkflow {
  return {
    id: `workflow-${Date.now()}`,
    name,
    version: "1.0",
    nodes: nodes.map((n) => ({
      id: n.id,
      type: n.type??"unknown",
      position: n.position,
      data: n.data,
    })),
    connections: edges.map((e) => ({
      source: e.source,
      sourceHandle: e.sourceHandle??"",
      target: e.target,
      targetHandle: e.targetHandle??"",
    })),
  };
}


export function deserializeWorkflow(payload: SerializedWorkflow): {
  nodes: WorkflowNode[];
  edges: Edge[];
}  {
  const nodes: WorkflowNode[] = payload.nodes.map((n) => ({
    id: n.id,
    type: n.type,
    position: n.position,
    data: n.data ,
  }));

  const edges: Edge[] = payload.connections.map((c, i) => ({
    id: `e-${c.source}-${c.target}-${i}`,
    source: c.source,
    sourceHandle: c.sourceHandle,
    target: c.target,
    targetHandle: c.targetHandle,
  }));

  return { nodes, edges };
}

