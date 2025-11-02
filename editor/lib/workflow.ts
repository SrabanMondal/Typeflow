import api from "./api";
import { SerializedWorkflow } from "./serializer";



export async function getDag(): Promise<SerializedWorkflow|null>{
  try {
    const { data } =  await api.get<SerializedWorkflow>("/dag");
    return data;
    
  } catch (error) {
    console.log(error);
    return null;
  }
}

export async function saveWorkflow(workflow: SerializedWorkflow): Promise<{ status: string }> {
  try {
    const { data } =  await api.post<{ status: string }>("/save", workflow);
    return data;
    
  } catch (error) {
     return {status: String(error)}
  }
}
