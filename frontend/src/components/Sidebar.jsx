import { Shield } from "lucide-react";

export default function Sidebar({ analysis, isDemo }) {
  return (
    <aside className="hidden w-64 shrink-0 lg:block">
      <div className="sticky top-20 space-y-3 rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
        <div className="flex items-center gap-2 text-slate-200">
          <Shield size={16} className="text-cyan-400" />
          <p className="text-sm font-medium">Session status</p>
        </div>
        <p className="text-xs leading-5 text-slate-400">
          {isDemo
            ? "Showing labeled demo analysis until you evaluate a password."
            : "Live analysis metadata only. The plaintext password was discarded."}
        </p>
        <dl className="space-y-2 text-sm">
          <div className="flex justify-between text-slate-300">
            <dt>Score</dt>
            <dd className="font-medium">{analysis.score}/100</dd>
          </div>
          <div className="flex justify-between text-slate-300">
            <dt>Risk</dt>
            <dd>{analysis.risk_level}</dd>
          </div>
          <div className="flex justify-between text-slate-300">
            <dt>ML</dt>
            <dd>{analysis.ml_prediction}</dd>
          </div>
        </dl>
      </div>
    </aside>
  );
}
