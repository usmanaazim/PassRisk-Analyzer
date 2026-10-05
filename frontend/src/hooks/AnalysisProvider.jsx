import { useMemo, useState } from "react";
import { DEMO_ANALYSIS } from "../utils/demo.js";
import { loadHistory, saveHistoryItem, clearHistory } from "../utils/history.js";
import { analyzePassword } from "../services/api.js";
import { AnalysisContext } from "./analysisContext.js";

export function AnalysisProvider({ children }) {
  const [analysis, setAnalysis] = useState(DEMO_ANALYSIS);
  const [history, setHistory] = useState(loadHistory);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const value = useMemo(
    () => ({
      analysis,
      history,
      error,
      loading,
      isDemo: Boolean(analysis?.isDemo),
      async runAnalysis(password) {
        setError("");
        setLoading(true);
        try {
          const result = await analyzePassword(password);
          result.isDemo = false;
          setAnalysis(result);
          setHistory(saveHistoryItem(result));
          return result;
        } catch (err) {
          setError(err.message || "Analysis failed.");
          throw err;
        } finally {
          setLoading(false);
        }
      },
      resetToDemo() {
        setAnalysis(DEMO_ANALYSIS);
      },
      wipeHistory() {
        setHistory(clearHistory());
      },
    }),
    [analysis, history, error, loading]
  );

  return <AnalysisContext.Provider value={value}>{children}</AnalysisContext.Provider>;
}
