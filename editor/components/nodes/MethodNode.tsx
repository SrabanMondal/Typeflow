"use client";
import { Handle, Position } from "@xyflow/react";
import { MethodDef } from "@/types/node";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface MethodNodeProps {
  id: string;
  data: MethodDef;
}

export default function MethodNode({ id, data }: MethodNodeProps) {
  const { name, is_static, description, inputPorts = [], outputPorts = [] } = data;

  const cleaned = name.split(":");
  const className = cleaned[0].split("@")[0];
  const methodName = cleaned[1];

  // number of grid rows = max(inputPorts, outputPorts)
  const totalRows = Math.max(inputPorts.length, outputPorts.length);

  return (
    <TooltipProvider delayDuration={150}>
      <div
        className={`relative rounded-xl border bg-white shadow-sm hover:shadow-md transition-all w-56
          ${is_static ? "border-purple-300" : "border-emerald-300"}
        `}
      >
        {/* Header */}
        <div
          className={`text-sm font-semibold px-3 py-1 border-b truncate rounded-t-xl
            ${
              is_static
                ? "bg-purple-50 text-purple-700 border-purple-200"
                : "bg-emerald-50 text-emerald-700 border-emerald-200"
            }`}
        >
          🧩 {className}.{methodName}()
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
          {/* Input handles */}
          {inputPorts.map((port, i) => (
            <Tooltip key={`in-${port}`}>
              <TooltipTrigger asChild>
                <Handle
                  id={port}
                  type="target"
                  position={Position.Left}
                  className="absolute bg-blue-400! hover:bg-blue-600! w-2.5! h-2.5! transition-colors cursor-pointer"
                  style={{
                    top: `${i * 100 / totalRows}%`,
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

          {/* Output handles */}
          {outputPorts.map((port, i) => (
            <Tooltip key={`out-${port}`}>
              <TooltipTrigger asChild>
                <Handle
                  id={port}
                  type="source"
                  position={Position.Right}
                  className="absolute bg-green-400! hover:bg-green-600! w-2.5! h-2.5! transition-colors cursor-pointer"
                  style={{
                    top: `${i * 100 / totalRows}%`,
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
