// src/utils/workflowSerializer.ts
import { WorkflowNode } from "@/hooks/useWorkflowState";
import { SerializedWorkflow } from "@/types/workflow";
import { Edge } from "@xyflow/react";


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

