import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface ClassicalCitation {
  source: string;
  canonRef: string;
  quote?: string;
}

export interface HakeemInsightProps {
  suggestion: string;
  reasoning: string;
  uncertaintyScore: number; // e.g. 0.08
  citations?: ClassicalCitation[];
  onAccept?: () => void;
  onDismiss?: () => void;
  className?: string;
}

export const HakeemInsight: React.FC<HakeemInsightProps> = ({
  suggestion,
  reasoning,
  uncertaintyScore,
  citations = [],
  onAccept,
  onDismiss,
  className = '',
}) => {
  const isHighConfidence = uncertaintyScore <= 0.15;

  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-teal-500/30 rounded-xl shadow-sm space-y-3', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-teal-600 text-white flex items-center justify-center text-xs font-bold font-mono">
            H
          </div>
          <div>
            <h4 className="text-xs font-bold text-stone-900 dark:text-stone-100">
              Hakeem Sahab AI™ — AI-Assisted Clinical Decision Support
            </h4>
            <span className="text-[10px] text-stone-400">Grounded in Unani classical corpus & modern trial synthesis</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={twMerge('px-2 py-0.5 text-[10px] font-mono font-bold rounded border', isHighConfidence ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/30' : 'bg-amber-500/10 text-amber-600 border-amber-500/30')}>
            Uncertainty: {uncertaintyScore.toFixed(2)} {isHighConfidence ? '(Low)' : '(Moderate)'}
          </span>
        </div>
      </div>

      <div className="text-xs">
        <div className="font-semibold text-[#2D6A4F] mb-1">Proposed Clinical Guidance:</div>
        <p className="text-stone-800 dark:text-stone-200 leading-relaxed font-medium">
          {suggestion}
        </p>
      </div>

      <div className="text-xs text-stone-600 dark:text-stone-400 bg-stone-50 dark:bg-stone-950 p-2.5 rounded-lg">
        <span className="font-semibold text-stone-700 dark:text-stone-300">Clinical Reasoning: </span>
        {reasoning}
      </div>

      {citations.length > 0 && (
        <div className="space-y-1">
          <span className="text-[10px] font-bold uppercase tracking-wider text-stone-400">Canonical Citations:</span>
          {citations.map((c, i) => (
            <div key={i} className="text-[11px] text-stone-500 font-mono">
              • <span className="font-semibold text-stone-700 dark:text-stone-300">{c.source}</span> ({c.canonRef})
            </div>
          ))}
        </div>
      )}

      {/* Mandatory Regulatory Disclaimer */}
      <div className="flex items-center justify-between pt-2 border-t border-stone-200 dark:border-stone-800 text-[10px] text-stone-400">
        <span className="font-semibold italic">AI suggests. Clinician decides.</span>
        <div className="flex items-center gap-2">
          {onDismiss && (
            <button
              type="button"
              onClick={onDismiss}
              className="px-2 py-1 rounded text-stone-500 hover:text-stone-700 dark:hover:text-stone-200 transition"
            >
              Dismiss
            </button>
          )}
          {onAccept && (
            <button
              type="button"
              onClick={onAccept}
              className="px-2.5 py-1 rounded bg-[#2D6A4F] hover:bg-[#255840] text-white font-medium transition"
            >
              Adopt Guidance
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
