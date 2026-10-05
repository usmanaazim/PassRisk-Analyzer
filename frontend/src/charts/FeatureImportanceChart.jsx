import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { featureLabel } from "../utils/demo.js";

export default function FeatureImportanceChart({ items }) {
  const data = (items || []).slice(0, 8).map((row) => ({
    name: featureLabel(row.feature),
    value: Number((row.importance * 100).toFixed(1)),
  }));
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Feature Importance</p>
      <div className="mt-3 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 16 }}>
            <XAxis type="number" domain={[0, "auto"]} tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <YAxis type="category" dataKey="name" width={150} tick={{ fill: "#cbd5e1", fontSize: 11 }} />
            <Tooltip />
            <Bar dataKey="value" fill="#22d3ee" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
