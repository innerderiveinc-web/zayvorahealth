"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";

export default function ClinicianApplyPage() {
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [applicationId, setApplicationId] = useState("");

  const [formData, setFormData] = useState({
    // Step 1: Personal
    fullName: "",
    email: "",
    phone: "",
    dob: "1988-06-15",
    gender: "Male",
    // Step 2: Qualification
    qualification: "BUMS (Bachelor of Unani Medicine & Surgery)",
    university: "Aligarh Muslim University (AMU), AKTC",
    gradYear: "2012",
    pgSpecialty: "MD (Ilm-ul-Adwiya)",
    // Step 3: Statutory NCISM
    regNumber: "",
    councilName: "National Commission for Indian System of Medicine (NCISM)",
    regState: "Delhi",
    regYear: "2013",
    // Step 4: Clinical Scope
    primaryAxis: "Waja-ul-Mafasil & Musculoskeletal",
    tadbeerCompetence: true,
    nuskhaPrescribing: true,
    // Step 5: Practice Setting
    facilityType: "Private Matab / OPD Care Centre",
    practiceCity: "New Delhi",
    telehealthEnabled: true,
    // Step 6: Documents
    degreeProofName: "degree_bums_cert.pdf",
    councilProofName: "ncism_registration_cert.pdf",
    idProofName: "aadhaar_verified.pdf",
    // Step 7: 21 CFR Part 11
    signaturePasscode: "",
    acceptDigitalSeal: true,
    // Step 8: Ethics & Statutory Undertaking
    undertakeNCISM: true,
    undertakeZeroCommercialBias: true
  });

  const update = (field: string, val: any) => {
    setFormData(prev => ({ ...prev, [field]: val }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (step < 8) {
      setStep(step + 1);
      return;
    }
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      const generatedId = `APP-NCISM-2026-${Math.floor(10000 + Math.random() * 90000)}`;
      setApplicationId(generatedId);
      setSubmitted(true);
    }, 1200);
  };

  const stepsMeta = [
    { num: 1, label: "Identity" },
    { num: 2, label: "Education" },
    { num: 3, label: "NCISM Council" },
    { num: 4, label: "Clinical Scope" },
    { num: 5, label: "Practice Setting" },
    { num: 6, label: "Documents" },
    { num: 7, label: "21 CFR Part 11" },
    { num: 8, label: "Governance" }
  ];

  return (
    <PublicWebsiteShell>
      <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-950/70 border border-teal-800 text-teal-400 text-xs font-mono mb-3">
            <span>⚖️ Statutory Regulatory Gate</span>
            <span>•</span>
            <span>NCISM Act 2020 Compliant</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Clinician Credentialing & Onboarding
          </h1>
          <p className="mt-2 text-sm text-slate-400 max-w-xl mx-auto">
            Authorized portal for Unani medical practitioners, Hakeems, and clinical researchers seeking prescribing privileges on ZAYVORA Health OS™.
          </p>
        </div>

        {/* Stepper Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between overflow-x-auto pb-2">
            {stepsMeta.map((s) => (
              <div key={s.num} className="flex flex-col items-center flex-1 min-w-[70px]">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition ${
                    step === s.num
                      ? "bg-teal-500 text-slate-950 ring-4 ring-teal-500/20"
                      : step > s.num
                      ? "bg-teal-900 text-teal-300 border border-teal-700"
                      : "bg-slate-900 text-slate-500 border border-slate-800"
                  }`}
                >
                  {step > s.num ? "✓" : s.num}
                </div>
                <span className={`text-[10px] mt-1 font-medium text-center ${step === s.num ? "text-teal-400" : "text-slate-500"}`}>
                  {s.label}
                </span>
              </div>
            ))}
          </div>
          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden mt-3">
            <div
              className="bg-gradient-to-r from-teal-600 to-emerald-400 h-full transition-all duration-300"
              style={{ width: `${(step / 8) * 100}%` }}
            ></div>
          </div>
        </div>

        {submitted ? (
          <div className="bg-[#0D1527] border border-slate-800 rounded-3xl p-8 sm:p-12 text-center space-y-6 shadow-2xl">
            <div className="w-16 h-16 rounded-full bg-teal-900/50 border border-teal-600 text-teal-300 flex items-center justify-center text-3xl mx-auto">
              ✓
            </div>
            <h2 className="text-2xl font-bold text-white">Application Successfully Lodged</h2>
            <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 inline-block font-mono text-sm text-teal-400">
              Tracking Ref: {applicationId}
            </div>
            <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
              Your credentials have been submitted to the ZAYVORA Clinical Governance & Credentialing Committee. In accordance with NCISM verification protocol, our statutory officer verifies council registry records within 48-72 business hours.
            </p>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 text-left max-w-md mx-auto space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-500">Applicant:</span>
                <span className="font-semibold">{formData.fullName}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Council Reg:</span>
                <span className="font-semibold">{formData.regNumber} ({formData.regState})</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Privilege Scope:</span>
                <span className="font-semibold">{formData.primaryAxis}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Review SLA:</span>
                <span className="text-emerald-400">48-72 Hours</span>
              </div>
            </div>
            <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/doctor/login" className="px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition">
                Return to Doctor Portal →
              </Link>
              <Link href="/" className="px-6 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">
                Return to Homepage
              </Link>
            </div>
          </div>
        ) : (
          <div className="bg-[#0D1527] border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Step 1: Personal Details */}
              {step === 1 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>1.</span> Personal & Practitioner Identity
                  </h3>
                  <p className="text-xs text-slate-400">
                    Provide legal practitioner identification details matching your government identity documents.
                  </p>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Full Legal Name (as on Council Registration) *</label>
                    <input
                      type="text"
                      required
                      value={formData.fullName}
                      onChange={e => update("fullName", e.target.value)}
                      placeholder="e.g. Dr. Hakeem Ahmad Tariq"
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Official Email Address *</label>
                      <input
                        type="email"
                        required
                        value={formData.email}
                        onChange={e => update("email", e.target.value)}
                        placeholder="practitioner@clinic.com"
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Direct Mobile Number (for 2FA) *</label>
                      <input
                        type="tel"
                        required
                        value={formData.phone}
                        onChange={e => update("phone", e.target.value)}
                        placeholder="+91-9876543210"
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Date of Birth</label>
                      <input
                        type="date"
                        value={formData.dob}
                        onChange={e => update("dob", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Gender</label>
                      <select
                        value={formData.gender}
                        onChange={e => update("gender", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      >
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 2: Qualifications */}
              {step === 2 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>2.</span> Primary Medical & Tibbi Qualification
                  </h3>
                  <p className="text-xs text-slate-400">
                    Degrees recognized under the National Commission for Indian System of Medicine (NCISM) Act 2020.
                  </p>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Degree *</label>
                    <select
                      value={formData.qualification}
                      onChange={e => update("qualification", e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    >
                      <option value="BUMS (Bachelor of Unani Medicine & Surgery)">BUMS (Bachelor of Unani Medicine & Surgery)</option>
                      <option value="MD (Unani) / Mahir-e-Tibb">MD (Unani) / Mahir-e-Tibb</option>
                      <option value="MS (Unani)">MS (Unani)</option>
                      <option value="Fazil-ut-Tibb wa Jarahat">Fazil-ut-Tibb wa Jarahat (State recognized)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">University / College / Institution *</label>
                    <input
                      type="text"
                      required
                      value={formData.university}
                      onChange={e => update("university", e.target.value)}
                      placeholder="e.g. Ajmal Khan Tibbiya College, AMU, Aligarh"
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Graduation Year</label>
                      <input
                        type="text"
                        value={formData.gradYear}
                        onChange={e => update("gradYear", e.target.value)}
                        placeholder="2012"
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Postgraduate Specialization (if any)</label>
                      <input
                        type="text"
                        value={formData.pgSpecialty}
                        onChange={e => update("pgSpecialty", e.target.value)}
                        placeholder="e.g. Moalejat, Ilaj-bit-Tadbeer, Ilm-ul-Adwiya"
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Step 3: Statutory NCISM Details */}
              {step === 3 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>3.</span> Statutory NCISM / State Medical Board Registration
                  </h3>
                  <p className="text-xs text-slate-400">
                    Prescribing authority is strictly fail-closed: credentials are cross-referenced with official state registries.
                  </p>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Registration Certificate Number *</label>
                    <input
                      type="text"
                      required
                      value={formData.regNumber}
                      onChange={e => update("regNumber", e.target.value)}
                      placeholder="e.g. DEL-UNANI-2018-04421"
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">State of Registration *</label>
                      <select
                        value={formData.regState}
                        onChange={e => update("regState", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      >
                        <option value="Delhi">Delhi</option>
                        <option value="Uttar Pradesh">Uttar Pradesh</option>
                        <option value="Telangana">Telangana</option>
                        <option value="Maharashtra">Maharashtra</option>
                        <option value="Karnataka">Karnataka</option>
                        <option value="Bihar">Bihar</option>
                        <option value="Jammu & Kashmir">Jammu & Kashmir</option>
                        <option value="Other">Other State Council</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Year of First Registration</label>
                      <input
                        type="text"
                        value={formData.regYear}
                        onChange={e => update("regYear", e.target.value)}
                        placeholder="2013"
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Registering Body</label>
                    <input
                      type="text"
                      value={formData.councilName}
                      onChange={e => update("councilName", e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    />
                  </div>
                </div>
              )}

              {/* Step 4: Clinical Scope */}
              {step === 4 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>4.</span> Organ-Axis Privileging & Regimenal Scope
                  </h3>
                  <p className="text-xs text-slate-400">
                    Define clinical focus areas and clinical modalities requested under your institutional license.
                  </p>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Clinical Domain *</label>
                    <select
                      value={formData.primaryAxis}
                      onChange={e => update("primaryAxis", e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    >
                      <option value="Waja-ul-Mafasil & Musculoskeletal">Waja-ul-Mafasil & Musculoskeletal (Joints & Cartilage)</option>
                      <option value="Meda & Amaa (Gastroenterology & Metabolic)">Meda & Amaa (Gastroenterology & Metabolic)</option>
                      <option value="Dimagh & Aasab (Neurology & Stress)">Dimagh & Aasab (Neurology & Stress)</option>
                      <option value="Jigar & Tihal (Hepatology & Splenic Care)">Jigar & Tihal (Hepatology & Splenic Care)</option>
                      <option value="Riya & Sadr (Pulmonology)">Riya & Sadr (Pulmonology)</option>
                      <option value="Niswan & Qabalat (Gynaecology & Obstetrics)">Niswan & Qabalat (Gynaecology & Obstetrics)</option>
                      <option value="General Tibb & Constitutional Mizaj">General Tibb & Constitutional Mizaj Balancing</option>
                    </select>
                  </div>
                  <div className="space-y-2 pt-2">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.tadbeerCompetence}
                        onChange={e => update("tadbeerCompetence", e.target.checked)}
                        className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                      />
                      <span>Ilaj-bit-Tadbeer Certification (Hijama, Fasd, Dal'k, Hammam, Tareeq)</span>
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.nuskhaPrescribing}
                        onChange={e => update("nuskhaPrescribing", e.target.checked)}
                        className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                      />
                      <span>Compound Murakkabat & Schedule E(1) Mudabbar Authorized Prescriber</span>
                    </label>
                  </div>
                </div>
              )}

              {/* Step 5: Practice Setting */}
              {step === 5 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>5.</span> Practice Setting & Facility Affiliation
                  </h3>
                  <p className="text-xs text-slate-400">
                    Indicate the clinical facilities where you currently see patients or wish to consult.
                  </p>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Facility Practice Type</label>
                    <select
                      value={formData.facilityType}
                      onChange={e => update("facilityType", e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    >
                      <option value="Private Matab / OPD Care Centre">Private Matab / OPD Care Centre</option>
                      <option value="Hospital AYUSH Department">Hospital AYUSH Department</option>
                      <option value="Academic Institution Clinic">Academic Institution Clinic</option>
                      <option value="ZAYVORA Virtual Care Matab (Telemedicine)">ZAYVORA Virtual Care Matab (Telemedicine)</option>
                    </select>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Practice City</label>
                      <input
                        type="text"
                        value={formData.practiceCity}
                        onChange={e => update("practiceCity", e.target.value)}
                        placeholder="e.g. New Delhi"
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Virtual Consultation</label>
                      <select
                        value={formData.telehealthEnabled ? "yes" : "no"}
                        onChange={e => update("telehealthEnabled", e.target.value === "yes")}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                      >
                        <option value="yes">Offer QSURA Telehealth Consultations</option>
                        <option value="no">Physical In-Clinic Only</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 6: Document Verification Dossier */}
              {step === 6 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>6.</span> Document Verification Dossier
                  </h3>
                  <p className="text-xs text-slate-400">
                    Upload scanned high-resolution copies for statutory council record cross-referencing.
                  </p>
                  <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-white block">Degree Certificate (BUMS / MD)</span>
                        <span className="text-[11px] text-slate-500">{formData.degreeProofName}</span>
                      </div>
                      <span className="px-2.5 py-1 rounded bg-teal-950 text-teal-400 border border-teal-800 text-[10px]">
                        Attached (Demo)
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs border-t border-slate-800/60 pt-3">
                      <div>
                        <span className="font-semibold text-white block">State / NCISM Registration Certificate</span>
                        <span className="text-[11px] text-slate-500">{formData.councilProofName}</span>
                      </div>
                      <span className="px-2.5 py-1 rounded bg-teal-950 text-teal-400 border border-teal-800 text-[10px]">
                        Attached (Demo)
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs border-t border-slate-800/60 pt-3">
                      <div>
                        <span className="font-semibold text-white block">Government Photo Identity (Aadhaar / PAN)</span>
                        <span className="text-[11px] text-slate-500">{formData.idProofName}</span>
                      </div>
                      <span className="px-2.5 py-1 rounded bg-teal-950 text-teal-400 border border-teal-800 text-[10px]">
                        Attached (Demo)
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 7: 21 CFR Part 11 Digital Signature */}
              {step === 7 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>7.</span> 21 CFR Part 11 Digital Signature Setup
                  </h3>
                  <p className="text-xs text-slate-400">
                    Under statutory clinical governance, all electronic prescriptions (Nuskhas) must be digitally sealed with a dual-factor cryptographic key.
                  </p>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Create 6-Digit Clinical Signing PIN *</label>
                    <input
                      type="password"
                      maxLength={6}
                      required
                      value={formData.signaturePasscode}
                      onChange={e => update("signaturePasscode", e.target.value)}
                      placeholder="••••••"
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm font-mono tracking-widest focus:outline-none focus:border-teal-500"
                    />
                    <p className="text-[10px] text-slate-500 mt-1">
                      You will be asked for this PIN to digitally sign and commit every Nuskha to the tamper-evident Merkle audit log.
                    </p>
                  </div>
                  <div className="p-3 rounded-xl bg-teal-950/40 border border-teal-800/60 flex items-start gap-2.5">
                    <input
                      type="checkbox"
                      id="digitalSealConsent"
                      checked={formData.acceptDigitalSeal}
                      onChange={e => update("acceptDigitalSeal", e.target.checked)}
                      className="mt-0.5 rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                      required
                    />
                    <label htmlFor="digitalSealConsent" className="text-slate-300 text-[11px] leading-relaxed cursor-pointer">
                      I acknowledge that digital signatures generated through this credential carry identical legal authority to physical ink signatures under the Information Technology Act 2000 and 21 CFR Part 11 electronic records framework.
                    </label>
                  </div>
                </div>
              )}

              {/* Step 8: Ethics & Statutory Undertaking */}
              {step === 8 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>8.</span> Ethical Code & Statutory Undertaking
                  </h3>
                  <p className="text-xs text-slate-400">
                    Final regulatory agreement pursuant to the NCISM Act 2020 and Drugs & Magic Remedies Act.
                  </p>
                  <div className="space-y-3 p-4 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-300">
                    <label className="flex items-start gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.undertakeNCISM}
                        onChange={e => update("undertakeNCISM", e.target.checked)}
                        className="mt-0.5 rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                        required
                      />
                      <span>I solemnize that I hold a valid, un-revoked registration under NCISM / State Medical Board and will practice strictly within classical Unani posology and ethical guidelines.</span>
                    </label>
                    <label className="flex items-start gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.undertakeZeroCommercialBias}
                        onChange={e => update("undertakeZeroCommercialBias", e.target.checked)}
                        className="mt-0.5 rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                        required
                      />
                      <span>I commit to zero commercial bias: AI copilot suggestions will remain non-binding clinical aids, and clinical decision authority rests 100% on my professional scrutiny.</span>
                    </label>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-6 border-t border-slate-800">
                {step > 1 ? (
                  <button
                    type="button"
                    onClick={() => setStep(step - 1)}
                    className="px-5 py-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition"
                  >
                    ← Previous Step
                  </button>
                ) : (
                  <div></div>
                )}
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:brightness-110 text-white text-xs font-bold transition shadow-lg shadow-teal-900/40 flex items-center gap-2"
                >
                  {submitting ? (
                    <>
                      <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                      <span>Submitting Dossier...</span>
                    </>
                  ) : step === 8 ? (
                    <span>Submit NCISM Credential Application ✓</span>
                  ) : (
                    <span>Continue to Step {step + 1} →</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </PublicWebsiteShell>
  );
}
