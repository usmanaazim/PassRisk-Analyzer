import { useEffect, useState } from "react";
import { fetchMetrics } from "../services/api.js";
import { useAnalysis } from "../hooks/useAnalysis.js";
import MLPredictionCard from "../components/MLPredictionCard.jsx";
import FeatureImportanceChart from "../charts/FeatureImportanceChart.jsx";
import ErrorState from "../components/ErrorState.jsx";

export default function MLInsights() {
  const { analysis } = useAnalysis();
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMetrics()
      .then(setMetrics)
      .catch((err) => setError(err.message));
  }, []);

  const matrix = metrics?.selected?.confusion_matrix || [];
  const labels = metrics?.labels || [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">Machine Learning Insights</h1>
      <ErrorState message={error} />
      <div className="grid gap-4 md:grid-cols-3">
        <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <p className="text-xs text-slate-400">Model</p>
          <p className="mt-2 text-xl text-white">{metrics?.selected_model || analysis.ml?.model_name}</p>
        </section>
        <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <p className="text-xs text-slate-400">Accuracy</p>
          <p className="mt-2 text-xl text-white">
            {metrics ? `${(metrics.selected.accuracy * 100).toFixed(1)}%` : "—"}
          </p>
        </section>
        <section className="rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <p className="text-xs text-slate-400">F1 Score</p>
          <p className="mt-2 text-xl text-white">{metrics ? metrics.selected.f1_weighted.toFixed(2) : "—"}</p>
        </section>
      </div>
      {matrix.length > 0 ? (
        <section className="overflow-x-auto rounded-2xl border border-slate-800 bg-[#121a2b] p-4">
          <p className="text-sm text-slate-300">Confusion Matrix</p>
          <table className="mt-3 min-w-full text-center text-xs text-slate-300">
            <thead>
              <tr>
                <th className="p-2" />
                {labels.map((label) => (
                  <th key={label} className="p-2 font-normal">
                    {label.replaceAll("_", " ")}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {matrix.map((row, i) => (
                <tr key={labels[i]}>
                  <th className="p-2 text-left font-normal">{labels[i]?.replaceAll("_", " ")}</th>
                  {row.map((cell, j) => (
                    <td key={`${i}-${j}`} className="p-2">
                      <span className="inline-block min-w-8 rounded bg-cyan-500/15 px-2 py-1">{cell}</span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ) : null}
      <MLPredictionCard ml={analysis.ml} prediction={analysis.ml_prediction} confidence={analysis.ml_confidence} />
      <FeatureImportanceChart items={analysis.ml?.feature_importance || metrics?.feature_importance} />
    </div>
  );
}
