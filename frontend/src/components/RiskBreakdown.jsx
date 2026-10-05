const LABELS = {
  length: "Length",
  complexity: "Complexity",
  entropy: "Entropy",
  uniqueness: "Uniqueness",
  dictionary_resistance: "Dictionary",
  pattern_resistance: "Pattern",
};

export default function RiskBreakdown({ radar }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Risk Breakdown</p>
      <div className="mt-4 space-y-3">
        {Object.entries(LABELS).map(([key, label]) => (
          <div key={key}>
            <div className="mb-1 flex justify-between text-xs text-slate-400">
              <span>{label}</span>
              <span>{radar[key]}</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-teal-400"
                style={{ width: `${radar[key]}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
