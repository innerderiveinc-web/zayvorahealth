import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface ErrorStateProps {
  title?: string;
  message?: string;
  code?: string;
  correlationId?: string;
  onRetry?: () => void;
  actionLabel?: string;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Clinical Operation Interrupted',
  message = 'An unexpected system condition occurred while evaluating clinical records. Safe fail-closed posture maintained.',
  code,
  correlationId,
  onRetry,
  actionLabel = 'Retry Verification',
  className = '',
}) => {
  return (
    <div className={twMerge('flex flex-col items-center justify-center p-8 text-center bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl', className)}>
      <div className="w-12 h-12 rounded-full bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400 flex items-center justify-center mb-4">
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>

      <h3 className="text-sm font-semibold text-stone-900 dark:text-stone-100 mb-1">
        {title}
      </h3>
      <p className="text-xs text-stone-600 dark:text-stone-400 max-w-md mb-4 leading-relaxed">
        {message}
      </p>

      {(code || correlationId) && (
        <div className="flex items-center gap-3 text-[10px] font-mono text-stone-500 mb-4 bg-white dark:bg-stone-900 px-3 py-1.5 rounded border border-stone-200 dark:border-stone-800">
          {code && <span>ERR_CODE: {code}</span>}
          {code && correlationId && <span>•</span>}
          {correlationId && <span>CID: {correlationId}</span>}
        </div>
      )}

      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-medium rounded-lg text-white bg-rose-700 hover:bg-rose-800 transition"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{actionLabel}</span>
        </button>
      )}
    </div>
  );
};
