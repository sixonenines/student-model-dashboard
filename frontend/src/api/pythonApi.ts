import { pythonClient } from "./client";
import type { PythonTrainResponse, ValidateResponse } from "../types/models";

export async function validateFile(file: File): Promise<ValidateResponse> {
  const form = new FormData();
  form.append("file", file);
  const { data } = await pythonClient.post<ValidateResponse>("/validate", form);
  return data;
}

export async function trainPythonModels(
  file: File,
  modelTypes: string[]
): Promise<PythonTrainResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("model_types", JSON.stringify(modelTypes));
  const { data } = await pythonClient.post<PythonTrainResponse>("/train", form);
  return data;
}
