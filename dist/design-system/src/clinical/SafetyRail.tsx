import React from 'react';
import { twMerge } from 'tailwind-merge';

export type SafetyRailStatus = 'PASS' | 'CAUTION' | 'BLOCK' | 'UNKNOWN';

export interface SafetyCheck {
  id: string;
  name: string;
  status: SafetyRailStatus;
  detail: string;
  actionRequired?: string;
}

export interface SafetyRailProps {
  checks: SafetyCheck[];
  overallStatus: SafetyRailStatus;
  onReevaluate?: () => void;
  onResolveCaution?: (checkId: string) => void;
  className?: string;
}

export const SafetyRail: React.FC<SafetyRailProps> = ({
  checks,
  overallStatus,
  onReevaluate,
  onResolveCaution,
  className = '',
}) => {
  const overallConfig = {
    PASS: { label: 'ALL RAILS CLEAR', bg: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/30' },
    CAUTION: { label: 'CAUTION: JUSTIFICATION REQ', bg: 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/30' },
    BLOCK: { label: 'HARD BLOCK ENFORCED', bg: 'bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/30' },
    UNKNOWN: { label: 'PENDING SAFETY EVAL', bg: 'bg-stone-500/10 text-stone-700 dark:text-stone-400 border-stone-500/30' },
  }[overallStatus];

  const checkBadgeClasses: Record<SafetyRailStatus, string> = {
    PASS: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/30',
    CAUTION: 'bg-amber-500/10 text-amber-600 border-amber-500/30',
    BLOCK: 'bg-rose-500/10 text-rose-600 border-rose-500/30',
    UNKNOWN: 'bg-stone-500/10 text-stone-600 border-stone-500/30',
  };

  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-3', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2.5">
        <div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#2D6A4F] animate-pulse" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-stone-900 dark:text-stone-100">
              Permanent Safety Rail (Fail-Closed)
            </h4>
          </div>
          <span className="text-[10px] text-stone-400">Zero-bypass deterministic clinical verification</span>
        </div>
        <span className={twMerge('px-2 py-0.5 text-[10px] font-bold rounded border uppercase', overallConfig.bg)}>
          {overallConfig.label}
        </span>
      </div>

      <div className="space-y-2">
        {checks.map((check) => (
          <div
            key={check.id}
            className="p-2.5 rounded-lg bg-stone-50 dark:bg-stone-950/50 border border-stone-200/60 dark:border-stone-800/60 flex items-start justify-between gap-2"
          >
            <div className="flex-1 text-xs">
              <div className="flex items-center gap-2 mb-0.5">
                <span className="font-semibold text-stone-800 dark:text-stone-200">{check.name}</span>
                <span className={twMerge('px-1.5 py-0.2 text-[9px] font-bold rounded border uppercase', checkBadgeClasses[check.status])}>
                  {check.status}
                </span>
              </div>
              <p className="text-[11px] text-stone-500">{check.detail}</p>
              {check.actionRequired && (
                <div className="mt-1 text-[10px] font-medium text-amber-700 dark:text-amber-400">
                  Required: {check.actionRequired}
                </div>
              )}
            </div>
            {check.status === 'CAUTION' && onResolveCaution && (
              <button
                type="button"
                onClick={() => onResolveCaution(check.id)}
                className="px-2 py-1 text-[10px] font-semibold text-amber-800 bg-amber-100 hover:bg-amber-200 rounded border border-amber-300 transition"
              >
                Resolve
              </button>
            )}
          </div>
        ))}
      </div>

      {onReevaluate && (
        <button
          type="button"
          onClick={onReevaluate}
          className="w-full py-1.5 text-xs font-medium text-stone-600 dark:text-stone-300 bg-stone-100 dark:bg-stone-800 hover:bg-stone-200 dark:hover:bg-stone-700 rounded-lg transition"
        >
          Re-evaluate Safety Rails
        </button>
      )}
    </div>
  );
};
