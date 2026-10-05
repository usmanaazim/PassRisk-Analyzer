export default function RiskBadge({ level, label }) {
  const text = label || level || "UNKNOWN";
  const tone = String(text).toUpperCase();
  const color =
    tone.includes("CRITICAL") || tone.includes("VERY_WEAK") || tone === "VERY_LOW"
      ? "bg-red-500/15 text-red-300 border-red-500/30"
      : tone.includes("HIGH") || tone === "WEAK"
        ? "bg-orange-500/15 text-orange-300 border-orange-500/30"
        : tone.includes("MEDIUM") || tone === "MODERATE"
          ? "bg-amber-500/15 text-amber-200 border-amber-500/30"
          : tone.includes("LOW") || tone === "STRONG"
            ? "bg-teal-500/15 text-teal-200 border-teal-500/30"
            : "bg-emerald-500/15 text-emerald-200 border-emerald-500/30";
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs ${color}`}>
      <span aria-hidden>●</span>
      {text.replaceAll("_", " ")}
    </span>
  );
}
