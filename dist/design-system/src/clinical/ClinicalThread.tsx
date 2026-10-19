import React from 'react';
import { twMerge } from 'tailwind-merge';

export type ClinicalThreadStageId =
  | 'patient'
  | 'assessment'
  | 'mizaj'
  | 'axes'
  | 'knowledge'
  | 'evidence'
  | 'safety'
  | 'hakeem'
  | 'nuskha'
  | 'approval'
  | 'treatment'
  | 'outcome';

export interface ClinicalStageDef {
  id: ClinicalThreadStageId;
  label: string;
  sub: string;
  status: 'completed' | 'active' | 'pending' | 'warning' | 'blocked';
}

export interface ClinicalThreadProps {
  currentStageId: ClinicalThreadStageId;
  stages?: ClinicalStageDef[];
  onSelectStage?: (stageId: ClinicalThreadStageId) => void;
  className?: string;
}

export const DEFAULT_CLINICAL_THREAD_STAGES: ClinicalStageDef[] = [
  { id: 'patient', label: '1. Patient 360', sub: 'Demographics & Vitals', status: 'completed' },
  { id: 'assessment', label: '2. Assessment', sub: 'Nabz, Baul, Baraz', status: 'completed' },
  { id: 'mizaj', label: '3. Mizaj', sub: 'Humoral Polarity', status: 'completed' },
  { id: 'axes', label: '4. Organ-Axis', sub: 'Functional Balance', status: 'completed' },
  { id: 'knowledge', label: '5. Knowledge', sub: 'Classical + Form.', status: 'completed' },
  { id: 'evidence', label: '6. Evidence', sub: 'GRADE & Modern trials', status: 'completed' },
  { id: 'safety', label: '7. Safety Rail', sub: 'CYP450 & Mudabbar', status: 'completed' },
  { id: 'hakeem', label: '8. Hakeem Sahab™', sub: 'AI Co-pilot (0.08)', status: 'completed' },
  { id: 'nuskha', label: '9. Nuskha', sub: 'Multi-Pillar Rx', status: 'active' },
  { id: 'approval', label: '10. 21 CFR Pt 11', sub: 'Digital Seal & PIN', status: 'pending' },
  { id: 'treatment', label: '11. Dispense', sub: 'FEFO & Barcode', status: 'pending' },
  { id: 'outcome', label: '12. Outcomes', sub: 'PROM & Recurrence', status: 'pending' },
];

export const ClinicalThread: React.FC<ClinicalThreadProps> = ({
  currentStageId,
  stages = DEFAULT_CLINICAL_THREAD_STAGES,
  onSelectStage,
  className = '',
}) => {
  return (
    <div className={twMerge('w-full bg-[#1B4332] text-white p-2.5 rounded-xl shadow-md overflow-x-auto', className)}>
      <div className="flex items-center justify-between min-w-[900px] gap-1 px-1">
        {stages.map((stage, idx) => {
          const isActive = stage.id === currentStageId;
          const statusStyle = {
            completed: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
            active: 'bg-amber-400 text-stone-900 border-amber-300 ring-2 ring-amber-400/50 font-bold',
            pending: 'bg-stone-800/60 text-stone-400 border-stone-700/50',
            warning: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
            blocked: 'bg-rose-500/20 text-rose-300 border-rose-500/40',
          }[isActive ? 'active' : stage.status];

          return (
            <React.Fragment key={stage.id}>
              <button
                type="button"
                onClick={() => onSelectStage?.(stage.id)}
                className={twMerge(
                  'flex flex-col items-center justify-center px-2 py-1.5 rounded-lg border text-center transition min-w-[70px]',
                  statusStyle,
                  onSelectStage ? 'cursor-pointer hover:opacity-90' : 'cursor-default'
                )}
              >
                <span className="text-[10px] leading-tight truncate w-full">
                  {stage.label}
                </span>
                <span className={twMerge('text-[9px] leading-tight opacity-75 truncate w-full', isActive ? 'text-stone-800' : '')}>
                  {stage.sub}
                </span>
              </button>
              {idx < stages.length - 1 && (
                <span className="text-stone-500 text-[10px] select-none">→</span>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
