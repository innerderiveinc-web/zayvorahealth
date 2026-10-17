/**
 * @file EmptyState.tsx
 * @description Empty-state illustration with title, message, and optional CTA.
 * Placed in /ui to co-exist with the root EmptyState.tsx without collision.
 */
import React from "react";

interface EmptyStateProps {
  /** Emoji or icon character displayed above the title */
  icon?: string;
  /** Bold heading */
  title: string;
  /** Descriptive paragraph */
  description: string;
  /** Optional call-to-action button label */
  actionLabel?: string;
  /** Handler for the action button */
  onAction?: () => void;
}

/**
 * EmptyState – illustrated placeholder shown when a list/table has no data.
 */
export function EmptyState({
  icon = "📋",
  title,
  description,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 text-center">
      {/* Icon bubble */}
      <div className="w-16 h-16 rounded-2xl bg-[#1E293B] border border-[#334155] flex items-center justify-center text-3xl mb-4 shadow-inner">
        {icon}
      </div>

      <h3 className="text-sm font-semibold text-white mb-1">{title}</h3>
      <p className="text-xs text-slate-400 max-w-xs leading-relaxed mb-5">
        {description}
      </p>

      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#2D6A4F] hover:bg-[#40916c] text-white text-xs font-semibold transition-colors"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
