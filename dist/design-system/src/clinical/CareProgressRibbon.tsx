import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface CareProgressStep {
  id: string;
  label: string;
  date?: string;
  status: 'completed' | 'current' | 'upcoming';
}

export interface CareProgressRibbonProps {
  steps: CareProgressStep[];
  currentStepId: string;
  className?: string;
}

export const DEFAULT_CARE_STEPS: CareProgressStep[] = [
  { id: 'triage', label: 'Triage & Intake', status: 'completed' },
  { id: 'consultation', label: 'Consultation', status: 'completed' },
  { id: 'rx_dispatched', label: 'Nuskha Dispensed', status: 'current' },
  { id: 'day7_followup', label: 'Day 7 Asbab Check', status: 'upcoming' },
  { id: 'milestone_review', label: 'Milestone Review', status: 'upcoming' },
];

export const CareProgressRibbon: React.FC<CareProgressRibbonProps> = ({
  steps = DEFAULT_CARE_STEPS,
  currentStepId,
  className = '',
}) => {
  return (
    <div className={twMerge('w-full p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-2', className)}>
      <div className="flex items-center justify-between text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">
        <span>Care Pathway Progression</span>
        <span className="text-[#2D6A4F] lowercase font-medium">patient journey view</span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
        {steps.map((step) => {
          const isCurrent = step.id === currentStepId || step.status === 'current';
          const isCompleted = step.status === 'completed';

          return (
            <div
              key={step.id}
              className={twMerge(
                'p-2.5 rounded-lg border text-center transition flex flex-col items-center justify-center text-xs',
                isCurrent
                  ? 'bg-[#2D6A4F]/10 border-[#2D6A4F] text-[#2D6A4F] font-bold ring-1 ring-[#2D6A4F]'
                  : isCompleted
                  ? 'bg-stone-50 dark:bg-stone-950 border-stone-200 dark:border-stone-800 text-stone-700 dark:text-stone-300'
                  : 'bg-stone-50/50 dark:bg-stone-950/20 border-dashed border-stone-200 dark:border-stone-800 text-stone-400'
              )}
            >
              <div className="flex items-center gap-1 mb-1">
                {isCompleted && <span className="text-emerald-600 font-bold">✓</span>}
                {isCurrent && <span className="w-2 h-2 rounded-full bg-[#2D6A4F] animate-ping" />}
                <span className="font-semibold truncate text-[11px]">{step.label}</span>
              </div>
              {step.date && (
                <span className="text-[10px] text-stone-400 font-mono">{step.date}</span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
