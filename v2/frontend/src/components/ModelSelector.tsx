import { useState } from "react";
import type { ModelType } from "../types/models";

interface Props {
  onTrain: (modelTypes: ModelType[]) => void;
  disabled: boolean;
}

const MODEL_OPTIONS: ModelType[] = ["AFM", "PFM", "IFM"];

export default function ModelSelector({ onTrain, disabled }: Props) {
  const [selected, setSelected] = useState<Set<ModelType>>(new Set());

  const toggle = (mt: ModelType) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(mt)) next.delete(mt);
      else next.add(mt);
      return next;
    });
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
      <p className="font-medium text-gray-700 mb-3">Choose Training Models</p>
      <div className="flex gap-4 items-center flex-wrap">
        {MODEL_OPTIONS.map((mt) => (
          <label key={mt} className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={selected.has(mt)}
              onChange={() => toggle(mt)}
              className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-gray-700">{mt}</span>
          </label>
        ))}
        <button
          onClick={() => onTrain(Array.from(selected))}
          disabled={disabled || selected.size === 0}
          className="ml-auto px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Train
        </button>
      </div>
    </div>
  );
}
