import { useState } from "react";
import PasswordInput from "../components/PasswordInput.jsx";
import LoadingAnalysis from "../components/LoadingAnalysis.jsx";
import ErrorState from "../components/ErrorState.jsx";
import SecurityScoreCard from "../components/SecurityScoreCard.jsx";
import RecommendationPanel from "../components/RecommendationPanel.jsx";
import ImprovementPath from "../components/ImprovementPath.jsx";
import CompositionChart from "../components/CompositionChart.jsx";
import { useAnalysis } from "../hooks/useAnalysis.js";

export default function Analyze() {
  const { runAnalysis, analysis, loading, error, isDemo } = useAnalysis();
  const [password, setPassword] = useState("");

  async function handleAnalyze() {
    try {
      await runAnalysis(password);
    } catch {
      return;
    } finally {
      setPassword("");
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <h1 className="text-2xl font-semibold text-white">Password Security Analyzer</h1>
      <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-5">
        <PasswordInput
          id="analyze-password"
          label="Enter password"
          value={password}
          onChange={setPassword}
          onSubmit={handleAnalyze}
          disabled={loading || !password}
        />
        <p className="mt-3 text-xs text-slate-500">Security is processed in memory and never stored.</p>
      </section>
      <ErrorState message={error} />
      {loading ? <LoadingAnalysis /> : null}
      {!isDemo && !loading ? (
        <>
          <SecurityScoreCard score={analysis.score} strength={analysis.strength} />
          <CompositionChart composition={analysis.composition} />
          <ImprovementPath steps={analysis.improvement_path} />
          <RecommendationPanel items={analysis.recommendations} />
        </>
      ) : null}
    </div>
  );
}
