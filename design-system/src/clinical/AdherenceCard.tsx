import React from 'react';
import { twMerge } from 'tailwind-merge';

export type AdherenceStatus = 'TAKEN' | 'PENDING' | 'SKIPPED';

export interface AdherenceItem {
  id: string;
  slot: 'Morning' | 'Afternoon' | 'Evening' | 'Bedtime';
  timeLabel: string;
  medicineName: string;
  dosageInstructions: string;
  status: AdherenceStatus;
}

export interface AdherenceCardProps {
  item: AdherenceItem;
  onUpdateStatus: (id: string, status: AdherenceStatus) => void;
  className?: string;
}

export const AdherenceCard: React.FC<AdherenceCardProps> = ({
  item,
  onUpdateStatus,
  className = '',
}) => {
  return (
    <div className={twMerge('p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-2 text-xs shadow-sm', className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-teal-500/10 text-teal-700 dark:text-teal-400 font-bold text-[10px] uppercase">
            {item.slot} • {item.timeLabel}
          </span>
          <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
            {item.medicineName}
          </span>
        </div>

        <span
          className={twMerge(
            'px-2 py-0.5 rounded text-[10px] font-bold uppercase',
            item.status === 'TAKEN'
              ? 'bg-emerald-500/10 text-emerald-600 border border-emerald-500/30'
              : item.status === 'SKIPPED'
              ? 'bg-rose-500/10 text-rose-600 border border-rose-500/30'
              : 'bg-amber-500/10 text-amber-600 border border-amber-500/30'
          )}
        >
          {item.status === 'TAKEN' ? '✓ Taken' : item.status === 'SKIPPED' ? '✕ Skipped' : '⏳ Not Yet'}
        </span>
      </div>

      <p className="text-stone-600 dark:text-stone-400 text-xs">
        {item.dosageInstructions}
      </p>

      <div className="flex items-center gap-2 pt-1">
        <button
          type="button"
          onClick={() => onUpdateStatus(item.id, 'TAKEN')}
          className={twMerge(
            'flex-1 py-1.5 rounded-lg font-semibold text-xs transition border',
            item.status === 'TAKEN'
              ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm'
              : 'bg-stone-50 dark:bg-stone-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/30 text-stone-700 dark:text-stone-300 border-stone-200 dark:border-stone-700'
          )}
        >
          ✓ Yes, Taken
        </button>
        <button
          type="button"
          onClick={() => onUpdateStatus(item.id, 'PENDING')}
          className={twMerge(
            'px-3 py-1.5 rounded-lg font-medium text-xs transition border',
            item.status === 'PENDING'
              ? 'bg-amber-500 text-black border-amber-500 font-semibold'
              : 'bg-stone-50 dark:bg-stone-800 hover:bg-amber-50 dark:hover:bg-amber-950/30 text-stone-600 dark:text-stone-400 border-stone-200 dark:border-stone-700'
          )}
        >
          ⏳ Not Yet
        </button>
        <button
          type="button"
          onClick={() => onUpdateStatus(item.id, 'SKIPPED')}
          className={twMerge(
            'px-3 py-1.5 rounded-lg font-medium text-xs transition border',
            item.status === 'SKIPPED'
              ? 'bg-rose-600 text-white border-rose-600 font-semibold'
              : 'bg-stone-50 dark:bg-stone-800 hover:bg-rose-50 dark:hover:bg-rose-950/30 text-stone-600 dark:text-stone-400 border-stone-200 dark:border-stone-700'
          )}
        >
          ✕ Skipped
        </button>
      </div>
    </div>
  );
};
