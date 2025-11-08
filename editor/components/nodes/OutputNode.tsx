"use client";
import React from "react";
import { Handle, Position } from "@xyflow/react";
import { OutputNodeDef } from "@/types/node";
import Image from "next/image";

interface OutputNodeProps {
  id: string;
  data: OutputNodeDef;
}

export function OutputNode({ id, data }: OutputNodeProps) {
  const { name, description, outputType, value } = data;

  // Parse helpers
  const tryParseJSON = (val: string) => {
    try {
      return JSON.parse(val);
    } catch {
      return null;
    }
  };

  // Renderer by type
  const renderContent = () => {
    if (!value || value.trim() === "") {
      return (
        <div className="text-gray-400 italic text-sm p-2">
          Waiting for output...
        </div>
      );
    }

    switch (outputType) {
      case "text":
        return (
          <pre className="text-xs bg-gray-50 rounded-md p-2 overflow-auto max-h-40 whitespace-pre-wrap">
            {value}
          </pre>
        );

      case "json": {
        const parsed = tryParseJSON(value);
        return parsed ? (
          <pre className="text-xs bg-gray-50 rounded-md p-2 overflow-auto max-h-40">
            {JSON.stringify(parsed, null, 2)}
          </pre>
        ) : (
          <div className="text-red-500 p-2">Invalid JSON</div>
        );
      }

      case "image": {
        const src = "http://localhost:3001" + value;
        console.log(src)
        return (
          <img
            src={`${src}`}
            alt="Output"
            className="rounded-md max-h-40 mx-auto"
          />
        );
      }

      case "table": {
        const rows = tryParseJSON(value);
        if (!Array.isArray(rows) || rows.length === 0) {
          return <div className="text-red-500 p-2">Invalid or empty table</div>;
        }

        const columns = Object.keys(rows[0]);
        return (
          <div className="overflow-auto max-h-48">
            <table className="text-xs border-collapse border border-gray-300 w-full">
              <thead>
                <tr className="bg-gray-100">
                  {columns.map((col) => (
                    <th key={col} className="border border-gray-300 p-1">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => (
                  <tr key={i}>
                    {columns.map((col) => (
                      <td key={col} className="border border-gray-300 p-1">
                        {String(row[col])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      }

      default:
        return (
          <div className="text-red-500 p-2">Unsupported output type</div>
        );
    }
  };

  return (
    <div className="rounded-2xl border border-gray-300 bg-white shadow-sm p-3 min-w-[200px]">
      <div className="font-medium text-sm mb-1">{name}</div>
      <div className="text-xs text-gray-500 mb-2">{description}</div>
      <Handle type="target" position={Position.Left} id="input" />

      {/* Main Render Area */}
      {renderContent()}
    </div>
  );
}
