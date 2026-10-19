import React from 'react';

export type ClinicalMizaj = 'Damawi' | 'Safrawi' | 'Balghami' | 'Sawdawi' | 'Motadil' | 'Pending';

export interface ClinicalStatusProps {
  mizaj: ClinicalMizaj;
  acuity?: 'CRITICAL' | 'URGENT' | 'STANDARD' | 'ROUTINE';
  showIcon?: boolean;
  className?: string;
}

export const ClinicalStatus: React.FC<ClinicalStatusProps> = ({
  mizaj,
  acuity,
  showIcon = true,
  className = '',
}) => {
  const mizajConfig = {
    Damawi: { label: 'Sanguine (Damawi)', bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30', icon: '🔴' },
    Safrawi: { label: 'Choleric (Safrawi)', bg: 'bg-amber-500/10 text-amber-400 border-amber-500/30', icon: '🟡' },
    Balghami: { label: 'Phlegmatic (Balghami)', bg: 'bg-sky-500/10 text-sky-400 border-sky-500/30', icon: '🔵' },
    Sawdawi: { label: 'Melancholic (Sawdawi)', bg: 'bg-purple-500/10 text-purple-400 border-purple-500/30', icon: '🟣' },
    Motadil: { label: 'Equable (Motadil)', bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30', icon: '🟢' },
    Pending: { label: 'Assessment Pending', bg: 'bg-gray-500/10 text-gray-400 border-gray-500/30', icon: '⚪' },
  }[mizaj] || { label: mizaj, bg: 'bg-gray-500/10 text-gray-400 border-gray-500/30', icon: '⚪' };

  return (
    <div className={`inline-flex items-center gap-2 ${className}`}>
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${mizajConfig.bg}`}>
        {showIcon && <span>{mizajConfig.icon}</span>}
        <span>{mizajConfig.label}</span>
      </span>
      {acuity && (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase ${
            acuity === 'CRITICAL'
              ? 'bg-red-600 text-white animate-pulse'
              : acuity === 'URGENT'
              ? 'bg-amber-500 text-black'
              : 'bg-gray-200 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
          }`}
        >
          {acuity}
        </span>
      )}
    </div>
  );
};
