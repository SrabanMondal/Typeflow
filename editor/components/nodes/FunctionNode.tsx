"use client";
import { Handle, Position } from "@xyflow/react";
import { FunctionNodeDef } from "@/types/node";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface FunctionNodeProps {
  id: string;
  data: FunctionNodeDef;
  style?: React.CSSProperties;
}

export default function FunctionNode({ id, data, style}: FunctionNodeProps) {
  const { name, description, inputPorts = [], outputPorts = [] } = data;
  // total rows = max(inputs, outputs)
  const totalRows = Math.max(inputPorts.length, outputPorts.length);

  return (
    <TooltipProvider delayDuration={150}>
      <div
        key={id}
        style={style}
        className="relative rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-all w-56"
      >
        {/* Header */}
        <div className="text-sm font-semibold px-3 py-1 border-b border-gray-200 bg-blue-50 text-blue-700 truncate rounded-t-xl">
          ⚙️ {name}
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

        {/* Port Grid */}
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
                  className="absolute bg-blue-400! hover:bg-blue-600! w-2.5! h-2.5! transition-all duration-150 cursor-pointer hover:ring-2 hover:ring-blue-300!"
                  style={{
                    top: `${(i ) * (100 / totalRows)}%`,
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
                  className="absolute bg-green-400! hover:bg-green-600! w-2.5! h-2.5! transition-all duration-150 cursor-pointer hover:ring-2 hover:ring-green-300!"
                  style={{
                    top: `${(i ) * (100 / totalRows)}%`,
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
      </div>
    </TooltipProvider>
  );
}
