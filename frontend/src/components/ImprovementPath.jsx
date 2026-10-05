import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function ImprovementPath({ steps }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Improve My Password</p>
      <p className="mt-1 text-xs text-slate-500">
        This simulator estimates how score components could improve. It does not generate a real password.
      </p>
      <div className="mt-4 h-48">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={steps}>
            <XAxis dataKey="label" hide />
            <YAxis domain={[0, 100]} tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#34d399" strokeWidth={2} dot />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <ol className="mt-3 space-y-2 text-sm text-slate-300">
        {(steps || []).map((step) => (
          <li key={step.label} className="flex justify-between">
            <span>{step.label}</span>
            <span>{step.score}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}
