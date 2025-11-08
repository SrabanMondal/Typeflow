// src/hooks/useNodeCatalog.ts
"use client";

import { ClassNodeDef, FunctionNodeDef, NodeCatalog } from "@/types/node";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import axios from "axios";
import { InputNodes } from "@/lib/inputs";
import { OutputNodes } from "@/lib/outputs";

export type NodesApiRes={
  nodes: FunctionNodeDef[],
  classes: ClassNodeDef[],
}

export function useNodeCatalog() {
  const [catalog, setCatalog] = useState<NodeCatalog>({
    classes: [],
    functions: [],
    inputs: [],
    outputs:[],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await api.get<NodesApiRes>("/nodes");
        const data = res.data;
        console.log(res.data)
        
        const dummy: NodeCatalog = {
          inputs: InputNodes,
        functions: data.nodes,
        classes: data.classes,
        outputs: OutputNodes,
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
