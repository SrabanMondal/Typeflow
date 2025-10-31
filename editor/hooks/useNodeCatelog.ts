// src/hooks/useNodeCatalog.ts
"use client";

import { NodeCatalog } from "@/types/node";
import { useEffect, useState } from "react";
//import api from "@/lib/api";


export function useNodeCatalog() {
  const [catalog, setCatalog] = useState<NodeCatalog>({
    classes: [],
    functions: [],
    inputs: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      // --- Uncomment this when backend is ready ---
      // const { data, error } = await get<NodeCatalog>("/api/nodes");
      // if (data) setCatalog(data);

      // --- Dummy fallback data for now ---
      const dummy: NodeCatalog = {
        inputs: [
          {
            entity: "X",
            name: "value",
            description: "Provide a string constant",
            valueType: "string",
            outputPorts: ["val"],
            value:""
          },
          {
            entity: "X",
            name: "num",
            description: "Provide a numeric constant",
            valueType: "integer",
            outputPorts: ["val"],
            value:""
          },
        ],
        functions: [
          {
            entity: "F",
            name: "console",
            description: "Print message to console",
            inputPorts: ["message"],
            outputPorts: [],
          },
          {
            entity: "F",
            name: "uppercase",
            description: "Convert string to uppercase",
            inputPorts: ["text","a","b","c","d","e","f","g","h","i"],
            outputPorts: ["returns","a","b","c","d","e","f","g","h","i"],
          },
        ],
        classes: [
          {
            entity: "C",
            name: "TextCleaner",
            description: "Clean and normalize text",
            inputPorts: ["raw_text","self"],
            outputPorts: ["self","raw_text","a","b","c","d","e","f","g","h","i"],
            methods: [
              {
                entity:"C",
                name: "clean",
                inputPorts: ["self", "raw_text","a","b","c","d","e","f","g","h","i"],
                outputPorts: ["returns"],
                description: "Normalize whitespace in text",
              },
            ],
          },
        ],
      };

      setCatalog(dummy);
      setLoading(false);
    }

    fetchData();
  }, []);

  return { ...catalog, loading };
}
