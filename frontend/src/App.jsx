import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Sidebar from "./components/Sidebar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Analyze from "./pages/Analyze.jsx";
import Attacks from "./pages/Attacks.jsx";
import MLInsights from "./pages/MLInsights.jsx";
import Compare from "./pages/Compare.jsx";
import History from "./pages/History.jsx";
import About from "./pages/About.jsx";
import { AnalysisProvider } from "./hooks/AnalysisProvider.jsx";
import { useAnalysis } from "./hooks/useAnalysis.js";

function Shell({ theme, onToggleTheme }) {
  const { analysis, isDemo } = useAnalysis();
  return (
    <div className={theme === "light" ? "light min-h-screen bg-slate-100 text-slate-900" : "min-h-screen bg-[#070b14] text-slate-100"}>
      <Navbar theme={theme} onToggleTheme={onToggleTheme} />
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6">
        <Sidebar analysis={analysis} isDemo={isDemo} />
        <main className="min-w-0 flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<Analyze />} />
            <Route path="/attacks" element={<Attacks />} />
            <Route path="/ml" element={<MLInsights />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/history" element={<History />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem("passwordguard-theme") || "dark");

  useEffect(() => {
    localStorage.setItem("passwordguard-theme", theme);
    document.documentElement.classList.toggle("light", theme === "light");
  }, [theme]);

  return (
    <AnalysisProvider>
      <Shell theme={theme} onToggleTheme={() => setTheme((t) => (t === "dark" ? "light" : "dark"))} />
    </AnalysisProvider>
  );
}
