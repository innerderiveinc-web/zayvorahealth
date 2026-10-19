import React from 'react';

export interface PrescriptionItemProps {
  name: string;
  dose: string;
  duration?: string;
  instructions?: string;
  isScheduleE1?: boolean;
  mudabbarCertified?: boolean;
  onAction?: () => void;
  actionLabel?: string;
  className?: string;
}

export const PrescriptionItem: React.FC<PrescriptionItemProps> = ({
  name,
  dose,
  duration,
  instructions,
  isScheduleE1,
  mudabbarCertified,
  onAction,
  actionLabel,
  className = '',
}) => {
  return (
    <div
      className={`p-4 rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${className}`}
    >
      <div className="space-y-1">
        <div className="flex flex-wrap items-center gap-2">
          <h4 className="font-semibold text-sm text-gray-900 dark:text-gray-100">{name}</h4>
          {isScheduleE1 && (
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-500 border border-amber-500/30">
              Schedule E(1)
            </span>
          )}
          {mudabbarCertified && (
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              ✓ Mudabbar Certified
            </span>
          )}
        </div>
        <p className="text-xs text-gray-600 dark:text-gray-300">
          <span className="font-medium text-brand-primary dark:text-emerald-400">{dose}</span>
          {duration && <span> • {duration}</span>}
        </p>
        {instructions && (
          <p className="text-[11px] text-gray-500 dark:text-gray-400 italic">“{instructions}”</p>
        )}
      </div>

      {onAction && actionLabel && (
        <button
          type="button"
          onClick={onAction}
          className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-brand-primary/10 text-brand-primary hover:bg-brand-primary hover:text-white dark:bg-emerald-500/10 dark:text-emerald-400 dark:hover:bg-emerald-600 dark:hover:text-white transition-all self-end sm:self-auto"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};
