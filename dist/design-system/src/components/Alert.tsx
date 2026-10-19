import React from "react";

export type AlertVariant = "info" | "success" | "warning" | "error" | "ai" | "schedule_e1";

export interface AlertProps {
  variant?: AlertVariant;
  title?: string;
  children: React.ReactNode;
  action?: React.ReactNode;
  onClose?: () => void;
  className?: string;
}

const STYLES: Record<AlertVariant, { container: string; icon: string; title: string; symbol: string }> = {
  info: {
    container: "bg-blue-950/40 border-blue-800/60 text-blue-200",
    icon: "text-blue-400",
    title: "text-blue-300",
    symbol: "ℹ️",
  },
  success: {
    container: "bg-emerald-950/40 border-emerald-800/60 text-emerald-200",
    icon: "text-emerald-400",
    title: "text-emerald-300",
    symbol: "✅",
  },
  warning: {
    container: "bg-amber-950/40 border-amber-800/60 text-amber-200",
    icon: "text-amber-400",
    title: "text-amber-300",
    symbol: "⚠️",
  },
  error: {
    container: "bg-red-950/40 border-red-800/60 text-red-200",
    icon: "text-red-400",
    title: "text-red-300",
    symbol: "🚨",
  },
  ai: {
    container: "bg-indigo-950/40 border-indigo-800/60 text-indigo-200",
    icon: "text-indigo-400",
    title: "text-indigo-300",
    symbol: "🤖",
  },
  schedule_e1: {
    container: "bg-purple-950/40 border-purple-800/60 text-purple-200",
    icon: "text-purple-400",
    title: "text-purple-300",
    symbol: "⚖️",
  },
};

export const Alert: React.FC<AlertProps> = ({
  variant = "info",
  title,
  children,
  action,
  onClose,
  className = "",
}) => {
  const style = STYLES[variant];

  return (
    <div
      role="alert"
      className={`p-4 rounded-xl border flex items-start gap-3 text-xs leading-relaxed ${style.container} ${className}`}
    >
      <span className="text-base shrink-0 select-none">{style.symbol}</span>
      <div className="flex-1 space-y-1 min-w-0">
        {title && <h5 className={`font-bold tracking-tight text-xs ${style.title}`}>{title}</h5>}
        <div className="text-slate-300">{children}</div>
      </div>
      {action && <div className="shrink-0">{action}</div>}
      {onClose && (
        <button
          onClick={onClose}
          aria-label="Dismiss alert"
          className="shrink-0 p-1 text-slate-400 hover:text-white rounded-lg transition"
        >
          ✕
        </button>
      )}
    </div>
  );
};
