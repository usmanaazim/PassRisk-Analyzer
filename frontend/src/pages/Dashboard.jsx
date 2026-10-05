import { useAnalysis } from "../hooks/useAnalysis.js";
import MetricCard from "../components/MetricCard.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import SecurityScoreCard from "../components/SecurityScoreCard.jsx";
import CompositionChart from "../components/CompositionChart.jsx";
import SecurityRadar from "../charts/SecurityRadar.jsx";
import AttackResistanceChart from "../charts/AttackResistanceChart.jsx";
import RiskBreakdown from "../components/RiskBreakdown.jsx";
import MLPredictionCard from "../components/MLPredictionCard.jsx";
import FeatureImportanceChart from "../charts/FeatureImportanceChart.jsx";
import RecommendationPanel from "../components/RecommendationPanel.jsx";
import PrivacyPanel from "../components/PrivacyPanel.jsx";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { analysis, isDemo } = useAnalysis();
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-white">Password Security & Attack-Resistance Analysis</h1>
          <p className="mt-2 max-w-3xl text-sm text-slate-400">
            Evaluate password strength using security analysis + machine learning. Theoretical entropy is an upper bound;
            real-world strength is reduced by human predictability.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {isDemo ? (
            <span className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs text-amber-200">
              Demo Analysis
            </span>
          ) : (
            <span className="rounded-full border border-cyan-500/30 bg-cyan-500/10 px-3 py-1 text-xs text-cyan-200">
              Live Analysis
            </span>
          )}
          <Link to="/analyze" className="focus-ring rounded-xl bg-cyan-500 px-4 py-2 text-sm font-medium text-slate-950">
            Analyze Password
          </Link>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard title="Security Score" value={`${analysis.score}/100`} subtitle={analysis.score_note} />
        <MetricCard title="Risk Level" value={<RiskBadge level={analysis.risk_level} />} />
        <MetricCard title="Entropy" value={`${analysis.entropy} bits`} subtitle="Theoretical, not human-adjusted" />
        <MetricCard title="ML Result" value={String(analysis.ml_prediction).replaceAll("_", " ")} subtitle={`Confidence ${((analysis.ml_confidence || 0) * 100).toFixed(1)}%`} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <SecurityScoreCard score={analysis.score} strength={analysis.strength} />
        <CompositionChart composition={analysis.composition} />
        <SecurityRadar radar={analysis.radar} />
        <AttackResistanceChart attack={analysis.attack_resistance} />
        <RiskBreakdown radar={analysis.radar} />
        <MLPredictionCard ml={analysis.ml} prediction={analysis.ml_prediction} confidence={analysis.ml_confidence} />
      </div>
      <FeatureImportanceChart items={analysis.ml?.feature_importance} />
      <RecommendationPanel items={analysis.recommendations} />
      <PrivacyPanel />
    </div>
  );
}
