import React, { useState } from 'react';
import { Modal } from '../components/Modal';
import { SafetyRailStatus } from './SafetyRail';

export interface SafetyDecisionProps {
  isOpen: boolean;
  onClose: () => void;
  checkName: string;
  status: SafetyRailStatus;
  detail: string;
  onConfirmOverride: (rationale: string) => void;
  className?: string;
}

export const SafetyDecision: React.FC<SafetyDecisionProps> = ({
  isOpen,
  onClose,
  checkName,
  status,
  detail,
  onConfirmOverride,
  className = '',
}) => {
  const [rationale, setRationale] = useState('');
  const [acknowledgedRisk, setAcknowledgedRisk] = useState(false);

  const isBlock = status === 'BLOCK';
  const canProceed = !isBlock && acknowledgedRisk && rationale.trim().length >= 15;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={
        <div className="flex items-center gap-2">
          <span className="text-base font-bold text-stone-900 dark:text-stone-100">
            {isBlock ? 'Safety Invariant Violation (Hard Block)' : 'Safety Caution: Clinical Justification Required'}
          </span>
        </div>
      }
      className={className}
    >
      <div className="space-y-4 text-xs">
        <div className={`p-3 rounded-lg border ${isBlock ? 'bg-rose-500/10 border-rose-500/30 text-rose-800 dark:text-rose-300' : 'bg-amber-500/10 border-amber-500/30 text-amber-800 dark:text-amber-300'}`}>
          <div className="font-bold mb-1">Check: {checkName}</div>
          <div>{detail}</div>
        </div>

        {isBlock ? (
          <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-lg text-stone-600 dark:text-stone-300">
            <p className="font-semibold text-rose-600 mb-1">Prescription Formulation Blocked</p>
            This invariant cannot be overridden by clinical rationale. The selected compound or dosage violates absolute toxicological or contraindication safety boundaries under AYUSH Schedule E(1) or international pharmacopoeia standards.
          </div>
        ) : (
          <>
            <div>
              <label className="block font-semibold text-stone-700 dark:text-stone-300 mb-1">
                Mandatory Clinician Justification (Min 15 characters):
              </label>
              <textarea
                value={rationale}
                onChange={(e) => setRationale(e.target.value)}
                rows={3}
                placeholder="State clinical justification, compensatory Musleh adjuvant, or specific monitoring protocol..."
                className="w-full p-2 text-xs border border-stone-300 dark:border-stone-700 rounded-lg bg-white dark:bg-stone-900 text-stone-900 dark:text-stone-100 focus:ring-2 focus:ring-[#2D6A4F] focus:outline-none"
              />
            </div>

            <label className="flex items-start gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={acknowledgedRisk}
                onChange={(e) => setAcknowledgedRisk(e.target.checked)}
                className="mt-0.5 rounded text-[#2D6A4F] focus:ring-[#2D6A4F]"
              />
              <span className="text-stone-600 dark:text-stone-400 leading-tight">
                I certify under my clinical license that I have evaluated the drug-herb or humoral interaction and deemed the therapeutic benefit to outweigh potential risk for this patient.
              </span>
            </label>
          </>
        )}

        <div className="flex justify-end gap-2 pt-2 border-t border-stone-200 dark:border-stone-800">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 text-xs rounded-lg bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:bg-stone-300 transition"
          >
            {isBlock ? 'Close' : 'Cancel'}
          </button>
          {!isBlock && (
            <button
              type="button"
              disabled={!canProceed}
              onClick={() => {
                onConfirmOverride(rationale);
                onClose();
              }}
              className="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-amber-600 hover:bg-amber-700 text-white disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Sign Justification & Proceed
            </button>
          )}
        </div>
      </div>
    </Modal>
  );
};
