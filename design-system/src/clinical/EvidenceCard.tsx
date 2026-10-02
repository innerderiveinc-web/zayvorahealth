import React from 'react';
import { twMerge } from 'tailwind-merge';

export type GradeLevel = 'HIGH' | 'MODERATE' | 'LOW' | 'VERY_LOW';

export interface EvidenceCardProps {
  claim: string;
  substanceName: string;
  indication: string;
  sourceType: 'CLASSICAL_CANON' | 'PHARMACOPOEIA' | 'RCT' | 'META_ANALYSIS' | 'OBSERVATIONAL';
  sourceTitle: string;
  citation: string;
  gradeLevel: GradeLevel;
  reviewerName?: string;
  reviewDate?: string;
  limitations?: string;
  onOpenDrawer?: () => void;
  className?: string;
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({
  claim,
  substanceName,
  indication,
  sourceType,
  sourceTitle,
  citation,
  gradeLevel,
  reviewerName,
  reviewDate,
  limitations,
  onOpenDrawer,
  className = '',
}) => {
  const gradeStyles: Record<GradeLevel, { label: string; bg: string }> = {
    HIGH: { label: 'GRADE: High', bg: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30' },
    MODERATE: { label: 'GRADE: Moderate', bg: 'bg-teal-500/10 text-teal-700 border-teal-500/30' },
    LOW: { label: 'GRADE: Low', bg: 'bg-amber-500/10 text-amber-700 border-amber-500/30' },
    VERY_LOW: { label: 'GRADE: Very Low', bg: 'bg-rose-500/10 text-rose-700 border-rose-500/30' },
  };

  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-2.5 shadow-sm', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-[#2D6A4F]">{substanceName}</span>
          <span className="text-stone-400 text-xs">•</span>
          <span className="text-xs font-medium text-stone-600 dark:text-stone-400">{indication}</span>
        </div>
        <span className={twMerge('px-2 py-0.5 text-[10px] font-bold rounded border uppercase', gradeStyles[gradeLevel].bg)}>
          {gradeStyles[gradeLevel].label}
        </span>
      </div>

      <p className="text-xs font-medium text-stone-800 dark:text-stone-200 leading-relaxed">
        "{claim}"
      </p>

      <div className="text-[11px] text-stone-500 bg-stone-50 dark:bg-stone-950 p-2.5 rounded-lg space-y-1">
        <div>
          <span className="font-semibold text-stone-700 dark:text-stone-300">Source: </span>
          <span className="font-mono text-stone-600 dark:text-stone-400">{sourceTitle}</span> ({sourceType})
        </div>
        <div className="truncate">
          <span className="font-semibold text-stone-700 dark:text-stone-300">Citation: </span>
          <span className="italic">{citation}</span>
        </div>
      </div>

      {(reviewerName || limitations || onOpenDrawer) && (
        <div className="flex items-center justify-between pt-2 border-t border-stone-100 dark:border-stone-800 text-[11px]">
          <div className="text-stone-400">
            {reviewerName && <span>Certified by {reviewerName} {reviewDate ? `(${reviewDate})` : ''}</span>}
          </div>
          {onOpenDrawer && (
            <button
              type="button"
              onClick={onOpenDrawer}
              className="text-[#2D6A4F] hover:underline font-semibold"
            >
              Inspect 6-Point Provenance →
            </button>
          )}
        </div>
      )}
    </div>
  );
};
