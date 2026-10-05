export default function EntropyCard({ entropy, caveat }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <p className="text-xs uppercase tracking-wider text-slate-400">Theoretical entropy</p>
      <p className="mt-2 text-2xl font-semibold text-white">{entropy} bits</p>
      <p className="mt-3 text-xs leading-5 text-slate-400">
        {caveat ||
          "Theoretical entropy does not perfectly represent real-world password security because humans choose predictable passwords."}
      </p>
    </section>
  );
}
