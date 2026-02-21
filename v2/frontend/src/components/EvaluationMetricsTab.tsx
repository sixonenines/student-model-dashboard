import { useState, useMemo } from "react";
import type { ModelResult, ModelStats } from "../types/models";
import MetricExplanations from "./MetricExplanations";
import MetricBarChart from "./MetricBarChart";

interface Props {
  pythonResults: Record<string, ModelResult> | null;
  rResults: Record<string, ModelResult> | null;
}

const METRIC_KEYS: (keyof ModelStats)[] = [
  "aic",
  "aicc",
  "bic",
  "num_parameters",
  "likelihood",
  "brier_score",
  "log_loss",
  "rmse",
  "acc_cv",
  "precision",
  "recall",
  "f1",
];

const METRIC_LABELS: Record<string, string> = {
  aic: "Models_AIC",
  aicc: "AICc",
  bic: "Models_BIC",
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

export default function EvaluationMetricsTab({
  pythonResults,
  rResults,
}: Props) {
  const allStats = useMemo(() => {
    const stats: ModelStats[] = [];
    if (pythonResults)
      Object.values(pythonResults).forEach((r) => stats.push(r.stats));
    if (rResults)
      Object.values(rResults).forEach((r) => stats.push(r.stats));
    return stats;
  }, [pythonResults, rResults]);

  const [selectedMetrics, setSelectedMetrics] = useState<string[]>(
    METRIC_KEYS.length > 0 ? [METRIC_KEYS[0]] : []
  );

  const toggleMetric = (m: string) => {
    setSelectedMetrics((prev) =>
      prev.includes(m) ? prev.filter((x) => x !== m) : [...prev, m]
    );
  };

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Evaluation Metrics
      </h2>

      {/* Combined stats table */}
      <div className="overflow-x-auto mb-4">
        <table className="min-w-full text-sm border border-gray-200">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-3 py-2 text-left font-medium text-gray-600 border-b">
                Model_type
              </th>
              {METRIC_KEYS.map((k) => (
                <th
                  key={k}
                  className="px-3 py-2 text-left font-medium text-gray-600 border-b"
                >
                  {METRIC_LABELS[k]}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {allStats.map((s) => (
              <tr key={s.model_type}>
                <td className="px-3 py-2 border-b text-gray-800 font-medium">
                  {s.model_type}
                </td>
                {METRIC_KEYS.map((k) => (
                  <td key={k} className="px-3 py-2 border-b text-gray-800">
                    {typeof s[k] === "number"
                      ? (s[k] as number).toFixed(2)
                      : s[k]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <MetricExplanations />

      {/* Metric selector */}
      <div className="mb-4">
        <p className="text-sm font-medium text-gray-700 mb-2">
          Which statistic do you want to compare?
        </p>
        <div className="flex flex-wrap gap-2">
          {METRIC_KEYS.map((k) => (
            <label
              key={k}
              className="flex items-center gap-1 text-sm cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selectedMetrics.includes(k)}
                onChange={() => toggleMetric(k)}
                className="w-3.5 h-3.5 rounded border-gray-300 text-blue-600"
              />
              {METRIC_LABELS[k]}
            </label>
          ))}
        </div>
      </div>

      <MetricBarChart allStats={allStats} selectedMetrics={selectedMetrics} />
    </div>
  );
}
