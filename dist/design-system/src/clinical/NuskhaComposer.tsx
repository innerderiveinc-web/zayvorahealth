import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface NuskhaItem {
  id: string;
  name: string;
  type: 'MUFRAD' | 'MURAKKAB';
  dosage: string;
  unit: string;
  frequency: string;
  duration: string;
  anupanVehicle?: string;
  isScheduleE1?: boolean;
  mudabbarCertified?: boolean;
  instructions?: string;
}

export interface NuskhaComposerProps {
  items: NuskhaItem[];
  onAddItem?: () => void;
  onRemoveItem?: (id: string) => void;
  onEditItem?: (item: NuskhaItem) => void;
  onProceedToSignoff?: () => void;
  canSignoff?: boolean;
  className?: string;
}

export const NuskhaComposer: React.FC<NuskhaComposerProps> = ({
  items,
  onAddItem,
  onRemoveItem,
  onEditItem,
  onProceedToSignoff,
  canSignoff = true,
  className = '',
}) => {
  return (
    <div className={twMerge('p-4 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-xl space-y-3', className)}>
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-2.5">
        <div>
          <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100">
            Nuskha Composer (Multi-Pillar Formulation)
          </h3>
          <p className="text-[11px] text-stone-500">
            Mufradat (Singles), Murakkabat (Compounds) & Regimen Planning
          </p>
        </div>
        {onAddItem && (
          <button
            type="button"
            onClick={onAddItem}
            className="px-2.5 py-1 text-xs font-semibold rounded-lg bg-[#2D6A4F] text-white hover:bg-[#255840] transition"
          >
            + Add Substance
          </button>
        )}
      </div>

      <div className="space-y-2">
        {items.length === 0 ? (
          <div className="p-8 text-center text-xs text-stone-400 border border-dashed border-stone-200 dark:border-stone-800 rounded-lg">
            No substances added to this prescription yet. Click "+ Add Substance" to begin authoring.
          </div>
        ) : (
          items.map((item) => (
            <div
              key={item.id}
              className="p-3 rounded-lg bg-stone-50 dark:bg-stone-950/60 border border-stone-200 dark:border-stone-800 flex flex-wrap items-center justify-between gap-2 text-xs"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-stone-900 dark:text-stone-100">{item.name}</span>
                  <span className="px-1.5 py-0.2 text-[9px] font-bold rounded bg-stone-200 dark:bg-stone-800 text-stone-600 dark:text-stone-400 uppercase">
                    {item.type}
                  </span>
                  {item.isScheduleE1 && (
                    <span className={twMerge('px-1.5 py-0.2 text-[9px] font-bold rounded uppercase border', item.mudabbarCertified ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/30' : 'bg-rose-500/10 text-rose-600 border-rose-500/30')}>
                      {item.mudabbarCertified ? 'Schedule E(1) Mudabbar Verified' : 'Schedule E(1) Mudabbar Required'}
                    </span>
                  )}
                </div>

                <div className="mt-1 flex flex-wrap items-center gap-3 text-stone-500 text-[11px]">
                  <span>Dose: <strong className="text-stone-700 dark:text-stone-300">{item.dosage} {item.unit}</strong></span>
                  <span>Freq: <strong className="text-stone-700 dark:text-stone-300">{item.frequency}</strong></span>
                  <span>Duration: <strong className="text-stone-700 dark:text-stone-300">{item.duration}</strong></span>
                  {item.anupanVehicle && (
                    <span>Vehicle (Badraqa): <strong className="text-teal-700 dark:text-teal-400">{item.anupanVehicle}</strong></span>
                  )}
                </div>

                {item.instructions && (
                  <div className="mt-1 text-[11px] text-stone-600 dark:text-stone-400 italic">
                    Note: {item.instructions}
                  </div>
                )}
              </div>

              <div className="flex items-center gap-2">
                {onEditItem && (
                  <button
                    type="button"
                    onClick={() => onEditItem(item)}
                    className="p-1 text-stone-400 hover:text-stone-600 text-xs"
                  >
                    Edit
                  </button>
                )}
                {onRemoveItem && (
                  <button
                    type="button"
                    onClick={() => onRemoveItem(item.id)}
                    className="p-1 text-rose-500 hover:text-rose-700 text-xs"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {onProceedToSignoff && (
        <div className="pt-2 border-t border-stone-200 dark:border-stone-800 flex justify-end">
          <button
            type="button"
            disabled={!canSignoff || items.length === 0}
            onClick={onProceedToSignoff}
            className="px-4 py-2 text-xs font-bold rounded-lg text-white bg-[#2D6A4F] hover:bg-[#255840] disabled:opacity-50 disabled:cursor-not-allowed shadow transition"
          >
            Proceed to 21 CFR Part 11 Signoff →
          </button>
        </div>
      )}
    </div>
  );
};
