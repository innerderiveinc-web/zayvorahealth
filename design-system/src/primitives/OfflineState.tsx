import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface OfflineStateProps {
  pendingMutationsCount?: number;
  lastSyncedAt?: string;
  onSyncNow?: () => void;
  isSyncing?: boolean;
  className?: string;
}

export const OfflineState: React.FC<OfflineStateProps> = ({
  pendingMutationsCount = 0,
  lastSyncedAt,
  onSyncNow,
  isSyncing = false,
  className = '',
}) => {
  return (
    <div
      role="alert"
      className={twMerge(
        'flex items-center justify-between p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-900 dark:text-amber-200 text-xs',
        className
      )}
    >
      <div className="flex items-center gap-2.5">
        <span className="relative flex h-2.5 w-2.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500" />
        </span>
        <div>
          <span className="font-semibold">Local Offline Cache Active:</span>{' '}
          <span>Read access available via local SQLite.</span>
          {pendingMutationsCount > 0 && (
            <span className="ml-1 text-amber-700 dark:text-amber-400 font-medium">
              ({pendingMutationsCount} clinical writes queued for encrypted synchronization)
            </span>
          )}
          {lastSyncedAt && (
            <span className="ml-2 text-[10px] text-stone-500">
              Last synced: {lastSyncedAt}
            </span>
          )}
        </div>
      </div>

      {onSyncNow && (
        <button
          type="button"
          onClick={onSyncNow}
          disabled={isSyncing}
          className="px-2.5 py-1 text-xs font-semibold rounded bg-amber-600 hover:bg-amber-700 text-white disabled:opacity-50 transition"
        >
          {isSyncing ? 'Syncing...' : 'Sync Now'}
        </button>
      )}
    </div>
  );
};
