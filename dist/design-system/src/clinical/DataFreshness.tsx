import React from 'react';
import { twMerge } from 'tailwind-merge';

export type FreshnessState = 'REALTIME' | 'CACHED' | 'STALE' | 'INSUFFICIENT_DATA';

export interface DataFreshnessProps {
  state: FreshnessState;
  timestamp?: string;
  source?: string;
  onRefresh?: () => void;
  className?: string;
}

export const DataFreshness: React.FC<DataFreshnessProps> = ({
  state,
  timestamp,
  source,
  onRefresh,
  className = '',
}) => {
  const stateConfig = {
    REALTIME: {
      label: 'Real-time Live Feed',
      bg: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/30',
      dot: 'bg-emerald-500 animate-pulse',
    },
    CACHED: {
      label: 'Cached Record',
      bg: 'bg-teal-500/10 text-teal-700 dark:text-teal-400 border-teal-500/30',
      dot: 'bg-teal-500',
    },
    STALE: {
      label: 'Stale (>24h)',
      bg: 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/30',
      dot: 'bg-amber-500',
    },
    INSUFFICIENT_DATA: {
      label: 'Insufficient Data / Unassessed',
      bg: 'bg-stone-500/10 text-stone-700 dark:text-stone-400 border-stone-500/30',
      dot: 'bg-stone-400',
    },
  }[state];

  return (
    <div className={twMerge('inline-flex items-center gap-2 px-2.5 py-1 rounded-md border text-xs', stateConfig.bg, className)}>
      <span className={twMerge('w-2 h-2 rounded-full', stateConfig.dot)} />
      <span className="font-semibold">{stateConfig.label}</span>
      {timestamp && (
        <span className="text-[10px] opacity-75 font-mono">({timestamp})</span>
      )}
      {source && (
        <span className="text-[10px] opacity-75">via {source}</span>
      )}
      {onRefresh && (
        <button
          type="button"
          onClick={onRefresh}
          className="ml-1 text-[10px] underline hover:opacity-80"
        >
          Refresh
        </button>
      )}
    </div>
  );
};
