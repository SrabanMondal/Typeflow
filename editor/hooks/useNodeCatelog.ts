// src/hooks/useNodeCatalog.ts
"use client";

import { ClassNodeDef, FunctionNodeDef, NodeCatalog } from "@/types/node";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import axios from "axios";

export type NodesApiRes={
  nodes: FunctionNodeDef[],
  classes: ClassNodeDef[],
}

export function useNodeCatalog() {
  const [catalog, setCatalog] = useState<NodeCatalog>({
    classes: [],
    functions: [],
    inputs: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await api.get<NodesApiRes>("/nodes");
        const data = res.data;
        console.log(res.data)
        
        const dummy: NodeCatalog = {
          inputs: [
            {
              entity: "X",
              name: "string_val",
              description: "Provide a string constant",
              valueType: "str",
              outputPorts: ["val"],
              value:""
            },
            {
              entity: "X",
              name: "num",
              description: "Provide a numeric constant",
              valueType: "int",
            outputPorts: ["val"],
            value:""
          },
          {
              entity: "X",
              name: "bool_val",
              description: "Provide a boolean constant",
              valueType: "bool",
            outputPorts: ["val"],
            value:""
          },
        ],
        functions: data.nodes,
        classes: data.classes,
      };
      
      setCatalog(dummy);
      setLoading(false);
      console.log(dummy);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.log(err.response?.status);
        console.log(err.response?.data);
        setLoading(false);
      }
    }
    }
    
    fetchData();
  }, []);

  return { ...catalog, loading };
}
