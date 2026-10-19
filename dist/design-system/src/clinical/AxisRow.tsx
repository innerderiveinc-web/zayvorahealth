import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface AxisRowProps {
  axisName: string;
  subName: string;
  score: number; // 0 - 10
  status: 'OPTIMAL' | 'MILD_VULNERABILITY' | 'MODERATE_DYSFUNCTION' | 'CRITICAL_IMBALANCE';
  imbalanceIndicators?: string[];
  onClick?: () => void;
  className?: string;
}

export const AxisRow: React.FC<AxisRowProps> = ({
  axisName,
  subName,
  score,
  status,
  imbalanceIndicators = [],
  onClick,
  className = '',
}) => {
  const statusConfig = {
    OPTIMAL: { label: 'Optimal', bg: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30', bar: 'bg-emerald-500' },
    MILD_VULNERABILITY: { label: 'Mild Vulnerability', bg: 'bg-teal-500/10 text-teal-700 border-teal-500/30', bar: 'bg-teal-500' },
    MODERATE_DYSFUNCTION: { label: 'Moderate Dysfunction', bg: 'bg-amber-500/10 text-amber-700 border-amber-500/30', bar: 'bg-amber-500' },
    CRITICAL_IMBALANCE: { label: 'Critical Imbalance', bg: 'bg-rose-500/10 text-rose-700 border-rose-500/30', bar: 'bg-rose-500' },
  }[status];

  return (
    <div
      onClick={onClick}
      className={twMerge(
        'p-3 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-lg transition',
        onClick ? 'cursor-pointer hover:border-stone-400 dark:hover:border-stone-600' : '',
        className
      )}
    >
      <div className="flex flex-wrap items-center justify-between gap-2 mb-1.5">
        <div>
          <span className="text-xs font-bold text-stone-900 dark:text-stone-100">{axisName}</span>
          <span className="text-[11px] text-stone-400 ml-1.5">({subName})</span>
        </div>
        <div className="flex items-center gap-2">
          <span className={twMerge('px-2 py-0.5 text-[10px] font-bold rounded border uppercase', statusConfig.bg)}>
            {statusConfig.label}
          </span>
          <span className="text-xs font-mono font-bold text-stone-700 dark:text-stone-300">
            {score}/10
          </span>
        </div>
      </div>

      <div className="w-full bg-stone-100 dark:bg-stone-800 rounded-full h-1.5 mb-2 overflow-hidden">
        <div
          className={twMerge('h-full transition-all duration-300', statusConfig.bar)}
          style={{ width: `${(score / 10) * 100}%` }}
        />
      </div>

      {imbalanceIndicators.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-1">
          {imbalanceIndicators.map((ind, i) => (
            <span key={i} className="text-[10px] bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-400 px-1.5 py-0.5 rounded">
              • {ind}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};
