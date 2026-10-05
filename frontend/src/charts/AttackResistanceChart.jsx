import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function AttackResistanceChart({ attack }) {
  const data = [
    { name: "Dictionary", value: attack.dictionary },
    { name: "Rule-Based", value: attack.rule_based },
    { name: "Pattern", value: attack.pattern },
    { name: "Brute Force", value: attack.brute_force },
  ];
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Attack Resistance</p>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <YAxis domain={[0, 100]} tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Tooltip
              content={({ active, payload, label }) =>
                active && payload?.[0] ? (
                  <div className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-slate-200">
                    <p>{label} resistance: {payload[0].value}</p>
                    <p className="mt-1 text-slate-400">Educational estimate, not a live crack attempt.</p>
                  </div>
                ) : null
              }
            />
            <Bar dataKey="value" fill="#38bdf8" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
