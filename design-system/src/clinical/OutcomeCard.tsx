import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface OutcomeMetric {
  name: string;
  baseline: number;
  current: number;
  unit?: string;
  improved: boolean;
}

export interface OutcomeCardProps {
  scaleName: string;
  category: string;
  assessedDate: string;
  metrics: OutcomeMetric[];
  clinicianComment?: string;
  className?: string;
}

export const OutcomeCard: React.FC<OutcomeCardProps> = ({
  scaleName,
  category,
  assessedDate,
  metrics,
  clinicianComment,
  className = '',
}) => {
  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-3 text-xs', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2">
        <div>
          <h4 className="font-bold text-stone-900 dark:text-stone-100">{scaleName}</h4>
          <span className="text-[10px] text-stone-400">{category} • Assessed: {assessedDate}</span>
        </div>
        <span className="px-2 py-0.5 rounded bg-teal-500/10 text-teal-700 dark:text-teal-400 border border-teal-500/30 text-[10px] font-semibold">
          Validated Clinical PROM
        </span>
      </div>

      <div className="space-y-2">
        {metrics.map((m, idx) => {
          const delta = m.current - m.baseline;
          const sign = delta > 0 ? '+' : '';

          return (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-stone-50 dark:bg-stone-950/60 flex items-center justify-between"
            >
              <span className="font-medium text-stone-700 dark:text-stone-300">{m.name}</span>
              <div className="flex items-center gap-3 font-mono">
                <span className="text-stone-400 text-[11px]">
                  Baseline: {m.baseline} {m.unit || ''}
                </span>
                <span className="text-stone-900 dark:text-stone-100 font-bold">
                  Now: {m.current} {m.unit || ''}
                </span>
                <span className={twMerge('px-1.5 py-0.2 rounded text-[10px] font-bold', m.improved ? 'bg-emerald-500/10 text-emerald-600' : 'bg-rose-500/10 text-rose-600')}>
                  {sign}{delta} {m.improved ? '(Improved)' : '(Worsened)'}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {clinicianComment && (
        <div className="p-2.5 rounded bg-stone-50 dark:bg-stone-950 text-[11px] text-stone-600 dark:text-stone-400">
          <strong className="text-stone-800 dark:text-stone-200">Clinician Note: </strong>
          {clinicianComment}
        </div>
      )}
    </div>
  );
};
