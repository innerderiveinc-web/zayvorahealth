import React, { useState } from 'react';
import { twMerge } from 'tailwind-merge';

export interface ApprovalPanelProps {
  clinicianName: string;
  registrationNumber: string;
  onApprove: (pin: string, reason: string) => void;
  onReject?: (reason: string) => void;
  disabled?: boolean;
  disabledReason?: string;
  isProcessing?: boolean;
  className?: string;
}

export const ApprovalPanel: React.FC<ApprovalPanelProps> = ({
  clinicianName,
  registrationNumber,
  onApprove,
  onReject,
  disabled = false,
  disabledReason,
  isProcessing = false,
  className = '',
}) => {
  const [pin, setPin] = useState('');
  const [reason, setReason] = useState('Authorized Unani clinical encounter order');
  const [confirmed, setConfirmed] = useState(false);

  const canApprove = !disabled && confirmed && pin.length >= 4;

  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-3 text-xs', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2">
        <div>
          <h4 className="font-bold text-stone-900 dark:text-stone-100">
            21 CFR Part 11 Electronic Signature Authority
          </h4>
          <span className="text-[10px] text-stone-500">
            Signer: {clinicianName} (Reg #{registrationNumber})
          </span>
        </div>
        <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 border border-emerald-500/30 text-[10px] font-bold uppercase">
          Statutory Verified
        </span>
      </div>

      {disabled && disabledReason && (
        <div className="p-2.5 rounded bg-rose-500/10 border border-rose-500/30 text-rose-700 dark:text-rose-300 font-medium">
          Approval Barrier: {disabledReason}
        </div>
      )}

      <div className="space-y-2">
        <label className="flex items-start gap-2 cursor-pointer select-none text-stone-600 dark:text-stone-300">
          <input
            type="checkbox"
            checked={confirmed}
            onChange={(e) => setConfirmed(e.target.checked)}
            disabled={disabled}
            className="mt-0.5 rounded text-[#2D6A4F] focus:ring-[#2D6A4F]"
          />
          <span className="text-[11px] leading-tight">
            I certify that this electronic order represents my clinical judgement, and my electronic signature is the legally binding equivalent of my handwritten signature under statutory healthcare law.
          </span>
        </label>

        <div className="flex flex-wrap items-end gap-3">
          <div className="flex-1 min-w-[140px]">
            <label className="block text-[11px] font-semibold text-stone-700 dark:text-stone-300 mb-1">
              Signing PIN:
            </label>
            <input
              type="password"
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              disabled={disabled}
              maxLength={8}
              placeholder="••••"
              className="w-full px-3 py-1.5 text-xs font-mono border border-stone-300 dark:border-stone-700 rounded-lg bg-stone-50 dark:bg-stone-950 focus:ring-2 focus:ring-[#2D6A4F] focus:outline-none"
            />
          </div>

          <button
            type="button"
            disabled={!canApprove || isProcessing}
            onClick={() => onApprove(pin, reason)}
            className="px-4 py-2 text-xs font-bold rounded-lg text-white bg-[#2D6A4F] hover:bg-[#255840] disabled:opacity-50 disabled:cursor-not-allowed shadow transition"
          >
            {isProcessing ? 'Executing Cryptographic Seal...' : 'Sign & Seal Order'}
          </button>
        </div>
      </div>
    </div>
  );
};
