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
import Instructions from "./components/Instructions";
import PrivacyPolicy from "./components/PrivacyPolicy";

export default function App() {
  const [page, setPage] = useState<"dashboard" | "privacy">("dashboard");
  const [file, setFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const { loading, error, pythonResults, rResults, train, reset } = useTraining();

  const handleFileAccepted = async (f: File) => {
    setFile(null);
    setValidationError(null);
    reset();
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

  if (page === "privacy") {
    return <PrivacyPolicy onBack={() => setPage("dashboard")} />;
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        IRT Student Models Dashboard
      </h1>

      <Instructions />

      <FileUpload onFileAccepted={handleFileAccepted} fileName={file?.name ?? null} />

      <p className="text-xs text-gray-400 -mt-3 mb-4 px-1">
        Your uploaded file is processed solely to train the selected models on
        our server and is automatically deleted after processing. No data is
        stored permanently or shared with third parties.{" "}
        <button
          onClick={() => setPage("privacy")}
          className="underline hover:text-gray-600"
        >
          Privacy Policy
        </button>
      </p>

      {validationError && <ErrorAlert message={validationError} />}

      <ExampleDownload />

      {file && (
        <ModelSelector onTrain={handleTrain} disabled={loading || hasResults} />
      )}

      {loading && <LoadingOverlay />}
      {error && <ErrorAlert message={error} />}

      {hasResults && (
        <ResultsTabs pythonResults={pythonResults} rResults={rResults} />
      )}

      <footer className="mt-12 pt-4 border-t border-gray-200 text-center text-xs text-gray-400">
        <button
          onClick={() => setPage("privacy")}
          className="underline hover:text-gray-600"
        >
          Privacy Policy
        </button>
      </footer>
    </div>
  );
}
