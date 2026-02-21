import JSZip from "jszip";
import type { ModelResult, ModelStats } from "../types/models";

function statsToCsv(allStats: ModelStats[]): string {
  if (allStats.length === 0) return "";
  const headers = [
    "Model_type",
    "Models_AIC",
    "AICc",
    "Models_BIC",
    "NumParameters",
    "Likelihood",
    "BrierScore",
    "LogLoss",
    "RMSE",
    "ACCcv",
    "Precision",
    "Recall",
    "F1",
  ];
  const rows = allStats.map((s) =>
    [
      s.model_type,
      s.aic,
      s.aicc,
      s.bic,
      s.num_parameters,
      s.likelihood,
      s.brier_score,
      s.log_loss,
      s.rmse,
      s.acc_cv,
      s.precision,
      s.recall,
      s.f1,
    ].join(",")
  );
  return [headers.join(","), ...rows].join("\n");
}

function coefficientsToCsv(
  coefficients: { feature: string; coef: number }[]
): string {
  const header = "Features,coef";
  const rows = coefficients.map((c) => `${c.feature},${c.coef}`);
  return [header, ...rows].join("\n");
}

function predictionsToCsv(
  mergedRows: Record<string, Record<string, number | string>>
): string {
  if (Object.keys(mergedRows).length === 0) return "";

  const firstRow = Object.values(mergedRows)[0];
  const headers = Object.keys(firstRow);
  const rows = Object.values(mergedRows).map((row) =>
    headers.map((h) => row[h] ?? "").join(",")
  );
  return [headers.join(","), ...rows].join("\n");
}

export async function buildResultsZip(
  pythonResults: Record<string, ModelResult> | null,
  rResults: Record<string, ModelResult> | null
): Promise<Blob> {
  const zip = new JSZip();

  // Collect all stats
  const allStats: ModelStats[] = [];
  if (pythonResults) {
    Object.values(pythonResults).forEach((r) => allStats.push(r.stats));
  }
  if (rResults) {
    Object.values(rResults).forEach((r) => allStats.push(r.stats));
  }
  zip.file("AllStats.csv", statsToCsv(allStats));

  // Coefficient files
  if (pythonResults) {
    Object.entries(pythonResults).forEach(([mt, r]) => {
      zip.file(`PY_${mt}_Coefficients.csv`, coefficientsToCsv(r.coefficients));
    });
  }
  if (rResults) {
    Object.entries(rResults).forEach(([mt, r]) => {
      zip.file(`R_${mt}_Coefficients.csv`, coefficientsToCsv(r.coefficients));
    });
  }

  // Merge predictions by row
  const merged: Record<string, Record<string, number | string>> = {};

  const addPredictions = (
    results: Record<string, ModelResult>,
    prefix: string
  ) => {
    Object.entries(results).forEach(([mt, r]) => {
      r.predictions.forEach((p) => {
        const key = String(p.row);
        if (!merged[key]) merged[key] = { Row: p.row };
        merged[key][`${prefix}_${mt}predictedProbabilities`] =
          p.predicted_probability;
        merged[key][`${prefix}_${mt}prediction`] = p.prediction;
      });
    });
  };

  if (pythonResults) addPredictions(pythonResults, "Py");
  if (rResults) addPredictions(rResults, "R");

  zip.file("PredictedOutcomes.csv", predictionsToCsv(merged));

  return zip.generateAsync({ type: "blob" });
}
