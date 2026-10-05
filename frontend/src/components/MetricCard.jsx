export default function MetricCard({ title, value, subtitle, children }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4 shadow-sm">
      <p className="text-xs uppercase tracking-wider text-slate-400">{title}</p>
      <div className="mt-2 text-2xl font-semibold text-white">{value}</div>
      {subtitle ? <p className="mt-1 text-sm text-slate-400">{subtitle}</p> : null}
      {children}
    </section>
  );
}
