import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

const COLORS = ["#38bdf8", "#818cf8", "#34d399", "#f59e0b"];

export default function CompositionChart({ composition }) {
  const data = [
    { name: "Lowercase", value: composition.lowercase },
    { name: "Uppercase", value: composition.uppercase },
    { name: "Numbers", value: composition.digits },
    { name: "Special", value: composition.special },
  ];
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Password Composition</p>
      <div className="mt-2 h-52">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" innerRadius={48} outerRadius={72} paddingAngle={3}>
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <ul className="grid grid-cols-2 gap-2 text-sm text-slate-300">
        {data.map((item, index) => (
          <li key={item.name} className="flex items-center justify-between">
            <span className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full" style={{ background: COLORS[index] }} />
              {item.name}
            </span>
            <span>{item.value}</span>
          </li>
        ))}
      </ul>
      <p className="mt-3 text-xs text-slate-400">
        Total Characters: {composition.length} · Unique Characters: {composition.unique}
      </p>
    </section>
  );
}
