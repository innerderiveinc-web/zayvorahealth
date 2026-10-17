"use client";

import React, { useState, useEffect } from "react";
import { scribeApi, type SOAPNote } from "@/lib/scribeApi";
import { governanceApi, type AuditVerificationOut, type Part11SignatureOut } from "@/lib/governanceApi";

interface AmbientScribeGovernanceCockpitProps {
  token: string;
  patientId: string;
  patientName: string;
}

const SAMPLE_TRANSCRIPTS = [
  {
    label: "Urdu (Roman Transliteration) - Joint & Gastric",
    text: "Mareez ne bataya ke pichhle do hafton se ghutno me shadeed dard aur subah ki sakhti rehti hai. Seenay me jalan aur tezaabiyat ki shikayat bhi hai. Qabz aur raat ko neend na aana bhi barh gaya hai.",
  },
  {
    label: "Roman Urdu / Hinglish - Sciatica & Acidity",
    text: "Doctor sahab, pichle 3 hafton se langdi ka dard (sciatica) kamar se paanv tak jaata hai. Sinay me jalan rehti hai aur pet me bhari pan hai. Subah thakan zyada hoti hai.",
  },
  {
    label: "Hindi (Devanagari) - Dyspepsia & Fatigue",
    text: "मरीज को पिछले एक महीने से पेट में मरोड़ और सीने में जलन है। बहुत कमजोरी और थकान महसूस होती है। जोड़ों का दर्द भी हल्का-हल्का रहता है।",
  },
  {
    label: "English - Bilious Gastritis & Palpitations",
    text: "Patient reports intense burning epigastric pain, bitter taste in mouth, palpitations (khafaqan), and anxiety especially at night. Aggravated by fried spicy food.",
  },
];

