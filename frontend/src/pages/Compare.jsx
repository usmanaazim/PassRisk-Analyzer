import { useState } from "react";
import PasswordInput from "../components/PasswordInput.jsx";
import ErrorState from "../components/ErrorState.jsx";
import { comparePasswords } from "../services/api.js";

export default function Compare() {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function run() {
    setError("");
    setLoading(true);
    try {
      const data = await comparePasswords(a, b);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setA("");
      setB("");
      setLoading(false);
    }
  }

  const rows = [
    ["Score", "score", "score"],
    ["Length", "length", "length"],
    ["Entropy", "entropy", "entropy"],
    ["Dictionary Risk", "dictionary_risk", "dictionary_risk"],
    ["Pattern Risk", "pattern_risk", "pattern_risk"],
    ["Attack Resistance", "attack_resistance", "attack_resistance"],
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">Compare Password Security</h1>
      <div className="grid gap-4 lg:grid-cols-2">
        <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <PasswordInput id="pwd-a" label="Password A" value={a} onChange={setA} />
        </section>
        <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <PasswordInput id="pwd-b" label="Password B" value={b} onChange={setB} />
        </section>
      </div>
      <button
        type="button"
        className="focus-ring rounded-xl bg-cyan-500 px-4 py-3 text-sm font-medium text-slate-950 disabled:opacity-50"
        onClick={run}
        disabled={loading || !a || !b}
      >
        Compare
      </button>
      <ErrorState message={error} />
      {result ? (
        <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <table className="min-w-full text-sm text-slate-300">
            <thead>
              <tr className="text-left text-slate-400">
                <th className="p-2" />
                <th className="p-2">Password A</th>
                <th className="p-2">Password B</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(([label, key]) => (
                <tr key={label} className="border-t border-slate-800">
                  <td className="p-2 text-slate-400">{label}</td>
                  <td className="p-2 text-white">{String(result.a[key])}</td>
                  <td className="p-2 text-white">{String(result.b[key])}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
