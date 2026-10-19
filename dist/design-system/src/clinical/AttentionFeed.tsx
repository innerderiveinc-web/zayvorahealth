import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface AttentionItem {
  id: string;
  type: 'CRITICAL' | 'SAFETY' | 'SIGNATURE' | 'LAB' | 'FOLLOWUP';
  badge: string;
  badgeVariant: 'danger' | 'warning' | 'info' | 'primary';
  patientName: string;
  token?: string;
  what: string;
  why: string;
  when: string;
  actionLabel: string;
  onAction: () => void;
}

export interface NextPatientSummary {
  tokenNumber: string;
  name: string;
  age: number;
  gender: string;
  chiefComplaint: string;
  waitTime: string;
  onStartConsultation: () => void;
}

export interface AttentionFeedProps {
  nextPatient?: NextPatientSummary;
  items: AttentionItem[];
  className?: string;
}

export const AttentionFeed: React.FC<AttentionFeedProps> = ({
  nextPatient,
  items,
  className = '',
}) => {
  const badgeClasses: Record<string, string> = {
    danger: 'bg-rose-500/10 text-rose-600 border-rose-500/30',
    warning: 'bg-amber-500/10 text-amber-600 border-amber-500/30',
    info: 'bg-teal-500/10 text-teal-600 border-teal-500/30',
    primary: 'bg-[#2D6A4F]/10 text-[#2D6A4F] border-[#2D6A4F]/30',
  };

  return (
    <div className={twMerge('space-y-4', className)}>
      {/* Primary Next Patient Card */}
      {nextPatient && (
        <div className="p-4 bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30 border border-emerald-500/30 rounded-xl shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-[10px] font-mono font-bold uppercase rounded bg-emerald-600 text-white tracking-wider">
                  NEXT PATIENT • TOKEN #{nextPatient.tokenNumber}
                </span>
                <span className="text-xs text-stone-500">Wait: {nextPatient.waitTime}</span>
              </div>
              <h2 className="text-base font-bold text-stone-900 dark:text-stone-100 mt-1">
                {nextPatient.name} ({nextPatient.age}y {nextPatient.gender})
              </h2>
              <p className="text-xs text-stone-600 dark:text-stone-400 mt-0.5">
                Chief Complaint: <span className="font-medium text-stone-800 dark:text-stone-200">{nextPatient.chiefComplaint}</span>
              </p>
            </div>
            <button
              type="button"
              onClick={nextPatient.onStartConsultation}
              className="px-4 py-2 text-xs font-bold rounded-lg text-white bg-[#2D6A4F] hover:bg-[#255840] shadow transition flex items-center gap-1.5"
            >
              <span>Start Consultation</span>
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Exception-First Attention Stream */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold text-stone-500 uppercase tracking-wider px-1">
          Clinical Attention Feed ({items.length} Actionable Items)
        </h3>
        {items.length === 0 ? (
          <div className="p-6 text-center text-xs text-stone-400 border border-dashed border-stone-300 dark:border-stone-800 rounded-xl">
            No acute clinical exceptions. All patients and prescriptions within nominal operating bounds.
          </div>
        ) : (
          items.map((item) => (
            <div
              key={item.id}
              className="p-3.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl hover:border-stone-300 dark:hover:border-stone-700 transition"
            >
              <div className="flex flex-wrap items-start justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <span className={twMerge('px-2 py-0.5 text-[10px] font-bold uppercase rounded border', badgeClasses[item.badgeVariant])}>
                    {item.badge}
                  </span>
                  <span className="text-xs font-semibold text-stone-900 dark:text-stone-100">
                    {item.patientName} {item.token ? `(#${item.token})` : ''}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={item.onAction}
                  className="px-2.5 py-1 text-xs font-medium rounded-md bg-stone-100 dark:bg-stone-800 hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-900 dark:text-stone-100 transition"
                >
                  {item.actionLabel}
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-xs text-stone-600 dark:text-stone-400 bg-stone-50 dark:bg-stone-950/50 p-2.5 rounded-lg">
                <div>
                  <span className="font-bold text-stone-700 dark:text-stone-300">WHAT: </span>
                  {item.what}
                </div>
                <div>
                  <span className="font-bold text-stone-700 dark:text-stone-300">WHY: </span>
                  {item.why}
                </div>
                <div>
                  <span className="font-bold text-stone-700 dark:text-stone-300">WHEN: </span>
                  {item.when}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
