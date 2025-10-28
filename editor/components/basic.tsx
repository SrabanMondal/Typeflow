"use client"

import { useState, useCallback } from 'react';
import { ReactFlow, applyNodeChanges, applyEdgeChanges, addEdge, Background
    , Controls, MiniMap, useEdgesState, useNodesState, Connection, Edge, Node
 } from '@xyflow/react';

 
const initialNodes: Node[] = [
  {
    id: "1",
    type: "input",
    data: { label: "Input Node" },
    position: { x: 250, y: 5 },
  },
  {
    id: "2",
    data: { label: "Output Node" },
    position: { x: 100, y: 100 },
  },
];

const initialEdges: Edge[] = [{ id: "e1-2", source: "1", target: "2" }];
 
export default function NodeEditor() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
    );

    const exportWorkflow = () => {
    const workflow = { nodes, edges };
    console.log("Workflow JSON:", workflow);
    console.log("Stringified:", JSON.stringify(workflow, null, 2));
  };


  return (
    <div className="relative w-full h-screen bg-zinc-900">
      {/* Export Button */}
      <button
        onClick={exportWorkflow}
        className="absolute z-10 top-4 left-4 bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg shadow-md"
      >
        Export Workflow
      </button>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      >
        <Background />
        <MiniMap />
        <Controls />
      </ReactFlow>
    </div>
  );
}