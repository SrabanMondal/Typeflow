// src/utils/workflowSerializer.ts
import { WorkflowNode } from "@/hooks/useWorkflowState";
import { SerializedWorkflow } from "@/types/workflow";
import { Edge } from "@xyflow/react";




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

