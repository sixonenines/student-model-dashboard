import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

const EXPLANATIONS = [
  {
    name: "Precision",
    text: "Proportion of true positives to the amount of positive predictions. Should be interpreted as a probability, where 1 is the highest value which means that the model is not making any false positive predictions.",
  },
  {
    name: "Recall",
    text: "Proportion of true positives to the amount of positive outcomes. Should be interpreted as a probability, where 1 is the highest value which means that the model has no false negatives.",
  },
  {
    name: "F1",
    text: "Harmonic mean of precision and recall. Useful in cases where you want to take both the amount of false positives and false negatives into account. F1 value ranges between 0 and 1, where a lower value means that the model is making too many false positives or false negative predictions.",
  },
  {
    name: "RMSE",
    text: "Root mean squared error. Measures the average distance between predicted values and the actual values.",
  },
  {
    name: "ACCcv",
    text: "Accuracy with cross-validation. Useful to evaluate the model's ability to generalize to new data. The value ranges between 0 and 1, where 1 means that the model was able to correctly classify all data entries.",
  },
  {
    name: "Likelihood",
    text: "Measure of how well a model fits the data.",
  },
  {
    name: "LogLoss",
    text: "Natural logarithm of the likelihood function.",
  },
  {
    name: "NumParameters",
    text: "Number of parameters the model has.",
  },
  {
    name: "AIC",
    text: "Akaike Information Criterion. Useful for comparing goodness of fit between different models, the lower the better.",
  },
  {
    name: "AICc",
    text: "Corrected Akaike Information Criterion. Like AIC, but with a correction term that accounts for the number of parameters in relation to the sample size.",
  },
  {
    name: "BIC",
    text: "Bayesian Information Criterion. Like AIC, but with a stronger penalty on overly complex models.",
  },
  {
    name: "BrierScore",
    text: "Brier Score Loss. Measures the accuracy of probabilistic predictions. A low score means that the model is able to predict the correct outcome with high confidence.",
  },
];

export default function MetricExplanations() {
  const [open, setOpen] = useState(false);

  return (
    <div className="mb-4">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-800"
      >
        {open ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        Metric explanation
      </button>
      {open && (
        <div className="mt-2 pl-4 space-y-2 text-sm text-gray-600">
          {EXPLANATIONS.map((e) => (
            <p key={e.name}>
              <strong>{e.name}:</strong> {e.text}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
