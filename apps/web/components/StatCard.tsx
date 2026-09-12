import React from "react";

interface StatCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  badge?: string;
  variant?: "teal" | "emerald" | "amber" | "rose" | "blue" | "purple";
  icon?: string;
}

export function StatCard({
  label,
  value,
  subtext,
  badge,
  variant = "teal",
  icon,
}: StatCardProps) {
  const borderColors = {
    teal: "border-[#0D9488]/40 hover:border-[#0D9488]",
    emerald: "border-[#10B981]/40 hover:border-[#10B981]",
    amber: "border-[#F59E0B]/40 hover:border-[#F59E0B]",
    rose: "border-[#EF4444]/40 hover:border-[#EF4444]",
    blue: "border-[#3B82F6]/40 hover:border-[#3B82F6]",
    purple: "border-[#8B5CF6]/40 hover:border-[#8B5CF6]",
  };

  const badgeStyles = {
    teal: "bg-[#0D9488]/20 text-[#2DD4BF]",
    emerald: "bg-[#10B981]/20 text-[#34D399]",
    amber: "bg-[#F59E0B]/20 text-[#FBBF24]",
    rose: "bg-[#EF4444]/20 text-[#FB7185]",
    blue: "bg-[#3B82F6]/20 text-[#60A5FA]",
    purple: "bg-[#8B5CF6]/20 text-[#C084FC]",
  };

  return (
    <div className={`zv-card p-4 transition-all duration-150 ${borderColors[variant]}`}>
      <div className="flex items-center justify-between gap-2 mb-2">
        <span className="text-xs font-medium text-[#94A3B8]">{label}</span>
        {icon && <span className="text-sm">{icon}</span>}
      </div>
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-xl font-bold tracking-tight text-white font-mono">{value}</span>
        {badge && (
          <span className={`text-[10px] px-2 py-0.5 rounded font-semibold ${badgeStyles[variant]}`}>
            {badge}
          </span>
        )}
      </div>
      {subtext && <p className="text-[11px] text-[#64748B] mt-1.5">{subtext}</p>}
    </div>
  );
}
