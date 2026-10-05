import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function MLPredictionCard({ ml, prediction, confidence }) {
  const data = Object.entries(ml?.probabilities || {}).map(([name, value]) => ({
    name: name.replaceAll("_", " "),
    value: Number((value * 100).toFixed(1)),
  }));
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">ML Prediction</p>
      <p className="mt-2 text-xl font-semibold text-white">
        {String(prediction || ml?.label || "").replaceAll("_", " ")}
      </p>
      <p className="text-sm text-slate-400">Confidence {(confidence * 100).toFixed(1)}%</p>
      <div className="mt-3 h-48">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 24 }}>
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis type="category" dataKey="name" width={100} tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Tooltip />
            <Bar dataKey="value" fill="#818cf8" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
