"use client";
import { Handle, Position } from "@xyflow/react";
import { InputNodeDef } from "@/types/node";
import { useState, useCallback } from "react";
import { useUpdateXNode } from "@/hooks/useUpdateNode";
import { uploadFileToBackend } from "@/lib/upload";
import toast from "react-hot-toast";

interface InputNodeProps {
  id: string;
  data: InputNodeDef;
}

export default function InputNode({ id, data }: InputNodeProps) {
  const [value, setValue] = useState(data.value);
  const [isValid, setIsValid] = useState(true);
  const { updateXNodeData } = useUpdateXNode();
  const checkValid = useCallback(
    (val: string): boolean => {
      try {
        switch (data.valueType) {
          case "str":
            return true;
          case "int":
          case "number":
          case "float":
            return !isNaN(Number(val));
          case "bool":
            return ["true", "false", "1", "0"].includes(val.toLowerCase());
          case "list":
          case "tuple":
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

      updateXNodeData(id, { value: newVal });
    },
    [id, updateXNodeData, checkValid]
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

       {data?.file ? (
      <input
        type="file"
       onChange={async (e) => {
          const file = e.target.files?.[0];
          if (!file) return;

          try {
            const filePath = await uploadFileToBackend(file, id);
            setValue(filePath);
            updateXNodeData(id, { value: filePath });
          } catch (err) {
            console.error(err);
            toast.error("File upload failed");
          }
        }}
        className="w-full text-sm"
      />
    ) : (
      <input
        type="text"
        value={value}
        onChange={handleChange}
        className={`w-full border rounded px-1 text-sm focus:outline-none
          ${isValid ? "border-gray-300" : "border-red-300"}`}
      />
    )}

      <Handle
        id={`val`}
        type="source"
        position={Position.Right}
        style={{ top: "50%" }}
      />
    </div>
  );
}
