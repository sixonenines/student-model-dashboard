import type { ModelResult } from "../types/models";
import StatsTable from "./StatsTable";
import CoefficientsTable from "./CoefficientsTable";

interface Props {
  results: Record<string, ModelResult>;
}

export default function PythonResultsTab({ results }: Props) {
  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Python Implementation
      </h2>
      {Object.entries(results).map(([mt, result]) => (
        <div key={mt} className="mb-6">
          <h3 className="text-lg font-medium text-gray-700 mb-2">{mt}</h3>
          <StatsTable stats={result.stats} />
          <div className="mt-2">
            <CoefficientsTable coefficients={result.coefficients} />
          </div>
        </div>
      ))}
    </div>
  );
}
