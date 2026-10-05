import { groupHistory } from "../utils/history.js";

export default function AnalysisHistory({ items, onClear }) {
  const groups = groupHistory(items);
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-sm text-slate-300">Analysis History</h2>
        <button type="button" className="focus-ring text-xs text-cyan-300" onClick={onClear}>
          Clear History
        </button>
      </div>
      <p className="mt-2 text-xs text-slate-500">
        Metadata only (score, risk, entropy, strength). No passwords are stored.
      </p>
      {items.length === 0 ? (
        <p className="mt-6 text-sm text-slate-400">No analyses yet in this browser session.</p>
      ) : (
        <div className="mt-4 space-y-4">
          {Object.entries(groups).map(([day, rows]) => (
            <div key={day}>
              <p className="text-xs uppercase tracking-wide text-slate-500">{day}</p>
              <ul className="mt-2 space-y-2">
                {rows.map((row) => (
                  <li key={row.id} className="flex items-center justify-between rounded-lg bg-slate-900/70 px-3 py-2 text-sm">
                    <span className="text-white">{row.score}</span>
                    <span className="text-slate-400">{row.strength.replaceAll("_", " ")}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
