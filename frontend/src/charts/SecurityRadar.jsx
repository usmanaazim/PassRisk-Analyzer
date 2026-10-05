import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer } from "recharts";

export default function SecurityRadar({ radar }) {
  const data = [
    { metric: "Length", value: radar.length },
    { metric: "Complexity", value: radar.complexity },
    { metric: "Entropy", value: radar.entropy },
    { metric: "Uniqueness", value: radar.uniqueness },
    { metric: "Dictionary", value: radar.dictionary_resistance },
    { metric: "Pattern", value: radar.pattern_resistance },
  ];
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Security Radar</p>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data}>
            <PolarGrid stroke="#334155" />
            <PolarAngleAxis dataKey="metric" tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Radar dataKey="value" stroke="#22d3ee" fill="#22d3ee" fillOpacity={0.3} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
