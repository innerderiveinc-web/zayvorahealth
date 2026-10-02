import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface SignatureSummaryProps {
  signerName: string;
  registrationNumber: string;
  signedAt: string;
  sha256Seal: string;
  merkleRoot?: string;
  verificationUrl?: string;
  className?: string;
}

export const SignatureSummary: React.FC<SignatureSummaryProps> = ({
  signerName,
  registrationNumber,
  signedAt,
  sha256Seal,
  merkleRoot,
  verificationUrl,
  className = '',
}) => {
  return (
    <div className={twMerge('p-4 bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-500/30 rounded-xl space-y-2.5 text-xs', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-emerald-500/20 pb-2">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold">
            ✓
          </div>
          <span className="font-bold text-emerald-900 dark:text-emerald-200">
            21 CFR Part 11 Digital Signature Seal Verified
          </span>
        </div>
        <span className="px-2 py-0.5 rounded bg-emerald-600 text-white font-mono text-[10px] font-bold">
          CRYPTOGRAPHICALLY SEALED
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-stone-700 dark:text-stone-300">
        <div>
          Signer: <span className="font-semibold text-stone-900 dark:text-stone-100">{signerName}</span>
        </div>
        <div>
          License: <span className="font-mono font-semibold">{registrationNumber}</span>
        </div>
        <div>
          Timestamp: <span className="font-mono">{signedAt}</span>
        </div>
        {merkleRoot && (
          <div className="truncate font-mono text-[10px] text-stone-500">
            Merkle: {merkleRoot}
          </div>
        )}
      </div>

      <div className="p-2 rounded bg-white dark:bg-stone-900 border border-emerald-500/20 font-mono text-[10px] text-stone-600 dark:text-stone-400 break-all">
        <span className="font-bold text-emerald-800 dark:text-emerald-400">SHA-256 Seal: </span>
        {sha256Seal}
      </div>

      {verificationUrl && (
        <div className="pt-1 text-right">
          <a
            href={verificationUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[11px] font-semibold text-[#2D6A4F] hover:underline"
          >
            Inspect Merkle Chain Audit Certificate ↗
          </a>
        </div>
      )}
    </div>
  );
};
