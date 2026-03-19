import { useState } from "react";
import { ChevronDown, ChevronUp, Info } from "lucide-react";

export default function Instructions() {
  const [open, setOpen] = useState(false);

  return (
    <div className="mb-6 border border-blue-200 rounded-lg bg-blue-50">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 text-left"
      >
        <span className="flex items-center gap-2 font-medium text-blue-800">
          <Info size={18} />
          About this application &amp; how to use it
        </span>
        {open ? (
          <ChevronUp size={18} className="text-blue-600" />
        ) : (
          <ChevronDown size={18} className="text-blue-600" />
        )}
      </button>

      {open && (
        <div className="px-4 pb-4 text-sm text-gray-700 space-y-4">
          <div>
            <h3 className="font-semibold text-gray-900 mb-1">
              What does this application do?
            </h3>
            <p>
              This dashboard lets you train and compare three logistic
              regression-based student models commonly used in educational data
              mining: the <strong>Additive Factor Model (AFM)</strong>, the{" "}
              <strong>Performance Factor Model (PFM)</strong>, and the{" "}
              <strong>Item Factor Model (IFM)</strong>. Each model is trained
              using both a <strong>Python</strong> (scikit-learn) and an{" "}
              <strong>R</strong> (glm) implementation so you can compare the
              results side by side.
            </p>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-1">
              How to use it
            </h3>
            <ol className="list-decimal list-inside space-y-1.5">
              <li>
                <strong>Upload your data</strong> &ndash; Drag and drop (or
                click to browse) an XLSX file containing your student
                interaction data. The file must include the columns:{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  AnonStudentId
                </code>
                ,{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  First Attempt
                </code>
                ,{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  Corrects
                </code>
                ,{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  Incorrects
                </code>
                ,{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  Hints
                </code>
                ,{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  Opportunity
                </code>
                , and{" "}
                <code className="bg-gray-100 px-1 rounded text-xs">
                  KC (Default)
                </code>
                . You can download an example template below to see the expected
                format.
              </li>
              <li>
                <strong>Select models</strong> &ndash; Choose one or more models
                to train (AFM, PFM, IFM).
              </li>
              <li>
                <strong>Train</strong> &ndash; Click the{" "}
                <em>Train Selected Models</em> button. The application trains
                each model in both Python and R simultaneously.
              </li>
              <li>
                <strong>Review results</strong> &ndash; After training, four
                tabs appear:
                <ul className="list-disc list-inside ml-4 mt-1 space-y-0.5">
                  <li>
                    <strong>Python / R</strong> &ndash; Model statistics and
                    feature coefficients for each implementation.
                  </li>
                  <li>
                    <strong>Evaluation Metrics</strong> &ndash; A comparative
                    table and bar charts across all models (AIC, BIC, RMSE, F1,
                    etc.).
                  </li>
                  <li>
                    <strong>Predicted Outcomes &amp; Downloads</strong> &ndash;
                    A preview of predicted probabilities and a button to download
                    all results as a ZIP file.
                  </li>
                </ul>
              </li>
            </ol>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-1">
              About the models
            </h3>
            <ul className="list-disc list-inside space-y-1.5">
              <li>
                <strong>AFM (Additive Factor Model)</strong> &ndash; Predicts
                student performance based on the number of practice
                opportunities per knowledge component (KC) and a per-student
                intercept.
              </li>
              <li>
                <strong>PFM (Performance Factor Model)</strong> &ndash; Extends
                AFM by also considering the number of prior correct and
                incorrect attempts per KC.
              </li>
              <li>
                <strong>IFM (Item Factor Model)</strong> &ndash; Models
                item-level difficulty by using only per-KC intercepts and a
                per-student intercept, without opportunity counts.
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
