import { rClient } from "./client";
import type { RTrainResponse } from "../types/models";

export async function trainRModel(
  file: File,
  modelType: string
): Promise<RTrainResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("model_type", modelType);
  const { data } = await rClient.post<RTrainResponse>("/train", form);
  return data;
}
