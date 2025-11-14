import api from "./api";
import { SerializedWorkflow } from "@/types/workflow";
import { toast } from "react-hot-toast";
import { updateCountersFromDag } from "./idGenerator";

export async function getDag(): Promise<SerializedWorkflow | null> {
  try {
    const { data } = await api.get<SerializedWorkflow>("/dag");
    toast.success("Workflow loaded successfully ✅");
    updateCountersFromDag(data);
    return data;
  } catch (error) {
    console.error(error);
    toast.error(
      "Workflow json not found in ur local dir"
    );
    return null;
  }
}

export async function saveWorkflow(
  workflow: SerializedWorkflow
): Promise<{ status: string }> {
  try {
    const { data } = await api.post<{ status: string }>("/save", workflow);
    toast.success("Workflow saved successfully 💾");
    return data;
  } catch (error) {
    console.error(error);
    toast.error("Failed to save workflow");
    return { status: "error" };
  }
}

export async function startWorkflow(workflow:SerializedWorkflow) {
    try {
      const res = await api.post("/start", workflow );
      return res.data
    } catch (error) {
       console.error(error)
       return null;
    }
}