import api from "./api";

export async function uploadFileToBackend(file: File, nodeId: string): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("nodeId", nodeId);

  try {
    const res = await api.post("/upload_file", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    const { filePath } = res.data;
    return filePath;
  } catch (error) {
    console.error(error);
    throw new Error("File upload failed");
  }
}
