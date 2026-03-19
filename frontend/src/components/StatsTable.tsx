import type { ModelStats } from "../types/models";

interface Props {
  stats: ModelStats;
}

const LABELS: Record<string, string> = {
  model_type: "Model Type",
  aic: "AIC",
  aicc: "AICc",
  bic: "BIC",
  num_parameters: "NumParameters",
  likelihood: "Likelihood",
  brier_score: "BrierScore",
  log_loss: "LogLoss",
  rmse: "RMSE",
  acc_cv: "ACCcv",
  precision: "Precision",
  recall: "Recall",
  f1: "F1",
};

export default function StatsTable({ stats }: Props) {
  const entries = Object.entries(stats) as [keyof ModelStats, string | number][];
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm border border-gray-200">
        <thead>
          <tr className="bg-gray-50">
            {entries.map(([key]) => (
              <th
                key={key}
                className="px-3 py-2 text-left font-medium text-gray-600 border-b"
              >
                {LABELS[key] || key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            {entries.map(([key, val]) => (
              <td key={key} className="px-3 py-2 border-b text-gray-800">
                {typeof val === "number" ? val.toFixed(2) : val}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}
