import { NavLink } from "react-router-dom";
import { Moon, ShieldCheck, Sun } from "lucide-react";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/analyze", label: "Analyze" },
  { to: "/attacks", label: "Attack Analysis" },
  { to: "/ml", label: "ML Insights" },
  { to: "/compare", label: "Compare" },
  { to: "/history", label: "History" },
  { to: "/about", label: "About" },
];

export default function Navbar({ theme, onToggleTheme }) {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-800/80 bg-[#070b14]/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-500/15 text-cyan-300">
            <ShieldCheck size={18} />
          </div>
          <div>
            <p className="text-sm font-semibold tracking-wide text-white">PasswordGuard</p>
            <p className="text-[11px] text-slate-400">Security Analyzer</p>
          </div>
        </div>
        <nav className="flex flex-wrap items-center gap-1" aria-label="Primary">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `focus-ring rounded-lg px-3 py-1.5 text-sm ${
                  isActive ? "bg-slate-800 text-cyan-300" : "text-slate-300 hover:bg-slate-800/70"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-300">
            Privacy Protected
          </span>
          <button
            type="button"
            className="focus-ring inline-flex items-center gap-1 rounded-lg border border-slate-700 px-3 py-1.5 text-xs text-slate-200"
            onClick={onToggleTheme}
            aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          >
            {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
            {theme === "dark" ? "Light" : "Dark"}
          </button>
        </div>
      </div>
    </header>
  );
}
