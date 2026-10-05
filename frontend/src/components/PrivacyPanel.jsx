import { Lock } from "lucide-react";

export default function PrivacyPanel() {
  const items = [
    "Passwords are not stored",
    "Passwords are not logged",
    "Passwords are not included in URLs",
    "Analysis data contains no plaintext password",
    "Local development mode",
  ];
  return (
    <section className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-4">
      <div className="mb-3 flex items-center gap-2 text-emerald-300">
        <Lock size={16} />
        <h2 className="text-sm font-medium">Privacy Protection</h2>
      </div>
      <ul className="space-y-2 text-sm text-slate-300">
        {items.map((item) => (
          <li key={item}>✓ {item}</li>
        ))}
      </ul>
    </section>
  );
}
