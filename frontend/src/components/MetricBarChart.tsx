import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
} from "recharts";
import type { ModelStats } from "../types/models";

interface Props {
  allStats: ModelStats[];
  selectedMetrics: string[];
}

export default function MetricBarChart({ allStats, selectedMetrics }: Props) {
  if (selectedMetrics.length === 0) return null;

  return (
    <div className="space-y-6">
      {selectedMetrics.map((metric) => {
        const data = allStats.map((s) => ({
          name: s.model_type,
          value: (s as any)[metric] as number,
          fill: s.model_type.startsWith("Py_") ? "#22c55e" : "#3b82f6",
        }));

        return (
          <div key={metric}>
            <h4 className="text-sm font-medium text-gray-700 mb-2">{metric}</h4>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip />
                <Legend
                  payload={[
                    { value: "Python", type: "square", color: "#22c55e" },
                    { value: "R", type: "square", color: "#3b82f6" },
                  ]}
                />
                <Bar dataKey="value" name={metric}>
                  {data.map((entry, index) => (
                    <Cell key={index} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        );
      })}
    </div>
  );
}
