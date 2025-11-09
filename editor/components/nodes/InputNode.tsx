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
  const [name, setName] = useState(data.name);

  const handleNameChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const newName = e.target.value;
      setName(newName);
      updateXNodeData(id, { name: newName });
    },
    [id, updateXNodeData]
  );
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

  const getHelpValue = (type: string):string=>{
        switch(type){
           case "str":
            return "Any text";
          case "int":
          case "number":
             return "Eg. 2,6,21."
          case "float":
            return "Eg. 2.5, 8.006.";
          case "bool":
            return "Eg. true, false"
          case "list":
          case "tuple":
          case "set":
            return "Eg. [1,2], [3,6,8]"
          case "dict":
            return 'Eg. {"val":67}'
          default:
            return ""
        }
  }

  return (
    <div
      className={`rounded-md border bg-white shadow-sm px-2 py-2 w-44 transition-colors
        ${isValid ? "border-green-400" : "border-red-400"}`}
    >
      <div className="mb-1">
        <input
          type="text"
          value={name}
          onChange={handleNameChange}
          className="w-full text-sm font-medium bg-gray-100 px-1 rounded-md text-green-600 outline-none border-b border-transparent focus:border-green-400"
        />
      </div>

      <div className="text-xs font-medium mb-1">{data.description}</div>


      <div className="text-xs text-gray-500">{data.valueType}</div>
      <div className="text-[10px] text-gray-800 font-medium mb-1">{getHelpValue(data.valueType)}</div>

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
