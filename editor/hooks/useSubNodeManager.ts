import { MethodDef } from "@/types/node";
import { useReactFlow } from "@xyflow/react";
import { WorkflowNode } from "./useWorkflowState";
import { generateId } from "@/lib/idGenerator";

export function useSubNodeManager(classNodeId: string) {
  const { getNode, addNodes, addEdges } = useReactFlow();

  const classNode = getNode(classNodeId);
  if (!classNode) throw new Error(`Class node ${classNodeId} not found`);

  const addMethodNode = (method: MethodDef) => {
    const className = classNode.id.split(":");
    const methodName = className[1]+":"+method.name
    const methodNodeData: MethodDef = {
      entity: "C",
      name: methodName,
      inputPorts: method.inputPorts,
      outputPorts: method.outputPorts,
      description: method.description,
    };
    const methodNode: WorkflowNode = {
      id: `${methodNodeData.entity}:${methodNodeData.name}@${generateId(methodNodeData.entity)}`,
      type: "M",
      position:  {
      x: classNode.position.x + 250,
      y: classNode.position.y + 80,
    },
    data: methodNodeData
    }

    addNodes(methodNode);

     addEdges({
      id: `edge-${classNode.id}-${methodNode.id}`,
      source: classNode.id,
      sourceHandle: `self`,
      target: methodNode.id,
      targetHandle: `self`,
      type: "default",
      animated: true, // optional
    });
  };

  return { addMethodNode };
}
