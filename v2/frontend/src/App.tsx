import { useState } from "react";
import type { ModelType } from "./types/models";
import { useTraining } from "./hooks/useTraining";
import { validateFile } from "./api/pythonApi";
import FileUpload from "./components/FileUpload";
import ModelSelector from "./components/ModelSelector";
import ResultsTabs from "./components/ResultsTabs";
import LoadingOverlay from "./components/LoadingOverlay";
import ErrorAlert from "./components/ErrorAlert";
import ExampleDownload from "./components/ExampleDownload";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const { loading, error, pythonResults, rResults, train } = useTraining();

  const handleFileAccepted = async (f: File) => {
    setFile(null);
    setValidationError(null);
    try {
      const res = await validateFile(f);
      if (!res.valid) {
        setValidationError(res.errors.join("; "));
        return;
      }
      setFile(f);
    } catch {
      setValidationError("Could not validate file. Is the Python backend running?");
    }
  };

  const handleTrain = (modelTypes: ModelType[]) => {
    if (!file) return;
    train(file, modelTypes);
  };

  const hasResults = pythonResults !== null || rResults !== null;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        IRT Student Models Dashboard
      </h1>

      <FileUpload onFileAccepted={handleFileAccepted} />

      {validationError && <ErrorAlert message={validationError} />}

      <ExampleDownload />

      {file && (
        <ModelSelector onTrain={handleTrain} disabled={loading} />
      )}

      {loading && <LoadingOverlay />}
      {error && <ErrorAlert message={error} />}

      {hasResults && (
        <ResultsTabs pythonResults={pythonResults} rResults={rResults} />
      )}
    </div>
  );
}
