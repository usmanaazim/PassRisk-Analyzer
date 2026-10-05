import { useAnalysis } from "../hooks/useAnalysis.js";
import RiskBadge from "../components/RiskBadge.jsx";
import AttackResistanceChart from "../charts/AttackResistanceChart.jsx";

function Card({ title, children }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
      <h2 className="text-sm font-medium text-white">{title}</h2>
      <div className="mt-3 space-y-2 text-sm text-slate-300">{children}</div>
    </section>
  );
}

export default function Attacks() {
  const { analysis } = useAnalysis();
  const a = analysis.attack_resistance;
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-white">Attack Resistance Analysis</h1>
        <p className="mt-2 max-w-3xl text-sm text-slate-400">
          Estimates depend on assumptions such as character set, password length, and an illustrative offline guess rate.
          This page does not perform uncontrolled brute-force cracking or target real accounts.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <Card title="Dictionary Attack">
          <p>Resistance: <RiskBadge level={a.levels.dictionary} /></p>
          <p>Dictionary Match: {analysis.dictionary.dictionary_match ? "DETECTED" : "NOT DETECTED"}</p>
        </Card>
        <Card title="Pattern Attack">
          <p>Resistance: <RiskBadge level={a.levels.pattern} /></p>
          <p>Predictable Patterns: {a.details.predictable_patterns}</p>
        </Card>
        <Card title="Rule-Based Attack">
          <p>Resistance: <RiskBadge level={a.levels.rule_based} /></p>
          <p>Predictable Transformations: {a.details.predictable_transformations}</p>
        </Card>
        <Card title="Brute Force">
          <p>Estimated Search Space: {a.details.estimated_search_space_bits} bits</p>
          <p>Estimated Resistance: <RiskBadge level={a.levels.brute_force} /></p>
        </Card>
      </div>
      <AttackResistanceChart attack={a} />
      <p className="text-xs leading-5 text-slate-500">{a.disclaimer}</p>
    </div>
  );
}
