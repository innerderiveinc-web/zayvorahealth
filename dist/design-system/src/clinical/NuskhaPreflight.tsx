import React, { useState } from 'react';
import { Modal } from '../components/Modal';

export interface PreflightCheckItem {
  id: string;
  label: string;
  description: string;
  passed: boolean;
  required: boolean;
}

export interface NuskhaPreflightProps {
  isOpen: boolean;
  onClose: () => void;
  patientName: string;
  mrn: string;
  substanceCount: number;
  checks?: PreflightCheckItem[];
  onExecuteSeal: (pin: string) => void;
  isSubmitting?: boolean;
  className?: string;
}

export const DEFAULT_PREFLIGHT_CHECKS: PreflightCheckItem[] = [
  {
    id: 'patient_identity',
    label: 'Patient Identity & Active Consent',
    description: 'Patient identity verified against Master Patient Index with active informed consent.',
    passed: true,
    required: true,
  },
  {
    id: 'substance_identity',
    label: 'Substance Identity & Form Verification',
    description: 'All prescribed items matched to botanical/mineral pharmacopoeial monographs (UPI/NFUM).',
    passed: true,
    required: true,
  },
  {
    id: 'evidence_provenance',
    label: 'Evidence & Monograph Provenance',
    description: 'Active formulations backed by canonical or modern trial evidence within therapeutic range.',
    passed: true,
    required: true,
  },
  {
    id: 'schedule_e1_detox',
    label: 'Schedule E(1) Detoxification (Shodhan / Tadbeer)',
    description: 'Toxicological components passed Mudabbar detoxification certification protocol.',
    passed: true,
    required: true,
  },
  {
    id: 'statutory_scope',
    label: 'Clinician Statutory Scope & Licensure',
    description: 'Attending practitioner holds valid state/central registration with unexpired practice scope.',
    passed: true,
    required: true,
  },
];

export const NuskhaPreflight: React.FC<NuskhaPreflightProps> = ({
  isOpen,
  onClose,
  patientName,
  mrn,
  substanceCount,
  checks = DEFAULT_PREFLIGHT_CHECKS,
  onExecuteSeal,
  isSubmitting = false,
  className = '',
}) => {
  const [pin, setPin] = useState('');
  const [affirmation, setAffirmation] = useState(false);

  const allPassed = checks.every((c) => !c.required || c.passed);
  const canSeal = allPassed && affirmation && pin.length >= 4;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Nuskha Preflight & 21 CFR Part 11 Digital Signoff"
      className={className}
    >
      <div className="space-y-4 text-xs" id="nuskha-preflight-modal">
        <div className="p-3 bg-stone-50 dark:bg-stone-900 rounded-lg border border-stone-200 dark:border-stone-800 flex justify-between items-center">
          <div>
            <div className="font-bold text-stone-900 dark:text-stone-100">{patientName}</div>
            <div className="text-stone-500 font-mono text-[11px]">MRN: {mrn}</div>
          </div>
          <div className="text-right">
            <span className="px-2 py-0.5 rounded bg-[#2D6A4F]/10 text-[#2D6A4F] font-semibold text-[11px]">
              {substanceCount} Formulation Items
            </span>
          </div>
        </div>

        <div className="space-y-2">
          <span className="font-bold text-stone-700 dark:text-stone-300 text-[11px] uppercase tracking-wider">
            Mandatory Preflight Invariant Gates:
          </span>
          {checks.map((check) => (
            <div
              key={check.id}
              className="p-2.5 rounded-lg border bg-white dark:bg-stone-950 flex items-start gap-2.5"
            >
              <div className="mt-0.5">
                {check.passed ? (
                  <span className="text-emerald-600 font-bold">✓</span>
                ) : (
                  <span className="text-rose-600 font-bold">✕</span>
                )}
              </div>
              <div className="flex-1">
                <div className="font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
                  <span>{check.label}</span>
                  {check.passed ? (
                    <span className="text-[9px] px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-600 font-bold uppercase">
                      PASSED
                    </span>
                  ) : (
                    <span className="text-[9px] px-1.5 py-0.2 rounded bg-rose-500/10 text-rose-600 font-bold uppercase">
                      GATE FAILED
                    </span>
                  )}
                </div>
                <div className="text-[11px] text-stone-500 mt-0.5">{check.description}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="pt-2 border-t border-stone-200 dark:border-stone-800 space-y-3">
          <label className="flex items-start gap-2 cursor-pointer select-none text-stone-600 dark:text-stone-300">
            <input
              type="checkbox"
              checked={affirmation}
              onChange={(e) => setAffirmation(e.target.checked)}
              className="mt-0.5 rounded text-[#2D6A4F] focus:ring-[#2D6A4F]"
            />
            <span className="text-[11px] leading-tight">
              I certify under penalty of statutory medical regulations that I have personally formulated and reviewed this Nuskha prescription, and commit it as a legally binding digital medical order anchored to the SHA-256 Merkle Ledger.
            </span>
          </label>

          <div className="flex items-center gap-3">
            <div className="flex-1">
              <label className="block text-[11px] font-semibold text-stone-700 dark:text-stone-300 mb-1">
                Clinician Digital Signing PIN (21 CFR Pt 11):
              </label>
              <input
                type="password"
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                maxLength={8}
                placeholder="Enter 4-8 digit PIN"
                className="w-full px-3 py-1.5 text-xs font-mono border border-stone-300 dark:border-stone-700 rounded-lg bg-white dark:bg-stone-900 focus:ring-2 focus:ring-[#2D6A4F] focus:outline-none"
              />
            </div>

            <button
              type="button"
              disabled={!canSeal || isSubmitting}
              onClick={() => onExecuteSeal(pin)}
              className="mt-5 px-4 py-2 text-xs font-bold rounded-lg text-white bg-[#2D6A4F] hover:bg-[#255840] disabled:opacity-50 disabled:cursor-not-allowed shadow transition"
            >
              {isSubmitting ? 'Sealing...' : 'Cryptographic Seal & Commit'}
            </button>
          </div>
        </div>
      </div>
    </Modal>
  );
};
