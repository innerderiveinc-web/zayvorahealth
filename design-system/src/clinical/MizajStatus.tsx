import React from 'react';
import { twMerge } from 'tailwind-merge';

export type MizajType = 'Damawi' | 'Safrawi' | 'Balghami' | 'Sawdawi' | 'Motadil' | 'Pending';

export interface MizajStatusProps {
  mizaj: MizajType;
  secondaryMizaj?: string;
  confidence?: number;
  qualities?: {
    hararat?: number; // Heat (0 - 100)
    buroodat?: number; // Cold (0 - 100)
    rutoobat?: number; // Moisture (0 - 100)
    yuboosat?: number; // Dryness (0 - 100)
  };
  assessedAt?: string;
  assessedBy?: string;
  className?: string;
}

export const MizajStatus: React.FC<MizajStatusProps> = ({
  mizaj,
  secondaryMizaj,
  confidence,
  qualities,
  assessedAt,
  assessedBy,
  className = '',
}) => {
  const configs = {
    Damawi: {
      name: 'Damawi (Sanguine)',
      primary: 'Hot & Moist (Haar-Rattab)',
      bg: 'bg-rose-500/10 border-rose-500/30 text-rose-700 dark:text-rose-300',
      tagBg: 'bg-rose-600 text-white',
    },
    Safrawi: {
      name: 'Safrawi (Choleric)',
      primary: 'Hot & Dry (Haar-Yaabis)',
      bg: 'bg-amber-500/10 border-amber-500/30 text-amber-700 dark:text-amber-300',
      tagBg: 'bg-amber-600 text-white',
    },
    Balghami: {
      name: 'Balghami (Phlegmatic)',
      primary: 'Cold & Moist (Baarid-Rattab)',
      bg: 'bg-sky-500/10 border-sky-500/30 text-sky-700 dark:text-sky-300',
      tagBg: 'bg-sky-600 text-white',
    },
    Sawdawi: {
      name: 'Sawdawi (Melancholic)',
      primary: 'Cold & Dry (Baarid-Yaabis)',
      bg: 'bg-purple-500/10 border-purple-500/30 text-purple-700 dark:text-purple-300',
      tagBg: 'bg-purple-600 text-white',
    },
    Motadil: {
      name: 'Motadil (Equable)',
      primary: 'Balanced Equilibrium',
      bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-700 dark:text-emerald-300',
      tagBg: 'bg-emerald-600 text-white',
    },
    Pending: {
      name: 'Needs Assessment',
      primary: 'Unassessed Baseline',
      bg: 'bg-stone-500/10 border-stone-500/30 text-stone-700 dark:text-stone-300',
      tagBg: 'bg-stone-600 text-white',
    },
  }[mizaj] || {
    name: mizaj,
    primary: 'Unspecified',
    bg: 'bg-stone-500/10 border-stone-500/30 text-stone-700 dark:text-stone-300',
    tagBg: 'bg-stone-600 text-white',
  };

  return (
    <div className={twMerge('p-4 border rounded-xl bg-white dark:bg-stone-900', configs.bg, className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <span className={twMerge('px-2 py-0.5 text-xs font-bold rounded uppercase tracking-wider', configs.tagBg)}>
            {mizaj}
          </span>
          <span className="text-sm font-bold text-stone-900 dark:text-stone-100">
            {configs.name}
          </span>
          {secondaryMizaj && (
            <span className="text-xs text-stone-500">
              (Sec: {secondaryMizaj})
            </span>
          )}
        </div>
        {confidence !== undefined && (
          <span className="text-xs font-medium px-2 py-0.5 bg-stone-100 dark:bg-stone-800 rounded text-stone-700 dark:text-stone-300">
            Confidence: {Math.round(confidence * 100)}%
          </span>
        )}
      </div>

      <div className="text-xs text-stone-600 dark:text-stone-400 mb-3">
        Humoral Polarity: <span className="font-semibold text-stone-800 dark:text-stone-200">{configs.primary}</span>
      </div>

      {qualities && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-stone-200 dark:border-stone-800 text-[11px]">
          <div>Heat (Haar): <span className="font-semibold">{qualities.hararat ?? 'N/A'}%</span></div>
          <div>Cold (Baarid): <span className="font-semibold">{qualities.buroodat ?? 'N/A'}%</span></div>
          <div>Moisture (Rattab): <span className="font-semibold">{qualities.rutoobat ?? 'N/A'}%</span></div>
          <div>Dryness (Yaabis): <span className="font-semibold">{qualities.yuboosat ?? 'N/A'}%</span></div>
        </div>
      )}

      {(assessedAt || assessedBy) && (
        <div className="mt-2.5 pt-2 border-t border-stone-200 dark:border-stone-800 text-[10px] text-stone-400 flex items-center justify-between">
          {assessedAt && <span>Assessed: {assessedAt}</span>}
          {assessedBy && <span>Clinician: {assessedBy}</span>}
        </div>
      )}
    </div>
  );
};