export function AmbientScribeGovernanceCockpit({
  token,
  patientId,
  patientName,
}: AmbientScribeGovernanceCockpitProps) {
  const [transcript, setTranscript] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [soapNote, setSoapNote] = useState<SOAPNote | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Signing & Attestation
  const [showSignModal, setShowSignModal] = useState(false);
  const [clinicianId, setClinicianId] = useState("HAK-4401");
  const [clinicianName, setClinicianName] = useState("Hakim Zafarullah Khan");
  const [clinicianRole, setClinicianRole] = useState("hakeem");
  const [clinicianNotes, setClinicianNotes] = useState("Clinically reviewed and approved under standard Unani posology.");
  const [isSigning, setIsSigning] = useState(false);
  const [signatureEnvelope, setSignatureEnvelope] = useState<Part11SignatureOut | null>(null);

  // Audit Ledger Verification
  const [auditStatus, setAuditStatus] = useState<AuditVerificationOut | null>(null);
  const [isVerifyingAudit, setIsVerifyingAudit] = useState(false);

  useEffect(() => {
    handleVerifyAudit();
  }, []);

  const handleProcessTranscript = async () => {
    if (!transcript.trim()) {
      setError("Please input or select a consultation dialogue transcript.");
      return;
    }
    setIsProcessing(true);
    setError(null);
    try {
      const res = await scribeApi.processTranscript(token, {
        patient_id: patientId,
        transcript: transcript,
      });
      setSoapNote(res);
      setSignatureEnvelope(null);
    } catch (err: any) {
      setError(err?.message || "Failed to process audio consultation transcript.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSignAndLock = async () => {
    if (!soapNote) return;
    setIsSigning(true);
    setError(null);
    try {
      // 1. Lock note in Scribe service
      const lockedNote = await scribeApi.signAndLockNote(token, {
        note_id: soapNote.note_id,
        clinician_id: clinicianId,
        clinician_name: clinicianName,
        clinician_role: clinicianRole,
        clinician_notes: clinicianNotes,
      });
      setSoapNote(lockedNote);

      // 2. Generate 21 CFR Part 11 Signature
      const sig = await governanceApi.signDocument(token, {
        signer_id: clinicianId,
        signer_name: clinicianName,
        signer_role: clinicianRole,
        document_payload: lockedNote,
        signature_meaning: "Clinical Review & Statutory Approval (21 CFR § 11.50)",
      });
      setSignatureEnvelope(sig);
      setShowSignModal(false);

      // 3. Refresh audit status
      await handleVerifyAudit();
    } catch (err: any) {
      setError(err?.message || "Failed to sign and lock clinical document.");
    } finally {
      setIsSigning(false);
    }
  };

  const handleVerifyAudit = async () => {
    setIsVerifyingAudit(true);
    try {
      const res = await governanceApi.verifyChain(token);
      setAuditStatus(res);
    } catch {
      // ignore
    } finally {
      setIsVerifyingAudit(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">🎙️</span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                Ambient Clinical Scribe & 21 CFR Part 11 Regulatory Governance
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Multi-Lingual Voice AI
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Active Patient: <span className="text-cyan-400 font-semibold">{patientName}</span> ({patientId})
              {" • "}Auto-maps Urdu (Nastaliq), Hindi (Devanagari), Roman Urdu, and English to canonical Unani pathology.
            </p>
          </div>

          {/* Cryptographic Ledger Status Badge */}
          <div className="flex items-center gap-3 bg-slate-950 border border-slate-800 rounded-lg p-3">
            <div className={`w-3 h-3 rounded-full ${auditStatus?.is_valid ? "bg-emerald-400 animate-pulse" : "bg-red-400"}`} />
            <div className="text-xs">
              <div className="font-semibold text-slate-200">
                Merkle Audit Trail: {auditStatus?.is_valid ? "VERIFIED INTACT" : "UNVERIFIED"}
              </div>
              <div className="text-slate-500 font-mono">
                {auditStatus ? `${auditStatus.total_blocks} Blocks • SHA-256 Hash Chained` : "Checking ledger..."}
              </div>
            </div>
            <button
              onClick={handleVerifyAudit}
              disabled={isVerifyingAudit}
              className="text-xs px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition"
            >
              {isVerifyingAudit ? "Verifying..." : "Re-Verify"}
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-sm flex items-center justify-between">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} className="text-red-300 hover:text-white text-xs">Dismiss</button>
        </div>
      )}

      {/* Main Grid: Transcript Input vs Generated Unani SOAP Note */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 5 Cols: Ambient Consultation Transcript */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider mb-3 flex items-center justify-between">
              <span>Ambient Audio Transcript</span>
              <span className="text-xs font-normal text-slate-400">Live Listening / Dictation</span>
            </h3>

            {/* Quick Sample Presets */}
            <div className="space-y-1.5 mb-3">
              <div className="text-xs text-slate-400 font-medium">Load Polyglot Clinical Encounter:</div>
              <div className="flex flex-wrap gap-1.5">
                {SAMPLE_TRANSCRIPTS.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => setTranscript(s.text)}
                    className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700/80 transition"
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>

            <textarea
              rows={8}
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              placeholder="Paste or transcribe doctor-patient dialogue in Urdu, Hindi, English, or Roman Urdu..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500/50 resize-none font-sans"
            />

            <button
              onClick={handleProcessTranscript}
              disabled={isProcessing}
              className="w-full mt-3 py-2.5 px-4 bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-500 hover:to-cyan-500 text-white font-semibold rounded-lg shadow-md transition disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {isProcessing ? (
                <>
                  <span className="animate-spin text-lg">⏳</span>
                  <span>Synthesizing Unani SOAP Note...</span>
                </>
              ) : (
                <>
                  <span>⚡ Process & Extract Unani SOAP Note</span>
                </>
              )}
            </button>
          </div>

          {/* 21 CFR Part 11 Stamp display if signed */}
          {signatureEnvelope && (
            <div className="bg-emerald-950/40 border border-emerald-600/40 rounded-xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                <span>🛡️ 21 CFR Part 11 Electronic Signature Executed</span>
              </div>
              <div className="space-y-1.5 text-xs text-slate-300 font-mono">
                <div>Signer: <span className="text-white font-semibold">{signatureEnvelope.signer_name}</span> ({signatureEnvelope.signer_role})</div>
                <div>Meaning: <span className="text-emerald-300">{signatureEnvelope.signature_meaning}</span></div>
                <div>Timestamp: <span className="text-slate-400">{signatureEnvelope.timestamp_utc}</span></div>
                <div>Signature ID: <span className="text-cyan-400">{signatureEnvelope.signature_id}</span></div>
                <div className="break-all text-[11px] text-slate-500 pt-1 border-t border-emerald-800/40">
                  HMAC Seal: {signatureEnvelope.cryptographic_seal}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right 7 Cols: Structured Unani SOAP Note */}
        <div className="lg:col-span-7">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <span>📋 Structured Unani Clinical Note (SOAP)</span>
                </h3>
                {soapNote && (
                  <div className="text-xs text-slate-400 mt-0.5">
                    Note ID: <span className="font-mono text-cyan-400">{soapNote.note_id}</span>
                    {" • "}Languages: {soapNote.detected_languages.join(", ")}
                  </div>
                )}
              </div>

              {soapNote && (
                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${soapNote.safe_to_lock ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40" : "bg-amber-500/20 text-amber-400 border border-amber-500/40"}`}>
                    {soapNote.status}
                  </span>
                  {!soapNote.safe_to_lock && (
                    <button
                      onClick={() => setShowSignModal(true)}
                      className="text-xs px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg shadow transition"
                    >
                      ✍️ Clinician Sign & Lock
                    </button>
                  )}
                </div>
              )}
            </div>

            {!soapNote ? (
              <div className="py-16 text-center text-slate-500 text-sm">
                <p>No SOAP note synthesized yet.</p>
                <p className="text-xs text-slate-600 mt-1">
                  Load a sample dialogue and click "Process & Extract Unani SOAP Note".
                </p>
              </div>
            ) : (
              <div className="space-y-4 text-sm max-h-[600px] overflow-y-auto pr-2">
                {/* Subjective */}
                <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-3.5 space-y-2">
                  <div className="text-xs font-bold uppercase text-cyan-400 tracking-wider">
                    S — Subjective (Shikayat-e-Awwaliyah)
                  </div>
                  <div>
                    <span className="text-xs text-slate-400">Extracted Symptoms: </span>
                    <div className="flex flex-wrap gap-1.5 mt-1">
                      {soapNote.subjective.colloquial_findings.map((f, i) => (
                        <span key={i} className="text-xs px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-800/60 text-cyan-300 font-medium">
                          {f.unani_pathology} <span className="text-slate-500">("{f.colloquial_phrase}")</span>
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="text-xs text-slate-300 pt-2 border-t border-slate-800/80">
                    <span className="font-semibold text-slate-400">Asbab-e-Sittah Zarooriyyah:</span>
                    <ul className="grid grid-cols-2 gap-1 mt-1 text-slate-400">
                      <li>• Hawa: {soapNote.subjective.asbab_sittah_zarooriyyah.hawa}</li>
                      <li>• Makool/Mashroob: {soapNote.subjective.asbab_sittah_zarooriyyah.makool_mashroob}</li>
                      <li>• Harkat/Sukoon: {soapNote.subjective.asbab_sittah_zarooriyyah.harkat_sukoon_badani}</li>
                      <li>• Naum/Yaqzah: {soapNote.subjective.asbab_sittah_zarooriyyah.naum_yaqzah}</li>
                    </ul>
                  </div>
                </div>

                {/* Objective */}
                <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-3.5 space-y-2">
                  <div className="text-xs font-bold uppercase text-amber-400 tracking-wider">
                    O — Objective (Nabz, Lisan, Baul-o-Baraz)
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs text-slate-300">
                    <div>
                      <span className="text-slate-400">Pulse (Nabz): </span>
                      {soapNote.objective.nabz_examination.speed}, {soapNote.objective.nabz_examination.tension}
                    </div>
                    <div>
                      <span className="text-slate-400">Tongue (Lisan): </span>
                      {soapNote.objective.lisan_examination.color}, {soapNote.objective.lisan_examination.coating}
                    </div>
                    <div>
                      <span className="text-slate-400">Urine (Baul): </span>
                      {soapNote.objective.baul_o_baraz.baul_color}
                    </div>
                    <div>
                      <span className="text-slate-400">Vitals: </span>
                      BP {soapNote.objective.vitals.blood_pressure} • HR {soapNote.objective.vitals.heart_rate}
                    </div>
                  </div>
                </div>

                {/* Assessment */}
                <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-3.5 space-y-2">
                  <div className="text-xs font-bold uppercase text-violet-400 tracking-wider">
                    A — Assessment (Tashkhees-e-Mizaj & Amraz)
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs text-slate-300">
                    <div>
                      <span className="text-slate-400">Dominant Mizaj: </span>
                      <span className="font-semibold text-violet-300">{soapNote.assessment.dominant_mizaj}</span>
                      {" ("}{soapNote.assessment.secondary_mizaj}{")"}
                    </div>
                    <div>
                      <span className="text-slate-400">Primary Pathology: </span>
                      <span className="font-semibold text-slate-200">{soapNote.assessment.primary_unani_diagnosis}</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Stage (Dawr): </span>
                      {soapNote.assessment.dawr_e_marad}
                    </div>
                    <div>
                      <span className="text-slate-400">Quwa Reserve: </span>
                      {soapNote.assessment.quwa_status}
                    </div>
                  </div>
                </div>

                {/* Plan */}
                <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-3.5 space-y-2">
                  <div className="text-xs font-bold uppercase text-emerald-400 tracking-wider">
                    P — Plan (4-Pillar Unani Care Plan)
                  </div>
                  <div className="space-y-1.5 text-xs text-slate-300">
                    <div>
                      <span className="text-emerald-400 font-medium">1. Diet (Ilaj-bil-Ghiza): </span>
                      {soapNote.plan.ilaj_bil_ghiza.join("; ")}
                    </div>
                    <div>
                      <span className="text-emerald-400 font-medium">2. Regimen (Ilaj-bil-Tadbeer): </span>
                      {soapNote.plan.ilaj_bil_tadbeer.join("; ")}
                    </div>
                    <div>
                      <span className="text-emerald-400 font-medium">3. Pharmacotherapy (Ilaj-bil-Dawa): </span>
                      {soapNote.plan.ilaj_bil_dawa.join("; ")}
                    </div>
                    <div>
                      <span className="text-emerald-400 font-medium">4. Follow-up: </span>
                      {soapNote.plan.follow_up}
                    </div>
                  </div>

                  <div className="mt-3 p-2 bg-amber-500/10 border border-amber-500/20 rounded text-[11px] text-amber-300">
                    ⚠️ {soapNote.plan.statutory_notice}
                  </div>
                </div>

                {soapNote.signed_by && (
                  <div className="p-3 bg-emerald-950/30 border border-emerald-800/40 rounded-lg text-xs text-slate-300">
                    <div className="font-semibold text-emerald-400">Clinician Attestation Signature:</div>
                    <div>{soapNote.signed_by} on {soapNote.signed_at}</div>
                    {soapNote.clinician_notes && (
                      <div className="text-slate-400 mt-1 italic">"{soapNote.clinician_notes}"</div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Sign & Lock Modal */}
      {showSignModal && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-lg w-full p-6 space-y-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span>✍️ 21 CFR Part 11 Clinician Sign-off & Lock</span>
            </h3>
            <p className="text-xs text-slate-400">
              Per 21 CFR § 11.50 and statutory medical governance, signing locks this clinical note and appends an immutable block to the cryptographic audit trail.
            </p>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Clinician ID</label>
                <input
                  type="text"
                  value={clinicianId}
                  onChange={(e) => setClinicianId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-slate-200"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Clinician Printed Name</label>
                <input
                  type="text"
                  value={clinicianName}
                  onChange={(e) => setClinicianName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-slate-200"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Professional Role</label>
                <select
                  value={clinicianRole}
                  onChange={(e) => setClinicianRole(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-slate-200"
                >
                  <option value="hakeem">Hakeem (Tabeeb)</option>
                  <option value="clinician">Clinician (MD/BUMS)</option>
                  <option value="doctor">Consultant Physician</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Attestation Notes</label>
                <textarea
                  rows={2}
                  value={clinicianNotes}
                  onChange={(e) => setClinicianNotes(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-slate-200 resize-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setShowSignModal(false)}
                className="px-4 py-2 text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition"
              >
                Cancel
              </button>
              <button
                onClick={handleSignAndLock}
                disabled={isSigning}
                className="px-4 py-2 text-xs bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg shadow transition disabled:opacity-50"
              >
                {isSigning ? "Signing & Hashing..." : "Confirm & Attest (Lock Note)"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
