"use client";
import { Handle, Position } from "@xyflow/react";
import { InputNodeDef } from "@/types/node";
import { useState, useCallback } from "react";
import { useWorkflowState } from "@/hooks/useWorkflowState";

interface InputNodeProps {
  id: string;
  data: InputNodeDef;
}

export default function InputNode({ id, data }: InputNodeProps) {
  const [value, setValue] = useState("");
  const [isValid, setIsValid] = useState(true);
  const { updateNodeData } = useWorkflowState();

  const checkValid = useCallback(
    (val: string): boolean => {
      try {
        switch (data.valueType) {
          case "string":
            return true;
          case "integer":
          case "number":
          case "float":
            return !isNaN(Number(val));
          case "boolean":
            return ["true", "false", "1", "0"].includes(val.toLowerCase());
          case "list":
          case "set": {
            const parsed = JSON.parse(val);
            return Array.isArray(parsed);
          }
          case "dict": {
            const parsed = JSON.parse(val);
            return typeof parsed === "object" && !Array.isArray(parsed);
          }
          default:
            return false;
        }
      } catch {
        return false;
      }
    },
    [data.valueType]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const newVal = e.target.value;
      setValue(newVal);

      const valid = checkValid(newVal);
      setIsValid(valid);

      updateNodeData(id, { value: newVal });
    },
    [id, updateNodeData, checkValid]
  );

  return (
    <div
      className={`rounded-md border bg-white shadow-sm px-2 py-2 w-44 transition-colors
        ${isValid ? "border-green-400" : "border-red-400"}`}
    >
      <div
        className="font-medium text-green-600 text-sm mb-1 truncate"
        title={data.description}
      >
        🧩 {data.name}
      </div>

      <div className="mb-1 text-xs text-gray-500">{data.valueType}</div>

      <input
        type="text"
        value={value}
        onChange={handleChange}
        className={`w-full border rounded px-1 text-sm focus:outline-none
          ${isValid ? "border-gray-300" : "border-red-300"}`}
      />

      <Handle
        id={`val`}
        type="source"
        position={Position.Right}
        style={{ top: "50%" }}
      />
    </div>
  );
}
