import React from "react";

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description: string;
  action?: React.ReactNode;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon = "📂",
  title,
  description,
  action,
  className = "",
}) => {
  return (
    <div
      className={`p-8 sm:p-12 text-center rounded-2xl border border-dashed border-slate-800 bg-[#0A0F1D]/50 flex flex-col items-center justify-center space-y-3 ${className}`}
    >
      <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-2xl shadow-inner select-none">
        {icon}
      </div>
      <div className="space-y-1 max-w-sm">
        <h4 className="text-sm font-bold text-white tracking-tight">{title}</h4>
        <p className="text-xs text-slate-400 leading-relaxed">{description}</p>
      </div>
      {action && <div className="pt-2">{action}</div>}
    </div>
  );
};
