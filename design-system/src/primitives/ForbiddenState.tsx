import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface ForbiddenStateProps {
  requiredRole?: string;
  currentRole?: string;
  scopeRestriction?: string;
  onGoBack?: () => void;
  className?: string;
}

export const ForbiddenState: React.FC<ForbiddenStateProps> = ({
  requiredRole = 'Licensed Clinician (Doctor / Hakeem)',
  currentRole = 'Unverified Identity',
  scopeRestriction = 'Prescription signing and clinical authorization are strictly reserved for licensed practitioners under statutory healthcare guidelines.',
  onGoBack,
  className = '',
}) => {
  return (
    <div className={twMerge('flex flex-col items-center justify-center p-8 text-center bg-stone-50 dark:bg-stone-900/50 border border-stone-200 dark:border-stone-800 rounded-xl', className)}>
      <div className="w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-950/50 text-amber-700 dark:text-amber-400 flex items-center justify-center mb-4">
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      </div>

      <h3 className="text-base font-semibold text-stone-900 dark:text-stone-100 mb-1">
        Statutory Access Boundary
      </h3>
      <p className="text-xs text-stone-600 dark:text-stone-400 max-w-md mb-4 leading-relaxed">
        {scopeRestriction}
      </p>

      <div className="flex flex-col sm:flex-row items-center gap-2 text-xs mb-6 text-stone-600 dark:text-stone-400">
        <div className="px-2.5 py-1 rounded bg-stone-200 dark:bg-stone-800 font-mono text-[11px]">
          Required: <span className="font-semibold text-stone-900 dark:text-stone-100">{requiredRole}</span>
        </div>
        <span className="hidden sm:inline">→</span>
        <div className="px-2.5 py-1 rounded bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300 font-mono text-[11px]">
          Current: <span className="font-semibold">{currentRole}</span>
        </div>
      </div>

      {onGoBack && (
        <button
          type="button"
          onClick={onGoBack}
          className="px-4 py-2 text-xs font-semibold rounded-lg bg-stone-800 hover:bg-stone-900 text-white transition"
        >
          Return to Permitted Workspace
        </button>
      )}
    </div>
  );
};
