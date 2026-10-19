import React from 'react';
import { twMerge } from 'tailwind-merge';

export type KnowledgeTier = 'TIER_1_CLASSICAL' | 'TIER_2_PHARMACOPOEIA' | 'TIER_3_MODERN_RWE';

export interface KnowledgeProvenanceProps {
  tier: KnowledgeTier;
  substanceName: string;
  canonTitle: string;
  volumeFolio: string;
  governanceStage: number; // 1 - 12
  isClinicalApproved: boolean;
  expertVerifier?: string;
  className?: string;
}

export const KnowledgeProvenance: React.FC<KnowledgeProvenanceProps> = ({
  tier,
  substanceName,
  canonTitle,
  volumeFolio,
  governanceStage,
  isClinicalApproved,
  expertVerifier,
  className = '',
}) => {
  const tierConfig = {
    TIER_1_CLASSICAL: { label: 'Tier 1: Classical Canon (Al-Qanun / Kamil al-Sina)', bg: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30' },
    TIER_2_PHARMACOPOEIA: { label: 'Tier 2: National Pharmacopoeia (UPI / NFUM)', bg: 'bg-teal-500/10 text-teal-700 border-teal-500/30' },
    TIER_3_MODERN_RWE: { label: 'Tier 3: Modern RWE & Controlled Trials', bg: 'bg-sky-500/10 text-sky-700 border-sky-500/30' },
  }[tier];

  return (
    <div className={twMerge('p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-2 text-xs', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="font-bold text-stone-900 dark:text-stone-100">{substanceName}</span>
        <span className={twMerge('px-2 py-0.5 text-[10px] font-bold rounded border uppercase', isClinicalApproved ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/30' : 'bg-amber-500/10 text-amber-600 border-amber-500/30')}>
          {isClinicalApproved ? 'CLINICAL APPROVED • STAGE 12/12' : `RESEARCH CANDIDATE • STAGE ${String(governanceStage).padStart(2, '0')}/12`}
        </span>
      </div>

      <div className={twMerge('p-2 rounded font-medium text-[11px] border', tierConfig.bg)}>
        {tierConfig.label}
      </div>

      <div className="flex items-center justify-between text-[11px] text-stone-500 pt-1">
        <span>Anchor: <span className="font-semibold text-stone-700 dark:text-stone-300">{canonTitle}</span> ({volumeFolio})</span>
        {expertVerifier && <span>Verified: {expertVerifier}</span>}
      </div>

      {!isClinicalApproved && (
        <div className="p-2 bg-amber-500/10 border border-amber-500/20 rounded text-[11px] text-amber-800 dark:text-amber-300 font-semibold">
          AI PRESCRIBING BLOCKED: Substance pending multi-expert consensus review in stage 10-12.
        </div>
      )}
    </div>
  );
};
