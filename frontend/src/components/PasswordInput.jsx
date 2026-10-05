import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { localStrengthHint } from "../utils/demo.js";

export default function PasswordInput({ id, label, value, onChange, onSubmitLabel, onSubmit, disabled }) {
  const [visible, setVisible] = useState(false);
  const hint = localStrengthHint(value);
  return (
    <div>
      <label htmlFor={id} className="text-sm text-slate-300">
        {label}
      </label>
      <div className="mt-2 flex gap-2">
        <input
          id={id}
          type={visible ? "text" : "password"}
          autoComplete="off"
          className="focus-ring w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-white"
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
        <button
          type="button"
          className="focus-ring rounded-xl border border-slate-700 px-3 text-slate-300"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? "Hide password" : "Show password"}
        >
          {visible ? <EyeOff size={16} /> : <Eye size={16} />}
        </button>
      </div>
      <div className="mt-3">
        <div className="mb-1 flex justify-between text-xs text-slate-400">
          <span>Local strength hint (not backend analysis)</span>
          <span>{hint.label}</span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-slate-800">
          <div className="h-full rounded-full" style={{ width: `${hint.score}%`, background: hint.color }} />
        </div>
      </div>
      {onSubmit ? (
        <button
          type="button"
          className="focus-ring mt-4 w-full rounded-xl bg-cyan-500 px-4 py-3 text-sm font-medium text-slate-950 disabled:opacity-50"
          onClick={onSubmit}
          disabled={disabled}
        >
          {onSubmitLabel || "Analyze Password"}
        </button>
      ) : null}
    </div>
  );
}
