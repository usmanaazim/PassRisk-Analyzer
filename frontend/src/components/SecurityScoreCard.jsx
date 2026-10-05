import { STRENGTH_COLORS } from "../utils/demo.js";

export default function SecurityScoreCard({ score, strength }) {
  const color = STRENGTH_COLORS[strength] || "#38bdf8";
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-5">
      <p className="text-sm text-slate-400">Security Score Gauge</p>
      <div className="mt-3 flex items-center justify-center">
        <svg width="160" height="160" viewBox="0 0 140 140" role="img" aria-label={`Score ${score}, ${strength}`}>
          <circle cx="70" cy="70" r={radius} stroke="#1e293b" strokeWidth="12" fill="none" />
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke={color}
            strokeWidth="12"
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            transform="rotate(-90 70 70)"
            className="motion-safe:transition-[stroke-dashoffset] motion-safe:duration-700"
          />
          <text x="70" y="66" textAnchor="middle" className="fill-white" fontSize="28" fontWeight="700">
            {score}
          </text>
          <text x="70" y="88" textAnchor="middle" className="fill-slate-400" fontSize="10">
            {String(strength).replaceAll("_", " ")}
          </text>
        </svg>
      </div>
    </section>
  );
}
