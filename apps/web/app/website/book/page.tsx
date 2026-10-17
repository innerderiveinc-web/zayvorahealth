"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppointmentService, AppointmentBookingRequest, AppointmentBookingResult } from "@/lib/services/appointmentService";
import { CLINICAL_FACULTY } from "@/lib/cms/doctorsData";

export default function BookAppointmentPage() {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [bookingResult, setBookingResult] = useState<AppointmentBookingResult | null>(null);

  const [formData, setFormData] = useState<AppointmentBookingRequest>({
    fullName: "",
    mobile: "",
    email: "",
    age: 32,
    gender: "Male",
    healthConcern: "Waja-ul-Mafasil (Joint & Knee Pain)",
    consultationType: "In-Clinic OPD",
    preferredDate: new Date(Date.now() + 86400000).toISOString().split("T")[0],
    preferredTime: "10:00 AM – 10:30 AM",
    doctorPreference: "Prof. (Dr.) Mansoor Alam — Ilmul Advia & Chronic Disorders",
    additionalMessage: "",
    hasPreviousReports: false,
    consentAccepted: false,
  });

  const availableSlots = AppointmentService.getAvailableSlots(formData.preferredDate);

  const handleInputChange = (field: keyof AppointmentBookingRequest, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setErrorMessage(null);
  };

  const validateStep = (step: number): boolean => {
    if (step === 1) {
      if (!formData.fullName || formData.fullName.trim().length < 3) {
        setErrorMessage("Please provide your full legal name (at least 3 characters).");
        return false;
      }
      const cleanMobile = formData.mobile.replace(/\D/g, "");
      if (cleanMobile.length < 10) {
        setErrorMessage("Please enter a valid 10-digit mobile number for appointment SMS/WhatsApp updates.");
        return false;
      }
      if (!formData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        setErrorMessage("Please provide a valid email address for your digital consultation receipt.");
        return false;
      }
      if (!formData.age || formData.age < 1 || formData.age > 120) {
        setErrorMessage("Please enter a valid age.");
        return false;
      }
    } else if (step === 2) {
      if (!formData.healthConcern) {
        setErrorMessage("Please select your primary clinical specialty or health concern.");
        return false;
      }
    } else if (step === 3) {
      if (!formData.preferredDate) {
        setErrorMessage("Please choose a preferred consultation date.");
        return false;
      }
      if (!formData.preferredTime) {
        setErrorMessage("Please select an available time slot.");
        return false;
      }
    } else if (step === 4) {
      if (!formData.consentAccepted) {
        setErrorMessage("You must accept the clinical record consent & ABDM/DPDP Act 2023 privacy terms to proceed.");
        return false;
      }
    }
    setErrorMessage(null);
    return true;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep((prev) => Math.min(prev + 1, 4));
    }
  };

  const prevStep = () => {
    setErrorMessage(null);
    setCurrentStep((prev) => Math.max(prev - 1, 1));
  };

  const handleFinalSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateStep(4)) return;

    setIsSubmitting(true);
    setErrorMessage(null);
    try {
      const result = await AppointmentService.bookAppointment(formData);
      setBookingResult(result);
    } catch (err: any) {
      setErrorMessage(err.message || "An unexpected error occurred while scheduling your consultation. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A101D] text-slate-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <Link href="/website" className="hover:text-teal-400 transition">ZAYVORA Health</Link>
            <span>/</span>
            <span className="text-teal-400 font-medium">Book Consultation</span>
          </div>
          <div className="flex items-center gap-2 text-[11px] bg-slate-800/80 px-3 py-1 rounded-full border border-slate-700">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>OPD Clinical Desk Active • Live Teleconsultation</span>
          </div>
        </div>

        {/* Page Header */}
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold tracking-wider text-teal-400 bg-teal-950/60 border border-teal-800/60 uppercase">
            Clinician-Supervised Scheduling
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Schedule Your Integrative Consultation
          </h1>
          <p className="text-sm text-slate-400">
            Direct access to senior Unani clinicians, comprehensive Mizaj constitution assessment, and evidence-guided chronic care protocols.
          </p>
        </div>

        {/* Success Confirmation Card */}
        {bookingResult ? (
          <div className="bg-gradient-to-b from-[#132338] to-[#0D1826] border border-emerald-500/40 rounded-3xl p-6 sm:p-10 shadow-2xl space-y-8 animate-fade-in">
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 border border-emerald-500/50 flex items-center justify-center text-emerald-400 text-3xl">
                ✓
              </div>
              <div>
                <span className="text-xs uppercase font-bold tracking-widest text-emerald-400 bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-800/60">
                  Appointment Confirmed
                </span>
                <h2 className="text-2xl sm:text-3xl font-bold text-white mt-2">
                  Reference: {bookingResult.referenceNumber}
                </h2>
                <p className="text-sm text-slate-300 mt-1">
                  Queue Token Assigned: <strong className="text-teal-300 text-base">{bookingResult.tokenNumber}</strong>
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/80 rounded-2xl p-6 border border-slate-800 text-xs">
              <div className="space-y-3">
                <div>
                  <span className="text-slate-500 block uppercase font-semibold text-[10px]">Patient Name</span>
                  <span className="text-slate-200 font-medium text-sm">{formData.fullName} ({formData.gender}, {formData.age} yrs)</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-semibold text-[10px]">Clinical Specialty</span>
                  <span className="text-slate-200 font-medium">{formData.healthConcern}</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-semibold text-[10px]">Attending Clinician</span>
                  <span className="text-slate-200 font-medium text-teal-400">{bookingResult.doctorName}</span>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <span className="text-slate-500 block uppercase font-semibold text-[10px]">Consultation Mode</span>
                  <span className="text-slate-200 font-medium">{bookingResult.mode}</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-semibold text-[10px]">Date & Time Slot</span>
                  <span className="text-slate-200 font-medium">{bookingResult.scheduledDate} at {bookingResult.scheduledTime}</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-semibold text-[10px]">Venue / Access</span>
                  <span className="text-slate-200 font-medium">{bookingResult.facilityLocation}</span>
                </div>
              </div>
            </div>

            {/* Notification Confirmation Badges */}
            <div className="flex flex-wrap items-center justify-center gap-4 text-xs text-slate-400 pt-2 border-t border-slate-800">
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span>✓</span> SMS Dispatched to {formData.mobile}
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span>✓</span> WhatsApp Confirmation Sent
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span>✓</span> Digital Intake Slip Emailed
              </span>
            </div>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link
                href="/patient"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-center text-sm shadow-lg shadow-teal-900/40 transition"
              >
                Access Patient Portal & Prescriptions →
              </Link>
              <button
                onClick={() => {
                  setBookingResult(null);
                  setCurrentStep(1);
                }}
                className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-center text-sm border border-slate-700 transition"
              >
                Book Another Appointment
              </button>
            </div>
          </div>
        ) : (
          /* Multi-Step Booking Card */
          <div className="bg-[#111A2E] border border-slate-800 rounded-3xl shadow-xl overflow-hidden">
            
            {/* Step Progress Tracker */}
            <div className="bg-[#0C1424] border-b border-slate-800 px-6 py-4">
              <div className="grid grid-cols-4 gap-2 text-center text-xs">
                {[
                  { step: 1, label: "1. Personal Info" },
                  { step: 2, label: "2. Care Specialty" },
                  { step: 3, label: "3. Date & Slot" },
                  { step: 4, label: "4. Consent & Confirm" },
                ].map((s) => (
                  <div
                    key={s.step}
                    className={`py-2 px-1 rounded-lg transition-all ${
                      currentStep === s.step
                        ? "bg-teal-950/80 border border-teal-600/60 text-teal-300 font-bold"
                        : currentStep > s.step
                        ? "text-emerald-400 font-medium"
                        : "text-slate-500"
                    }`}
                  >
                    <span className="block text-[11px] sm:text-xs">
                      {currentStep > s.step ? `✓ ${s.label.split(". ")[1]}` : s.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Error Alert */}
            {errorMessage && (
              <div className="mx-6 mt-6 p-4 rounded-xl bg-rose-950/70 border border-rose-800/80 text-rose-300 text-xs flex items-center gap-3">
                <span className="text-base font-bold">⚠</span>
                <span>{errorMessage}</span>
              </div>
            )}

            {/* Form Steps */}
            <form onSubmit={handleFinalSubmit} className="p-6 sm:p-8 space-y-6">
              
              {/* STEP 1: Personal Info */}
              {currentStep === 1 && (
                <div className="space-y-5 animate-fade-in">
                  <div className="border-b border-slate-800 pb-3">
                    <h3 className="text-lg font-bold text-white">Step 1: Patient Demographic Details</h3>
                    <p className="text-xs text-slate-400">Required for official hospital registration and Ayushman Bharat / ABDM health record.</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Full Legal Name <span className="text-rose-400">*</span>
                      </label>
                      <input
                        type="text"
                        placeholder="e.g. Hamza Farooqi"
                        value={formData.fullName}
                        onChange={(e) => handleInputChange("fullName", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Mobile Number (for SMS & WhatsApp reminders) <span className="text-rose-400">*</span>
                      </label>
                      <input
                        type="tel"
                        placeholder="+91-9876543210"
                        value={formData.mobile}
                        onChange={(e) => handleInputChange("mobile", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Email Address <span className="text-rose-400">*</span>
                      </label>
                      <input
                        type="email"
                        placeholder="patient@example.com"
                        value={formData.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                        required
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-slate-300 font-semibold mb-1.5">Age</label>
                        <input
                          type="number"
                          min="1"
                          max="120"
                          value={formData.age}
                          onChange={(e) => handleInputChange("age", parseInt(e.target.value) || 0)}
                          className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                          required
                        />
                      </div>
                      <div>
                        <label className="block text-slate-300 font-semibold mb-1.5">Gender</label>
                        <select
                          value={formData.gender}
                          onChange={(e) => handleInputChange("gender", e.target.value)}
                          className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                        >
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 2: Clinical Concern & Mode */}
              {currentStep === 2 && (
                <div className="space-y-5 animate-fade-in">
                  <div className="border-b border-slate-800 pb-3">
                    <h3 className="text-lg font-bold text-white">Step 2: Specialty & Care Mode</h3>
                    <p className="text-xs text-slate-400">Match with specialized Unani clinical departments and choose in-person vs digital care.</p>
                  </div>

                  <div className="space-y-4 text-xs">
                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Consultation Mode <span className="text-rose-400">*</span>
                      </label>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <button
                          type="button"
                          onClick={() => handleInputChange("consultationType", "Online Video Consultation")}
                          className={`p-4 rounded-xl border text-left flex flex-col justify-between transition ${
                            formData.consultationType === "Online Video Consultation"
                              ? "bg-teal-950/80 border-teal-500 text-white ring-1 ring-teal-500"
                              : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700"
                          }`}
                        >
                          <div className="font-bold text-sm text-teal-300">📹 Online Video Telehealth</div>
                          <div className="text-[11px] text-slate-400 mt-1">
                            HD encrypted video room. Digital prescription & delivery available pan-India.
                          </div>
                        </button>

                        <button
                          type="button"
                          onClick={() => handleInputChange("consultationType", "In-Clinic OPD")}
                          className={`p-4 rounded-xl border text-left flex flex-col justify-between transition ${
                            formData.consultationType === "In-Clinic OPD"
                              ? "bg-teal-950/80 border-teal-500 text-white ring-1 ring-teal-500"
                              : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700"
                          }`}
                        >
                          <div className="font-bold text-sm text-teal-300">🏥 In-Clinic Physical OPD</div>
                          <div className="text-[11px] text-slate-400 mt-1">
                            ZAYVORA Matab™ Central Care Centre OPD, New Delhi. Physical Nabz palpation & Ilaj-bit-Tadbeer.
                          </div>
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Primary Clinical Specialty / Condition <span className="text-rose-400">*</span>
                      </label>
                      <select
                        value={formData.healthConcern}
                        onChange={(e) => handleInputChange("healthConcern", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                      >
                        <option value="Waja-ul-Mafasil (Joint & Knee Pain)">Waja-ul-Mafasil (Joint & Knee Osteoarthritis / Rheumatology)</option>
                        <option value="Metabolic & Diabetes Care (Ziabetus Shakari)">Metabolic Health & Type-2 Diabetes Care (Ziabetus Shakari)</option>
                        <option value="Liver, Digestive & Gastrointestinal Disorders">Liver, Gut Microbiome & Gastrointestinal Health (Sue-Hazm)</option>
                        <option value="Reproductive Health & Fertility (Uqr)">Reproductive Health, Infertility & Vitality (Uqr)</option>
                        <option value="Chronic Fatigue, Insomnia & Stress (Sahar)">Chronic Fatigue, Neurological Stress & Insomnia (Sahar)</option>
                        <option value="Skin, Psoriasis & Dermatology (Jarb-o-Hikka)">Skin Health, Eczema & Psoriasis (Jarb-o-Hikka)</option>
                        <option value="General Preventive Health & Baseline Mizaj">General Preventive Health & Baseline Mizaj Assessment</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Doctor Preference (Optional)
                      </label>
                      <select
                        value={formData.doctorPreference}
                        onChange={(e) => handleInputChange("doctorPreference", e.target.value)}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                      >
                        <option value="Prof. (Dr.) Mansoor Alam — Ilmul Advia & Chronic Disorders">
                          Prof. (Dr.) Mansoor Alam — Senior Consulting Tabeeb (Ilmul Advia & Chronic Disorders)
                        </option>
                        <option value="Dr. Aisha Siddiqui — Lifestyle, Dietetics & Preventive Care">
                          Dr. Aisha Siddiqui — Tahaffuzi wa Samaji Tibb (Preventive Medicine & Dietetics)
                        </option>
                        <option value="Dr. Tariq Zafar — Ilaj-bit-Tadbeer & Musculoskeletal Therapy">
                          Dr. Tariq Zafar — Musculoskeletal & Regimenal Therapy (Ilaj-bit-Tadbeer)
                        </option>
                        <option value="Dr. Shagufta Parveen — Women's Health & Hormonal Care">
                          Dr. Shagufta Parveen — Niswan wa Qabalat (Gynecology & Endocrine)
                        </option>
                        <option value="Next Available Senior Specialist">
                          Assign Next Available Senior Specialist
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 3: Date & Slot Selection */}
              {currentStep === 3 && (
                <div className="space-y-5 animate-fade-in">
                  <div className="border-b border-slate-800 pb-3">
                    <h3 className="text-lg font-bold text-white">Step 3: Consultation Schedule & Notes</h3>
                    <p className="text-xs text-slate-400">Select an appointment time slot and outline your symptoms or history.</p>
                  </div>

                  <div className="space-y-4 text-xs">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-slate-300 font-semibold mb-1.5">
                          Consultation Date <span className="text-rose-400">*</span>
                        </label>
                        <input
                          type="date"
                          min="2026-09-14"
                          max="2026-10-31"
                          value={formData.preferredDate}
                          onChange={(e) => handleInputChange("preferredDate", e.target.value)}
                          className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-slate-300 font-semibold mb-1.5">
                          Time Slot <span className="text-rose-400">*</span>
                        </label>
                        <select
                          value={formData.preferredTime}
                          onChange={(e) => handleInputChange("preferredTime", e.target.value)}
                          className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                        >
                          {availableSlots.map((slot) => (
                            <option key={slot} value={slot}>{slot}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="block text-slate-300 font-semibold mb-1.5">
                        Chief Symptoms & Duration
                      </label>
                      <textarea
                        rows={3}
                        placeholder="Briefly describe your symptoms, how long you've experienced them, and any previous medications taken..."
                        value={formData.additionalMessage}
                        onChange={(e) => handleInputChange("additionalMessage", e.target.value)}
                        className="w-full p-3.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                      />
                    </div>

                    <div className="flex items-center gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                      <input
                        type="checkbox"
                        id="prevReports"
                        checked={formData.hasPreviousReports}
                        onChange={(e) => handleInputChange("hasPreviousReports", e.target.checked)}
                        className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                      />
                      <label htmlFor="prevReports" className="text-slate-300 text-xs cursor-pointer">
                        I have prior blood tests, imaging reports, or prescriptions to upload during clinical intake
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 4: Review, Consent & Confirm */}
              {currentStep === 4 && (
                <div className="space-y-5 animate-fade-in">
                  <div className="border-b border-slate-800 pb-3">
                    <h3 className="text-lg font-bold text-white">Step 4: Review & Clinical Consent</h3>
                    <p className="text-xs text-slate-400">Verify your consultation details and accept clinical intake terms.</p>
                  </div>

                  {/* Summary Box */}
                  <div className="bg-slate-900/90 rounded-2xl p-5 border border-slate-800 text-xs space-y-3">
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase font-semibold">Patient</span>
                        <span className="font-bold text-white">{formData.fullName} ({formData.gender}, {formData.age})</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase font-semibold">Contact</span>
                        <span className="font-bold text-white">{formData.mobile}</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800">
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase font-semibold">Specialty / Program</span>
                        <span className="text-teal-300 font-medium">{formData.healthConcern}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase font-semibold">Mode</span>
                        <span className="text-white font-medium">{formData.consultationType}</span>
                      </div>
                    </div>
                    <div className="pt-2 border-t border-slate-800">
                      <span className="text-slate-500 block text-[10px] uppercase font-semibold">Schedule</span>
                      <span className="text-white font-medium">{formData.preferredDate} at {formData.preferredTime}</span>
                    </div>
                  </div>

                  {/* Consent Checkbox */}
                  <div className="p-4 rounded-xl bg-teal-950/40 border border-teal-800/60 space-y-3 text-xs">
                    <div className="flex items-start gap-3">
                      <input
                        type="checkbox"
                        id="consent"
                        checked={formData.consentAccepted}
                        onChange={(e) => handleInputChange("consentAccepted", e.target.checked)}
                        className="mt-0.5 rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                        required
                      />
                      <label htmlFor="consent" className="text-slate-300 text-xs leading-relaxed cursor-pointer">
                        I hereby consent to integrative Unani medical consultation and authorize ZAYVORA Health clinicians to access my provided health details. I agree to receive appointment alerts via SMS and WhatsApp in accordance with the Digital Personal Data Protection Act (DPDP 2023) and ABDM guidelines.
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {/* Step Navigation Controls */}
              <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                {currentStep > 1 ? (
                  <button
                    type="button"
                    onClick={prevStep}
                    className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
                  >
                    ← Back
                  </button>
                ) : (
                  <Link
                    href="/website"
                    className="text-xs text-slate-400 hover:text-white transition"
                  >
                    ← Return to Homepage
                  </Link>
                )}

                {currentStep < 4 ? (
                  <button
                    type="button"
                    onClick={nextStep}
                    className="px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition flex items-center gap-2"
                  >
                    Continue to Next Step →
                  </button>
                ) : (
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="px-8 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 disabled:text-slate-600 text-white text-xs font-bold transition shadow-lg shadow-teal-900/30 flex items-center gap-2"
                  >
                    {isSubmitting ? (
                      <>
                        <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                        <span>Securing Slot...</span>
                      </>
                    ) : (
                      <span>Confirm & Book Appointment →</span>
                    )}
                  </button>
                )}
              </div>
            </form>
          </div>
        )}

        {/* Clinical Assurance & Hospital Footer Note */}
        <div className="text-center text-xs text-slate-400 space-y-1">
          <p>
            Emergency? For acute emergencies, call national helpline 112 or visit the nearest emergency trauma center immediately.
          </p>
          <p className="text-slate-500">
            OPD Services coordinated at ZAYVORA Healthcare System - Central Hospital, New Delhi • Ministry of AYUSH / NCISM Act 2020 Registered Clinicians
          </p>
        </div>

      </div>
    </div>
  );
}
