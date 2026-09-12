import React from "react";

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  title,
  description,
  icon = "📋",
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="zv-card p-8 text-center flex flex-col items-center justify-center max-w-md mx-auto my-6 border-dashed border-[#334155]">
      <div className="w-12 h-12 rounded-full bg-[#1E293B] border border-[#334155] flex items-center justify-center text-2xl mb-3">
        {icon}
      </div>
      <h3 className="text-sm font-semibold text-white mb-1">{title}</h3>
      <p className="text-xs text-[#94A3B8] mb-4 leading-relaxed">{description}</p>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="zv-btn-primary text-xs"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
