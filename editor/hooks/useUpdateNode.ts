"use client";

import { useCallback } from "react";
import { useReactFlow, Node } from "@xyflow/react";
import type { InputNodeDef } from "@/types/node";

export function useUpdateXNode() {
  const { getNodes, setNodes } = useReactFlow();

  const updateXNodeData = useCallback(
    (id: string, updates: Partial<InputNodeDef>) => {
      const nodes = getNodes();
      const newNodes: Node[] = nodes.map((node) =>
        node.id === id && node.data.entity === "X"
          ? { ...node, data: { ...node.data, ...updates } }
          : node
      );
      setNodes(newNodes);
    },
    [getNodes, setNodes]
  );

  return {
    updateXNodeData,
  } as const;
}
