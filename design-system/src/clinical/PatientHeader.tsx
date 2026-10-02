import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface PatientHeaderProps {
  mrn: string;
  name: string;
  age: number;
  gender: 'Male' | 'Female' | 'Other';
  dominantMizaj?: 'Damawi' | 'Safrawi' | 'Balghami' | 'Sawdawi' | 'Motadil' | null;
  secondaryMizaj?: string | null;
  tokenNumber?: string;
  acuity?: 'CRITICAL' | 'URGENT' | 'STANDARD' | 'ROUTINE';
  allergies?: string[];
  attendingClinician?: string;
  onSelectToken?: () => void;
  className?: string;
}

export const PatientHeader: React.FC<PatientHeaderProps> = ({
  mrn,
  name,
  age,
  gender,
  dominantMizaj,
  secondaryMizaj,
  tokenNumber,
  acuity = 'STANDARD',
  allergies = [],
  attendingClinician,
  onSelectToken,
  className = '',
}) => {
  const mizajBadge = dominantMizaj ? {
    Damawi: { label: 'Damawi (Sanguine)', bg: 'bg-rose-500/10 text-rose-600 border-rose-500/30' },
    Safrawi: { label: 'Safrawi (Choleric)', bg: 'bg-amber-500/10 text-amber-600 border-amber-500/30' },
    Balghami: { label: 'Balghami (Phlegmatic)', bg: 'bg-sky-500/10 text-sky-600 border-sky-500/30' },
    Sawdawi: { label: 'Sawdawi (Melancholic)', bg: 'bg-purple-500/10 text-purple-600 border-purple-500/30' },
    Motadil: { label: 'Motadil (Equable)', bg: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/30' },
  }[dominantMizaj] : {
    label: 'Needs Assessment',
    bg: 'bg-stone-200 text-stone-600 border-stone-300 dark:bg-stone-800 dark:text-stone-400',
  };

  return (
    <div className={twMerge('flex flex-wrap items-center justify-between gap-3 p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl shadow-sm', className)}>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[#2D6A4F]/10 text-[#2D6A4F] flex items-center justify-center font-bold text-sm">
          {name.charAt(0)}
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-base font-bold text-stone-900 dark:text-stone-100">
              {name}
            </h1>
            <span className="text-xs text-stone-500">
              ({age}y {gender})
            </span>
            {tokenNumber && (
              <span
                onClick={onSelectToken}
                className="px-2 py-0.5 text-[11px] font-mono font-bold rounded bg-teal-500/10 text-teal-700 dark:text-teal-400 border border-teal-500/20 cursor-pointer"
              >
                Token #{tokenNumber}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 mt-0.5 text-xs text-stone-500">
            <span className="font-mono">MRN: {mrn}</span>
            {attendingClinician && <span>• Attending: {attendingClinician}</span>}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2 text-xs">
        <div className={twMerge('px-2.5 py-1 rounded-md font-medium border text-xs', mizajBadge.bg)}>
          Mizaj: <span className="font-semibold">{mizajBadge.label}</span>
          {secondaryMizaj && <span className="opacity-75"> / {secondaryMizaj}</span>}
        </div>

        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
            acuity === 'CRITICAL'
              ? 'bg-rose-600 text-white animate-pulse'
              : acuity === 'URGENT'
              ? 'bg-amber-500 text-black'
              : 'bg-stone-200 text-stone-700 dark:bg-stone-800 dark:text-stone-300'
          }`}
        >
          {acuity}
        </span>

        {allergies.length > 0 ? (
          <span className="px-2.5 py-1 rounded-md bg-rose-500/10 text-rose-700 dark:text-rose-400 border border-rose-500/30 font-medium">
            ⚠ Allergies: {allergies.join(', ')}
          </span>
        ) : (
          <span className="px-2 py-1 rounded-md bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30 text-[11px]">
            No Known Allergies
          </span>
        )}
      </div>
    </div>
  );
};
