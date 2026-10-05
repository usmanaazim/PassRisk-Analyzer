import { AlertTriangle, CheckCircle2 } from "lucide-react";

export default function RecommendationPanel({ items }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-sm text-slate-300">Security Recommendations</p>
      <ul className="mt-3 space-y-3">
        {(items || []).map((item) => (
          <li key={item.title} className="flex gap-3">
            {item.severity === "ok" ? (
              <CheckCircle2 className="mt-0.5 shrink-0 text-emerald-400" size={18} />
            ) : (
              <AlertTriangle
                className={`mt-0.5 shrink-0 ${item.severity === "high" ? "text-red-400" : "text-amber-400"}`}
                size={18}
              />
            )}
            <div>
              <p className="text-sm text-white">{item.title}</p>
              <p className="text-xs leading-5 text-slate-400">{item.detail}</p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
