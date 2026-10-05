const STEPS = [
  "Extracting features",
  "Checking patterns",
  "Calculating entropy",
  "Evaluating attack resistance",
  "Running ML model",
];

export default function LoadingAnalysis({ active = true }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-[#121a2b] p-5" role="status" aria-live="polite">
      <p className="text-sm font-medium text-white">Analyzing Password</p>
      <ul className="mt-4 space-y-2 text-sm text-slate-300">
        {STEPS.map((step, index) => (
          <li key={step} className="flex items-center gap-2">
            <span className={active ? "text-cyan-400" : "text-emerald-400"}>{index < 4 ? "✓" : "●"}</span>
            {step}
          </li>
        ))}
      </ul>
    </div>
  );
}
