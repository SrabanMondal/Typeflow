"use client";
import React, { useState } from "react";
import { useNodeCatalog } from "@/hooks/useNodeCatelog";
import { motion, AnimatePresence } from "framer-motion";
import { Box, Cpu, Database } from "lucide-react";


export default function Sidebar() {
  const { inputs, functions, classes, loading } = useNodeCatalog();
  const [activeTab, setActiveTab] = useState<"inputs" | "functions" | "classes">("inputs");

  const onDragStart = (event: React.DragEvent, nodeData: any) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(nodeData));
    event.dataTransfer.effectAllowed = "move";
    const preview = document.createElement("div");
preview.textContent = nodeData.name;
preview.style.cssText = `
  padding: 6px 10px;
  border-radius: 6px;
  background: #1e293b;
  color: #10b981;
  font-size: 12px;
  font-weight: 600;
  width: 100px;
`;
document.body.appendChild(preview);
event.dataTransfer.setDragImage(preview, 0, 0);
setTimeout(() => preview.remove(), 0);

  };

  const tabs = [
    { id: "inputs", label: "Inputs", icon: <Database /> },
    { id: "functions", label: "Functions", icon: <Cpu /> },
    { id: "classes", label: "Classes", icon: <Box /> },
  ];

  const getTabData = () => {
    switch (activeTab) {
      case "inputs":
        return inputs;
      case "functions":
        return functions;
      case "classes":
        return classes;
      default:
        return [];
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center w-64 h-full bg-slate-900 text-gray-300">
        Loading...
      </div>
    );
  }

  return (
    <div className="sidebar w-80 h-full bg-slate-900/80 backdrop-blur-md border-r border-slate-800 text-white flex flex-col">
      {/* Tabs Header */}
      <div className="flex justify-between border-b border-slate-800">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors duration-200 ${
              activeTab === tab.id
                ? "bg-slate-800 text-emerald-400 border-b-2 border-emerald-400"
                : "text-gray-400 hover:text-white"
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="grid gap-2"
          >
            {getTabData().length > 0 ? (
              getTabData().map((node) => (
                <div
                  key={node.name}
                  draggable
                  onDragStart={(e) => onDragStart(e, node)}
                  className="p-3 bg-slate-800/70 hover:bg-slate-700/80 border border-slate-700 rounded-lg cursor-grab active:cursor-grabbing select-none transition-all duration-150 shadow-sm hover:shadow-md"
                >
                  <div className="text-sm font-medium">{node.name}</div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center text-sm py-10">No items found</p>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
