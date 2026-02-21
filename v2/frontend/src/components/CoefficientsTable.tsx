import type { CoefficientEntry } from "../types/models";

interface Props {
  coefficients: CoefficientEntry[];
}

export default function CoefficientsTable({ coefficients }: Props) {
  return (
    <div className="overflow-x-auto max-h-64 overflow-y-auto">
      <table className="min-w-full text-sm border border-gray-200">
        <thead className="sticky top-0 bg-gray-50">
          <tr>
            <th className="px-3 py-2 text-left font-medium text-gray-600 border-b">
              Features
            </th>
            <th className="px-3 py-2 text-left font-medium text-gray-600 border-b">
              Coefficient
            </th>
          </tr>
        </thead>
        <tbody>
          {coefficients.map((c, i) => (
            <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
              <td className="px-3 py-1 border-b text-gray-800 font-mono text-xs">
                {c.feature}
              </td>
              <td className="px-3 py-1 border-b text-gray-800">
                {c.coef.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
