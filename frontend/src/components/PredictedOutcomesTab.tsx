import { useMemo, useState } from "react";
import { Download } from "lucide-react";
import type { ModelResult } from "../types/models";
import { buildResultsZip } from "../lib/zipBuilder";

interface Props {
  pythonResults: Record<string, ModelResult> | null;
  rResults: Record<string, ModelResult> | null;
}

export default function PredictedOutcomesTab({
  pythonResults,
  rResults,
}: Props) {
  const [downloading, setDownloading] = useState(false);

  // Merge predictions by row
  const { headers, rows } = useMemo(() => {
    const merged: Record<string, Record<string, number | string>> = {};

    const addPreds = (
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

    if (pythonResults) addPreds(pythonResults, "Py");
    if (rResults) addPreds(rResults, "R");

    const allRows = Object.values(merged);
    const hdrs = allRows.length > 0 ? Object.keys(allRows[0]) : [];
    return { headers: hdrs, rows: allRows };
  }, [pythonResults, rResults]);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const blob = await buildResultsZip(pythonResults, rResults);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "results.zip";
      a.click();
      URL.revokeObjectURL(url);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-2">
        Predicted Outcomes
      </h2>
      <p className="text-sm text-gray-600 mb-4">
        Here is the predicted Outcome (1 or 0) of each data entry used to build
        the model and the confidence (predicted probability) in that predicted
        Outcome.
      </p>

      <div className="overflow-x-auto max-h-96 overflow-y-auto mb-4">
        <table className="min-w-full text-sm border border-gray-200">
          <thead className="sticky top-0 bg-gray-50">
            <tr>
              {headers.map((h) => (
                <th
                  key={h}
                  className="px-3 py-2 text-left font-medium text-gray-600 border-b"
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 200).map((row, i) => (
              <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                {headers.map((h) => (
                  <td key={h} className="px-3 py-1 border-b text-gray-800">
                    {typeof row[h] === "number"
                      ? Number(row[h]).toFixed(2)
                      : row[h]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length > 200 && (
          <p className="text-sm text-gray-500 mt-2">
            Showing first 200 of {rows.length} rows. Download the ZIP for full
            data.
          </p>
        )}
      </div>

      <button
        onClick={handleDownload}
        disabled={downloading}
        className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 transition-colors"
      >
        <Download size={16} />
        {downloading ? "Preparing..." : "Download Results"}
      </button>
    </div>
  );
}
