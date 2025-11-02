
import { SerializedWorkflow } from "@/types/workflow";
import React, { useRef } from "react";

interface FileModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImport: (json: SerializedWorkflow) => void;
}

export default function FileModal({ isOpen, onClose, onImport }: FileModalProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    try {
      const json = JSON.parse(text);
      onImport(json);
      onClose();
    } catch (err) {
      alert("Invalid JSON file!");
      console.error(err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-lg p-6 w-96 text-center border border-gray-200 dark:border-neutral-700">
        <h2 className="text-lg font-semibold mb-4">Import Workflow</h2>
        <input
          ref={fileInputRef}
          type="file"
          accept=".json"
          onChange={handleFileChange}
          className="mb-4 block w-full text-sm text-gray-700 dark:text-gray-300"
        />
        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 dark:bg-neutral-800 rounded hover:bg-gray-300 dark:hover:bg-neutral-700 transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
