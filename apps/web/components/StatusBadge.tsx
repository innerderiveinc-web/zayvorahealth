import React from "react";

export type StatusVariant = 
  | "verified"
  | "pending"
  | "urgent"
  | "neutral"
  | "research"
  | "locked";

interface StatusBadgeProps {
  status: string;
  variant?: StatusVariant;
  pulse?: boolean;
}

export function StatusBadge({
  status,
  variant = "neutral",
  pulse = false,
}: StatusBadgeProps) {
  const styles: Record<StatusVariant, { badge: string; dot: string }> = {
    verified: {
      badge: "zv-badge-emerald",
      dot: "bg-[#10B981]",
    },
    pending: {
      badge: "zv-badge-amber",
      dot: "bg-[#F59E0B]",
    },
    urgent: {
      badge: "zv-badge-rose",
      dot: "bg-[#EF4444]",
    },
    neutral: {
      badge: "zv-badge-blue",
      dot: "bg-[#3B82F6]",
    },
    research: {
      badge: "zv-badge-purple",
      dot: "bg-[#8B5CF6]",
    },
    locked: {
      badge: "zv-badge-teal",
      dot: "bg-[#0D9488]",
    },
  };

  const selected = styles[variant] || styles.neutral;

  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase ${selected.badge}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${selected.dot} ${pulse ? "animate-ping" : ""}`} />
      <span>{status}</span>
    </span>
  );
}
