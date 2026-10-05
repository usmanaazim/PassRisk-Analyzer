import PrivacyPanel from "../components/PrivacyPanel.jsx";

export default function About() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">About PasswordGuard</h1>
      <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-5 text-sm leading-6 text-slate-300">
        <p>
          PasswordGuard is an academic platform for password security evaluation and attack-resistance analysis.
          It combines feature extraction, entropy modeling, dictionary and pattern heuristics, and a Random Forest
          classifier trained on synthetic data.
        </p>
        <p className="mt-3">
          Theoretical entropy (H = L × log2(R)) estimates search space under a uniform-random assumption. Human-chosen
          passwords are typically much weaker because of dictionary words, years, keyboard walks, and mangling rules.
        </p>
        <p className="mt-3">Author / team: [Your Name], Final-year engineering project.</p>
      </section>
      <PrivacyPanel />
    </div>
  );
}
