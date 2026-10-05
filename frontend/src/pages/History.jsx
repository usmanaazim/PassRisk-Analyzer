import AnalysisHistory from "../components/AnalysisHistory.jsx";
import { useAnalysis } from "../hooks/useAnalysis.js";

export default function History() {
  const { history, wipeHistory } = useAnalysis();
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">Analysis History</h1>
      <AnalysisHistory items={history} onClear={wipeHistory} />
    </div>
  );
}
