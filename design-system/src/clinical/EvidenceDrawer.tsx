import React from 'react';
import { Drawer } from '../primitives/Drawer';

export interface EvidenceDrawerData {
  claim: string;
  source: string;
  sourceType: string;
  strength: string;
  gradeScore: string;
  reviewer: string;
  reviewerRole: string;
  reviewTimestamp: string;
  limitations: string;
  classicalContext?: string;
  doiOrCanonRef?: string;
}

export interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  data: EvidenceDrawerData | null;
  className?: string;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({
  isOpen,
  onClose,
  data,
  className = '',
}) => {
  return (
    <Drawer
      isOpen={isOpen}
      onClose={onClose}
      title="Evidence Provenance Drawer"
      subtitle="Canonical Rigor & Scientific Validation Ledger"
      size="lg"
      className={className}
      id="evidence-drawer-overlay"
      footer={
        <div className="flex items-center justify-between text-xs">
          <span className="text-stone-500">ZAYVORA Evidence Governance Protocol v2.4</span>
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 font-medium hover:bg-stone-300 dark:hover:bg-stone-700 transition"
          >
            Close Provenance
          </button>
        </div>
      }
    >
      {!data ? (
        <div className="p-8 text-center text-xs text-stone-400 italic">
          No evidence record selected for inspection.
        </div>
      ) : (
        <div className="space-y-4 text-xs">
          {/* Question 1: What is the Clinical Claim? */}
          <div className="p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#2D6A4F]">
              1. What is the Clinical Claim?
            </span>
            <p className="mt-1 font-semibold text-stone-900 dark:text-stone-100 text-sm">
              "{data.claim}"
            </p>
            {data.classicalContext && (
              <p className="mt-1 text-stone-500 italic text-[11px]">
                Classical Context: {data.classicalContext}
              </p>
            )}
          </div>

          {/* Question 2: What is the Authoritative Source? */}
          <div className="p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#2D6A4F]">
              2. What is the Authoritative Source?
            </span>
            <div className="mt-1 font-medium text-stone-800 dark:text-stone-200">
              {data.source}
            </div>
            <div className="mt-0.5 text-stone-500 text-[11px]">
              Type: <span className="font-mono text-stone-700 dark:text-stone-300">{data.sourceType}</span>
              {data.doiOrCanonRef && (
                <span className="ml-2 font-mono">| Ref: {data.doiOrCanonRef}</span>
              )}
            </div>
          </div>

          {/* Question 3: How Strong is the Evidence? */}
          <div className="p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#2D6A4F]">
              3. How Strong is the Evidence?
            </span>
            <div className="mt-1 flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-teal-500/10 text-teal-700 dark:text-teal-400 border border-teal-500/30 font-bold">
                {data.gradeScore}
              </span>
              <span className="text-stone-700 dark:text-stone-300">{data.strength}</span>
            </div>
          </div>

          {/* Question 4: Who Reviewed and Approved It? */}
          <div className="p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#2D6A4F]">
              4. Who Reviewed and Approved It?
            </span>
            <div className="mt-1 text-stone-800 dark:text-stone-200 font-semibold">
              {data.reviewer}
            </div>
            <div className="text-stone-500 text-[11px]">
              Credential / Role: {data.reviewerRole}
            </div>
          </div>

          {/* Question 5: When Was the Review Certified? */}
          <div className="p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#2D6A4F]">
              5. When Was the Review Certified?
            </span>
            <div className="mt-1 font-mono text-stone-700 dark:text-stone-300">
              {data.reviewTimestamp}
            </div>
          </div>

          {/* Question 6: What are the Clinical Limitations? */}
          <div className="p-3.5 bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl">
            <span className="text-[10px] font-bold uppercase tracking-wider text-rose-700 dark:text-rose-400">
              6. What are the Clinical Limitations?
            </span>
            <p className="mt-1 text-stone-700 dark:text-stone-300 leading-relaxed">
              {data.limitations}
            </p>
          </div>
        </div>
      )}
    </Drawer>
  );
};
