"use client";
import { Handle, Position, NodeToolbar } from "@xyflow/react";
import { useState } from "react";
import { ClassNodeDef } from "@/types/node";
import { useSubNodeManager } from "@/hooks/useSubNodeManager";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export default function ClassNode({ id, data }: { id: string; data: ClassNodeDef }) {
  const [showToolbar, setShowToolbar] = useState(false);
  const { addMethodNode } = useSubNodeManager(id);

  const { name, description, inputPorts = [], outputPorts = [], methods = [] } = data;

  const totalRows = Math.max(inputPorts.length, outputPorts.length);

  return (
    <TooltipProvider delayDuration={150}>
      <div
        key={id}
        onDoubleClick={() => setShowToolbar((s) => !s)}
        className="relative rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-all w-56 cursor-pointer"
      >
        {/* Header */}
        <div className="text-sm font-semibold px-3 py-1 border-b border-gray-200 bg-purple-50 text-purple-700 truncate rounded-t-xl">
          🏛 {name}
        </div>

        {/* Description */}
        {description ? (
          <div className="px-3 py-2 text-[11px] text-gray-600 line-clamp-3">
            {description}
          </div>
        ) : (
          <div className="px-3 py-2 italic text-[11px] text-gray-400">
            No description
          </div>
        )}

        {/* Port Grid (EXACT same structure as FunctionNode) */}
        <div
          className="relative grid"
          style={{
            gridTemplateRows: `repeat(${totalRows}, minmax(16px, auto))`,
            marginBottom: "4px",
            paddingTop: "2px",
            paddingBottom: "4px",
          }}
        >
          {/* Input Handles */}
          {inputPorts.map((port, i) => (
            <Tooltip key={`in-${port}`}>
              <TooltipTrigger asChild>
                <Handle
                  id={`${port}`}
                  type="target"
                  position={Position.Left}
                  className="absolute bg-blue-400! hover:bg-blue-600! w-2.5 h-2.5 transition-all duration-150 cursor-pointer hover:ring-2 hover:ring-blue-300!"
                  style={{
                    top: `${((i + 0.5) * 100) / totalRows}%`,
                    transform: "translateY(-50%)",
                  }}
                />
              </TooltipTrigger>
              <TooltipContent
                side="right"
                className="text-xs px-2 py-1 bg-gray-800 text-white rounded"
              >
                <span className="font-semibold">{port}</span>
              </TooltipContent>
            </Tooltip>
          ))}

          {/* Output Handles */}
          {outputPorts.map((port, i) => (
            <Tooltip key={`out-${port}`}>
              <TooltipTrigger asChild>
                <Handle
                  id={`${port}`}
                  type="source"
                  position={Position.Right}
                  className="absolute bg-green-400! hover:bg-green-600! w-2.5 h-2.5 transition-all duration-150 cursor-pointer hover:ring-2 hover:ring-green-300!"
                  style={{
                    top: `${((i + 0.5) * 100) / totalRows}%`,
                    transform: "translateY(-50%)",
                  }}
                />
              </TooltipTrigger>
              <TooltipContent
                side="left"
                className="text-xs px-2 py-1 bg-gray-800 text-white rounded"
              >
                <span className="font-semibold">{port}</span>
              </TooltipContent>
            </Tooltip>
          ))}
        </div>

        {/* Toolbar (unchanged) */}
        {showToolbar && (
          <NodeToolbar isVisible position={Position.Bottom}>
            <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-2 min-w-[130px]">
              <div className="text-[11px] font-medium text-gray-500 px-1 pb-1 border-b mb-1">
                Available Methods
              </div>
              {methods.map((m) => (
                <button
                  key={m.name}
                  onClick={() => addMethodNode(m)}
                  className="flex items-center gap-1 text-sm text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded px-2 py-1 w-full text-left transition-colors"
                >
                  ➕ <span>{m.name}()</span>
                </button>
              ))}
            </div>
          </NodeToolbar>
        )}
      </div>
    </TooltipProvider>
  );
}
