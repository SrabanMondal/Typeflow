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