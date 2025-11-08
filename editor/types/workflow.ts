import { WorkflowNodeData } from "@/hooks/useWorkflowState";

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