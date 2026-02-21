import { useState, useCallback } from "react";
import type { ModelType, ModelResult, TrainingState } from "../types/models";
import { trainPythonModels } from "../api/pythonApi";
import { trainRModel } from "../api/rApi";

export function useTraining() {
  const [state, setState] = useState<TrainingState>({
    loading: false,
    error: null,
    pythonResults: null,
    rResults: null,
  });

  const train = useCallback(
    async (file: File, modelTypes: ModelType[]) => {
      setState({ loading: true, error: null, pythonResults: null, rResults: null });

      try {
        // Fire Python + R requests concurrently
        const [pythonResponse, ...rResponses] = await Promise.all([
          trainPythonModels(file, modelTypes),
          ...modelTypes.map((mt) => trainRModel(file, mt)),
        ]);

        // Aggregate R results
        const rResults: Record<string, ModelResult> = {};
        modelTypes.forEach((mt, i) => {
          rResults[mt] = rResponses[i];
        });

        setState({
          loading: false,
          error: null,
          pythonResults: pythonResponse.models,
          rResults,
        });
      } catch (err: any) {
        const message =
          err?.response?.data?.detail ??
          err?.message ??
          "Training failed";
        setState((prev) => ({
          ...prev,
          loading: false,
          error: typeof message === "string" ? message : JSON.stringify(message),
        }));
      }
    },
    []
  );

  return { ...state, train };
}
