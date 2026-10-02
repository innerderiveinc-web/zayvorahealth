import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface AxisMetric {
  name: string;
  value: string;
  status: 'normal' | 'abnormal' | 'borderline';
}

export interface AxisDetailProps {
  axisName: string;
  classicalConcept: string;
  classicalReference: string;
  functionalScore: number;
  vulnerabilityStatus: string;
  metrics: AxisMetric[];
  clinicalNotes?: string;
  className?: string;
}

export const AxisDetail: React.FC<AxisDetailProps> = ({
  axisName,
  classicalConcept,
  classicalReference,
  functionalScore,
  vulnerabilityStatus,
  metrics,
  clinicalNotes,
  className = '',
}) => {
  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-3', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2.5">
        <div>
          <h4 className="text-sm font-bold text-stone-900 dark:text-stone-100">{axisName}</h4>
          <p className="text-xs text-stone-500 italic mt-0.5">{classicalConcept}</p>
        </div>
        <div className="text-right">
          <div className="text-xs font-mono font-bold text-[#2D6A4F]">Score: {functionalScore}/10</div>
          <span className="text-[10px] text-stone-500 uppercase">{vulnerabilityStatus}</span>
        </div>
      </div>

      <div>
        <h5 className="text-[11px] font-bold uppercase text-stone-400 mb-1.5 tracking-wider">Functional Biomarkers & Signs</h5>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          {metrics.map((m, idx) => (
            <div key={idx} className="flex items-center justify-between p-2 rounded bg-stone-50 dark:bg-stone-950/50">
              <span className="text-stone-600 dark:text-stone-400">{m.name}</span>
              <span className={twMerge('font-mono font-semibold', m.status === 'abnormal' ? 'text-rose-600' : m.status === 'borderline' ? 'text-amber-600' : 'text-emerald-600')}>
                {m.value}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="p-2.5 rounded bg-stone-50 dark:bg-stone-950 text-xs border border-stone-200/50 dark:border-stone-800/50">
        <span className="font-bold text-stone-700 dark:text-stone-300">Classical Canon Anchor: </span>
        <span className="text-stone-600 dark:text-stone-400">{classicalReference}</span>
      </div>

      {clinicalNotes && (
        <div className="text-xs text-stone-600 dark:text-stone-400 bg-teal-500/5 p-2.5 rounded border border-teal-500/20">
          <span className="font-bold text-teal-800 dark:text-teal-300">Clinician Guidance: </span>
          {clinicalNotes}
        </div>
      )}
    </div>
  );
};
