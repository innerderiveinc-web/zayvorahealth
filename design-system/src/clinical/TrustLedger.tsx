import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface TrustLedgerProps {
  merkleRoot: string;
  sha256Seal: string;
  timestamp: string;
  clinicianRegistration: string;
  status: 'COMMITTED' | 'PENDING' | 'TAMPER_DETECTED';
  onVerifyProof?: () => void;
  className?: string;
}

export const TrustLedger: React.FC<TrustLedgerProps> = ({
  merkleRoot,
  sha256Seal,
  timestamp,
  clinicianRegistration,
  status,
  onVerifyProof,
  className = '',
}) => {
  const statusConfig = {
    COMMITTED: { label: 'Cryptographically Sealed (21 CFR Pt 11)', bg: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30' },
    PENDING: { label: 'Pending Signature Anchoring', bg: 'bg-amber-500/10 text-amber-700 border-amber-500/30' },
    TAMPER_DETECTED: { label: 'ALERT: HASH MISMATCH', bg: 'bg-rose-500/10 text-rose-700 border-rose-500/30' },
  }[status];

  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-2.5 text-xs', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2">
        <span className="font-bold text-stone-900 dark:text-stone-100 flex items-center gap-1.5">
          <svg className="w-4 h-4 text-[#2D6A4F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          Trust & Audit Ledger
        </span>
        <span className={twMerge('px-2 py-0.5 text-[10px] font-bold rounded border uppercase', statusConfig.bg)}>
          {statusConfig.label}
        </span>
      </div>

      <div className="space-y-1.5 font-mono text-[11px] bg-stone-50 dark:bg-stone-950 p-2.5 rounded-lg text-stone-600 dark:text-stone-400">
        <div className="truncate">
          <span className="font-bold text-stone-700 dark:text-stone-300">Merkle Root: </span>
          <span>{merkleRoot}</span>
        </div>
        <div className="truncate">
          <span className="font-bold text-stone-700 dark:text-stone-300">Seal Hash: </span>
          <span>{sha256Seal}</span>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-stone-200 dark:border-stone-800 font-sans text-xs">
          <span>Lic: <span className="font-semibold text-stone-800 dark:text-stone-200">{clinicianRegistration}</span></span>
          <span>Timestamp: {timestamp}</span>
        </div>
      </div>

      {onVerifyProof && (
        <button
          type="button"
          onClick={onVerifyProof}
          className="w-full py-1 text-[11px] font-semibold text-[#2D6A4F] hover:bg-emerald-50 dark:hover:bg-emerald-950/20 rounded border border-emerald-500/20 transition"
        >
          Verify Merkle Proof Chain
        </button>
      )}
    </div>
  );
};
