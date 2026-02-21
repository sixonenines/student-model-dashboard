import { useState } from "react";
import type { ModelResult } from "../types/models";
import PythonResultsTab from "./PythonResultsTab";
import RResultsTab from "./RResultsTab";
import EvaluationMetricsTab from "./EvaluationMetricsTab";
import PredictedOutcomesTab from "./PredictedOutcomesTab";

interface Props {
  pythonResults: Record<string, ModelResult> | null;
  rResults: Record<string, ModelResult> | null;
}

const TABS = [
  "Python",
  "R",
  "Evaluation Metrics",
  "Predicted Outcomes and Downloads",
] as const;

type Tab = (typeof TABS)[number];

export default function ResultsTabs({ pythonResults, rResults }: Props) {
  const [activeTab, setActiveTab] = useState<Tab>("Python");

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      {/* Tab headers */}
      <div className="flex border-b border-gray-200">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-3 text-sm font-medium transition-colors ${
              activeTab === tab
                ? "text-blue-600 border-b-2 border-blue-600 bg-blue-50"
                : "text-gray-600 hover:text-gray-800 hover:bg-gray-50"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-4">
        {activeTab === "Python" && pythonResults && (
          <PythonResultsTab results={pythonResults} />
        )}
        {activeTab === "R" && rResults && (
          <RResultsTab results={rResults} />
        )}
        {activeTab === "Evaluation Metrics" && (
          <EvaluationMetricsTab
            pythonResults={pythonResults}
            rResults={rResults}
          />
        )}
        {activeTab === "Predicted Outcomes and Downloads" && (
          <PredictedOutcomesTab
            pythonResults={pythonResults}
            rResults={rResults}
          />
        )}
      </div>
    </div>
  );
}
