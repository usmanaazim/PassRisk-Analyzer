import { useContext } from "react";
import { AnalysisContext } from "./analysisContext.js";

export function useAnalysis() {
  return useContext(AnalysisContext);
}
