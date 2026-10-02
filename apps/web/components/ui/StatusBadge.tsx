/**
 * @file StatusBadge.tsx
 * @description Generic status badge for admin console and shared UI.
 * Supports green/red/yellow/blue/purple variants with optional pulse animation.
 */
import React from "react";

export type BadgeVariant =
  | "success"
  | "danger"
  | "warning"
  | "info"
  | "neutral"
  | "purple";

interface StatusBadgeProps {
  /** Display label inside the badge */
  label: string;
  /** Color variant */
  variant?: BadgeVariant;
  /** Whether to animate the dot with a pulse */
  pulse?: boolean;
  /** Additional Tailwind classes */
  className?: string;
}

const VARIANT_STYLES: Record<
  BadgeVariant,
  { wrapper: string; dot: string }
> = {
  success: {
    wrapper: "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30",
    dot: "bg-emerald-400",
  },
  danger: {
    wrapper: "bg-red-500/15 text-red-400 border border-red-500/30",
    dot: "bg-red-400",
  },
  warning: {
    wrapper: "bg-amber-500/15 text-amber-400 border border-amber-500/30",
    dot: "bg-amber-400",
  },
  info: {
    wrapper: "bg-blue-500/15 text-blue-400 border border-blue-500/30",
    dot: "bg-blue-400",
  },
  neutral: {
    wrapper: "bg-slate-500/15 text-slate-400 border border-slate-500/30",
    dot: "bg-slate-400",
  },
  purple: {
    wrapper: "bg-purple-500/15 text-purple-400 border border-purple-500/30",
    dot: "bg-purple-400",
  },
};

/**
 * StatusBadge – compact pill badge with a coloured status dot.
 */
export function StatusBadge({
  label,
  variant = "neutral",
  pulse = false,
  className = "",
}: StatusBadgeProps) {
  const { wrapper, dot } = VARIANT_STYLES[variant];

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase select-none ${wrapper} ${className}`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full shrink-0 ${dot} ${
          pulse ? "animate-ping" : ""
        }`}
        aria-hidden="true"
      />
      {label}
    </span>
  );
}
