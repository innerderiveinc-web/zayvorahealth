import React from 'react';
import { twMerge } from 'tailwind-merge';

export type ConsentLevel = 'ACTIVE' | 'PENDING' | 'EXPIRED' | 'EMERGENCY_OVERRIDE';

export interface ConsentStatusProps {
  status: ConsentLevel;
  consentedScope?: string[];
  expiresAt?: string;
  patientSigned?: boolean;
  onRequestConsent?: () => void;
  className?: string;
}

export const ConsentStatus: React.FC<ConsentStatusProps> = ({
  status,
  consentedScope = ['CLINICAL_TREATMENT', 'ELECTRONIC_HEALTH_RECORDS'],
  expiresAt,
  patientSigned = true,
  onRequestConsent,
  className = '',
}) => {
  const config = {
    ACTIVE: {
      label: 'Informed Consent Active',
      bg: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/30',
      tag: 'bg-emerald-600 text-white',
    },
    PENDING: {
      label: 'Consent Pending Signature',
      bg: 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/30',
      tag: 'bg-amber-600 text-white',
    },
    EXPIRED: {
      label: 'Statutory Consent Expired',
      bg: 'bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/30',
      tag: 'bg-rose-600 text-white',
    },
    EMERGENCY_OVERRIDE: {
      label: 'Emergency Care Waiver Active',
      bg: 'bg-purple-500/10 text-purple-700 dark:text-purple-400 border-purple-500/30',
      tag: 'bg-purple-600 text-white',
    },
  }[status];

  return (
    <div className={twMerge('p-3.5 bg-white dark:bg-stone-900 border rounded-xl text-xs space-y-2', config.bg, className)}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className={twMerge('px-2 py-0.5 text-[10px] font-bold rounded uppercase', config.tag)}>
            {status}
          </span>
          <span className="font-bold text-stone-900 dark:text-stone-100">
            {config.label}
          </span>
        </div>
        {expiresAt && (
          <span className="text-[11px] text-stone-500 font-mono">
            Valid until: {expiresAt}
          </span>
        )}
      </div>

      <div className="text-[11px] text-stone-600 dark:text-stone-400">
        Scope: {consentedScope.join(' • ')}
      </div>

      {status !== 'ACTIVE' && onRequestConsent && (
        <div className="pt-1">
          <button
            type="button"
            onClick={onRequestConsent}
            className="px-2.5 py-1 text-xs font-semibold rounded bg-[#2D6A4F] text-white hover:bg-[#255840] transition"
          >
            Obtain Patient Digital Signature
          </button>
        </div>
      )}
    </div>
  );
};
