"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { CLINICAL_TEAM, Clinician } from "@/lib/cms/doctorsData";
import { AppointmentService, AppointmentBookingRequest, AppointmentBookingResult } from "@/lib/services/appointmentService";

function BookContent() {
  const searchParams = useSearchParams();
  const initialCondition = searchParams.get("condition") || searchParams.get("concern") || "";
  const initialDoctorId = searchParams.get("doctor") || "";

  const [step, setStep] = useState<number>(1);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [bookingResult, setBookingResult] = useState<AppointmentBookingResult | null>(null);

  const [formData, setFormData] = useState<AppointmentBookingRequest>({
    fullName: "",
    mobile: "",
    email: "",
    age: 35,
    gender: "Male",
    healthConcern: initialCondition ? `Condition: ${initialCondition}` : "General Constitutional Assessment",
    consultationType: "In-Clinic OPD",
    preferredDate: new Date(Date.now() + 86400000).toISOString().split("T")[0],
    preferredTime: "10:00 AM – 10:30 AM",
    doctorPreference: "",
    additionalMessage: "",
    hasPreviousReports: false,
    consentAccepted: false,
  });

  // Pre-select doctor if passed
  useEffect(() => {
    if (initialDoctorId) {
      const matched = CLINICAL_TEAM.find((d) => d.id === initialDoctorId);
      if (matched) {
        setFormData((prev) => ({
          ...prev,
          doctorPreference: `${matched.name} (${matched.specialty})`,
        }));
      }
    }
  }, [initialDoctorId]);

  const availableSlots = AppointmentService.getAvailableSlots(formData.preferredDate);

  const handleFieldChange = (field: keyof AppointmentBookingRequest, val: any) => {
    setFormData((prev) => ({ ...prev, [field]: val }));
    setErrorMessage(null);
  };

  const validateCurrentStep = (): boolean => {
    if (step === 1) {
      if (!formData.consultationType) {
        setErrorMessage("Please select your consultation mode.");
        return false;
      }
    } else if (step === 2) {
      if (!formData.healthConcern || formData.healthConcern.trim().length < 3) {
        setErrorMessage("Please describe or select your primary health concern.");
        return false;
      }
    } else if (step === 3) {
      if (!formData.preferredDate) {
        setErrorMessage("Please select a preferred date.");
        return false;
      }
      if (!formData.preferredTime) {
        setErrorMessage("Please choose an available appointment slot.");
        return false;
      }
    } else if (step === 4) {
      if (!formData.fullName || formData.fullName.trim().length < 3) {
        setErrorMessage("Please enter your full legal name (at least 3 characters).");
        return false;
      }
      const cleanMobile = formData.mobile.replace(/\D/g, "");
      if (cleanMobile.length < 10) {
        setErrorMessage("Please provide a valid 10-digit mobile number for appointment tokens.");
        return false;
      }
      if (!formData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        setErrorMessage("Please provide a valid email address for receipt and health records.");
        return false;
      }
    } else if (step === 5) {
      if (!formData.consentAccepted) {
        setErrorMessage("You must accept the DPDP Act 2023 health data consent to complete booking.");
        return false;
      }
    }
    setErrorMessage(null);
    return true;
  };

  const handleNext = () => {
    if (validateCurrentStep()) {
      setStep((prev) => Math.min(prev + 1, 5));
    }
  };

  const handlePrev = () => {
    setErrorMessage(null);
    setStep((prev) => Math.max(prev - 1, 1));
  };

  const handleSubmitBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateCurrentStep()) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const result = await AppointmentService.bookAppointment(formData);
      setBookingResult(result);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to confirm booking. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Clinician-Led Care Intake"
        title="Schedule a Clinical Consultation"
        subtitle="Consult with qualified Unani physicians registered under the NCISM Act 2020. Select in-person Matab™ visits or encrypted WebRTC teleconsultation."
        breadcrumbs={[
          { label: "Book Consultation" }
        ]}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Urgent Care Alert */}
        <div className="mb-8 p-4 rounded-2xl bg-[#FEF2F2] border border-[#FCA5A5] flex items-center justify-between text-xs">
          <div className="flex items-center gap-2.5 text-[#991B1B]">
            <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-[#DC2626] shrink-0" />
            <span>
              <strong>Emergency Care Note:</strong> ZAYVORA is for elective outpatient care. If experiencing chest pain, acute breathlessness, or severe trauma, call <strong>112</strong> immediately.
            </span>
          </div>
          <span className="px-2 py-0.5 rounded bg-[#DC2626] text-white font-bold text-[10px] shrink-0 hidden sm:inline">
            Call 112
          </span>
        </div>

        {bookingResult ? (
          /* Confirmation State */
          <div className="bg-white rounded-3xl border border-[#C8E6C9] p-8 shadow-sm space-y-6">
            <div className="w-14 h-14 rounded-2xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332] mx-auto">
              <HealthcareIcon name="check" className="w-8 h-8 text-[#2D6A4F]" />
            </div>

            <div className="text-center space-y-2">
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#E8F5E9] text-[#1B4332]">
                Booking Confirmed
              </span>
              <h2 className="text-2xl font-extrabold text-[#0F172A]">
                Appointment Token #{bookingResult.tokenNumber}
              </h2>
              <p className="text-xs text-[#64748B]">
                Reference ID: <span className="font-mono font-bold text-[#0F172A]">{bookingResult.referenceNumber}</span>
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-[#64748B] block text-[11px]">Patient Name</span>
                <span className="font-bold text-[#0F172A]">{formData.fullName}</span>
              </div>
              <div>
                <span className="text-[#64748B] block text-[11px]">Consultation Mode</span>
                <span className="font-bold text-[#0F172A]">{bookingResult.mode}</span>
              </div>
              <div>
                <span className="text-[#64748B] block text-[11px]">Scheduled Date &amp; Time</span>
                <span className="font-bold text-[#0F172A]">{bookingResult.scheduledDate} at {bookingResult.scheduledTime}</span>
              </div>
              <div>
                <span className="text-[#64748B] block text-[11px]">Assigned Clinician</span>
                <span className="font-bold text-[#0F172A]">{bookingResult.doctorName}</span>
              </div>
              <div className="sm:col-span-2">
                <span className="text-[#64748B] block text-[11px]">Facility Location / Link</span>
                <span className="font-bold text-[#1B4332]">{bookingResult.facilityLocation}</span>
              </div>
            </div>

            {/* Preparation Checklist */}
            <div className="p-4 rounded-2xl bg-white border border-[#E2E8F0] space-y-2 text-xs">
              <h4 className="font-bold text-[#0F172A]">Consultation Preparation Checklist:</h4>
              <ul className="space-y-1 text-[#64748B] list-disc list-inside">
                <li>Please bring or upload any recent blood test reports or imaging records from the last 6 months.</li>
                <li>Keep a list of all current prescription allopathic and herbal medicines handy.</li>
                <li>For in-person pulse assessment (Nabz), avoid heavy meals or caffeinated beverages 2 hours prior.</li>
              </ul>
            </div>

            <div className="pt-2 flex flex-col sm:flex-row gap-3 justify-center">
              <Link
                href="/patient"
                className="px-6 py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-semibold text-xs text-center transition shadow-sm"
              >
                Access My ZAYVORA™ Patient Portal
              </Link>
              <button
                onClick={() => {
                  setBookingResult(null);
                  setStep(1);
                }}
                className="px-5 py-3 rounded-xl bg-[#FAFAF7] hover:bg-[#E2E8F0] text-[#0F172A] font-semibold text-xs transition"
              >
                Book Another Appointment
              </button>
            </div>
          </div>
        ) : (
          /* Multi-Step Intake Form */
          <div className="bg-white rounded-3xl border border-[#E2E8F0] p-6 sm:p-8 shadow-sm space-y-8">
            
            {/* Step Progress Indicator */}
            <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4">
              {[
                { s: 1, label: "Care Mode" },
                { s: 2, label: "Concern" },
                { s: 3, label: "Slot" },
                { s: 4, label: "Details" },
                { s: 5, label: "Confirm" }
              ].map((item) => (
                <div key={item.s} className="flex items-center gap-2">
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition ${
                      step === item.s
                        ? "bg-[#1B4332] text-white"
                        : step > item.s
                        ? "bg-[#E8F5E9] text-[#2D6A4F]"
                        : "bg-[#F1F5F9] text-[#94A3B8]"
                    }`}
                  >
                    {step > item.s ? "✓" : item.s}
                  </div>
                  <span
                    className={`text-xs font-medium hidden md:inline ${
                      step === item.s ? "text-[#0F172A] font-bold" : "text-[#64748B]"
                    }`}
                  >
                    {item.label}
                  </span>
                </div>
              ))}
            </div>

            {errorMessage && (
              <div className="p-4 rounded-xl bg-[#FEF2F2] border border-[#FCA5A5] text-xs text-[#991B1B] flex items-center gap-2">
                <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-[#DC2626] shrink-0" />
                <span>{errorMessage}</span>
              </div>
            )}

            <form onSubmit={handleSubmitBooking}>
              {/* ── STEP 1: CARE MODE ─────────────────────────────────── */}
              {step === 1 && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-base font-bold text-[#0F172A]">Select Consultation Mode</h3>
                    <p className="text-xs text-[#64748B]">Choose whether you prefer an in-person clinical visit or a virtual teleconsultation.</p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <button
                      type="button"
                      onClick={() => handleFieldChange("consultationType", "In-Clinic OPD")}
                      className={`p-5 rounded-2xl border text-left transition ${
                        formData.consultationType === "In-Clinic OPD"
                          ? "border-[#1B4332] bg-[#E8F5E9]/40 ring-1 ring-[#1B4332]"
                          : "border-[#E2E8F0] hover:border-[#CBD5E1] bg-[#FAFAF7]"
                      }`}
                    >
                      <div className="w-9 h-9 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332] mb-3">
                        <HealthcareIcon name="building" className="w-5 h-5" />
                      </div>
                      <h4 className="text-sm font-bold text-[#0F172A]">In-Clinic Matab™ OPD</h4>
                      <p className="text-xs text-[#64748B] mt-1 leading-relaxed">
                        Complete physical examination, tactile 10-Ajnas pulse (Nabz) evaluation, and on-site pharmacy dispensing in Delhi, Mumbai, or Hyderabad.
                      </p>
                      <span className="mt-3 inline-block text-[11px] font-bold text-[#1B4332]">
                        Consultation Fee: ₹800
                      </span>
                    </button>

                    <button
                      type="button"
                      onClick={() => handleFieldChange("consultationType", "Online Video Consultation")}
                      className={`p-5 rounded-2xl border text-left transition ${
                        formData.consultationType === "Online Video Consultation"
                          ? "border-[#1B4332] bg-[#E8F5E9]/40 ring-1 ring-[#1B4332]"
                          : "border-[#E2E8F0] hover:border-[#CBD5E1] bg-[#FAFAF7]"
                      }`}
                    >
                      <div className="w-9 h-9 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332] mb-3">
                        <HealthcareIcon name="activity" className="w-5 h-5" />
                      </div>
                      <h4 className="text-sm font-bold text-[#0F172A]">Encrypted Video Teleconsultation</h4>
                      <p className="text-xs text-[#64748B] mt-1 leading-relaxed">
                        End-to-end encrypted WebRTC virtual consultation. Prescriptions are cryptographically signed and dispatched to your home.
                      </p>
                      <span className="mt-3 inline-block text-[11px] font-bold text-[#1B4332]">
                        Consultation Fee: ₹650
                      </span>
                    </button>
                  </div>
                </div>
              )}

              {/* ── STEP 2: PRIMARY CLINICAL CONCERN ──────────────────── */}
              {step === 2 && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-base font-bold text-[#0F172A]">Primary Health Concern</h3>
                    <p className="text-xs text-[#64748B]">Select the clinical specialty that best reflects your current health requirement.</p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {[
                      "Gastrointestinal & Digestive (Su-e-Hazm)",
                      "Musculoskeletal & Joint Pain (Waja-ul-Mafasil)",
                      "Cardiometabolic & Lipid Management",
                      "Endocrine & Diabetes Support (Ziabetes)",
                      "Women's Hormonal & Pelvic Health (PCOS)",
                      "Men's Vitality & Reproductive Health",
                      "Sleep Architecture & Chronic Stress",
                      "Hepatic Axis & Liver Health (Kabid)",
                      "Respiratory & Chronic Bronchial Allergy",
                      "General Preventive Mizaj Assessment"
                    ].map((concern) => (
                      <button
                        key={concern}
                        type="button"
                        onClick={() => handleFieldChange("healthConcern", concern)}
                        className={`p-3.5 rounded-xl border text-left text-xs transition ${
                          formData.healthConcern === concern
                            ? "border-[#1B4332] bg-[#E8F5E9] font-bold text-[#1B4332]"
                            : "border-[#E2E8F0] hover:border-[#CBD5E1] bg-[#FAFAF7] text-[#334155]"
                        }`}
                      >
                        {concern}
                      </button>
                    ))}
                  </div>

                  <div className="space-y-2 pt-2">
                    <label className="block text-xs font-bold text-[#0F172A]">
                      Describe your main symptoms or questions (Optional):
                    </label>
                    <textarea
                      rows={3}
                      value={formData.additionalMessage || ""}
                      onChange={(e) => handleFieldChange("additionalMessage", e.target.value)}
                      placeholder="e.g. Chronic bloating after meals for 3 months, stiffness in morning..."
                      className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                    />
                  </div>
                </div>
              )}

              {/* ── STEP 3: DATE & TIME SLOT ───────────────────────────── */}
              {step === 3 && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-base font-bold text-[#0F172A]">Choose Appointment Slot</h3>
                    <p className="text-xs text-[#64748B]">Select your preferred date and convenient time window.</p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-[#0F172A] mb-1.5">
                        Consultation Date:
                      </label>
                      <input
                        type="date"
                        min={new Date().toISOString().split("T")[0]}
                        value={formData.preferredDate}
                        onChange={(e) => handleFieldChange("preferredDate", e.target.value)}
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#0F172A] mb-1.5">
                        Preferred Clinician:
                      </label>
                      <select
                        value={formData.doctorPreference}
                        onChange={(e) => handleFieldChange("doctorPreference", e.target.value)}
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      >
                        <option value="">Next Available Specialized Clinician</option>
                        {CLINICAL_TEAM.map((doc) => (
                          <option key={doc.id} value={`${doc.name} (${doc.specialty})`}>
                            {doc.name} — {doc.specialty}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="block text-xs font-bold text-[#0F172A]">
                      Available Time Slots for {formData.preferredDate}:
                    </label>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      {availableSlots.map((slot) => (
                        <button
                          key={slot}
                          type="button"
                          onClick={() => handleFieldChange("preferredTime", slot)}
                          className={`p-2.5 rounded-xl border text-center text-xs transition ${
                            formData.preferredTime === slot
                              ? "border-[#1B4332] bg-[#1B4332] text-white font-bold"
                              : "border-[#E2E8F0] hover:border-[#CBD5E1] bg-[#FAFAF7] text-[#334155]"
                          }`}
                        >
                          {slot}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* ── STEP 4: PATIENT DEMOGRAPHICS & INTAKE ──────────────── */}
              {step === 4 && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-base font-bold text-[#0F172A]">Patient Information</h3>
                    <p className="text-xs text-[#64748B]">Provide your legal identity details for clinical record creation.</p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="sm:col-span-2">
                      <label className="block text-xs font-bold text-[#0F172A] mb-1">
                        Full Legal Name *
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.fullName}
                        onChange={(e) => handleFieldChange("fullName", e.target.value)}
                        placeholder="e.g. Hamza Farooqi"
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#0F172A] mb-1">
                        Mobile Phone Number *
                      </label>
                      <input
                        type="tel"
                        required
                        value={formData.mobile}
                        onChange={(e) => handleFieldChange("mobile", e.target.value)}
                        placeholder="+91 98765 43210"
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#0F172A] mb-1">
                        Email Address *
                      </label>
                      <input
                        type="email"
                        required
                        value={formData.email}
                        onChange={(e) => handleFieldChange("email", e.target.value)}
                        placeholder="patient@example.com"
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#0F172A] mb-1">
                        Age
                      </label>
                      <input
                        type="number"
                        min={1}
                        max={120}
                        value={formData.age}
                        onChange={(e) => handleFieldChange("age", parseInt(e.target.value) || 30)}
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#0F172A] mb-1">
                        Gender
                      </label>
                      <select
                        value={formData.gender}
                        onChange={(e) => handleFieldChange("gender", e.target.value)}
                        className="w-full p-3 rounded-xl border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#1B4332]"
                      >
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other / Prefer not to say</option>
                      </select>
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] flex items-center justify-between">
                    <div>
                      <span className="text-xs font-bold text-[#0F172A] block">
                        Do you have prior laboratory reports or scans to share?
                      </span>
                      <span className="text-[11px] text-[#64748B]">
                        You can present or upload them during your consultation.
                      </span>
                    </div>
                    <input
                      type="checkbox"
                      checked={formData.hasPreviousReports}
                      onChange={(e) => handleFieldChange("hasPreviousReports", e.target.checked)}
                      className="w-4 h-4 text-[#1B4332] rounded focus:ring-0"
                    />
                  </div>
                </div>
              )}

              {/* ── STEP 5: REVIEW & CONSENT ──────────────────────────── */}
              {step === 5 && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-base font-bold text-[#0F172A]">Review &amp; Informed Consent</h3>
                    <p className="text-xs text-[#64748B]">Review your consultation summary and grant statutory privacy consent.</p>
                  </div>

                  <div className="p-5 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-3 text-xs">
                    <div className="flex justify-between border-b border-[#E2E8F0] pb-2">
                      <span className="text-[#64748B]">Patient</span>
                      <span className="font-bold text-[#0F172A]">{formData.fullName} ({formData.gender}, {formData.age} yrs)</span>
                    </div>
                    <div className="flex justify-between border-b border-[#E2E8F0] pb-2">
                      <span className="text-[#64748B]">Contact</span>
                      <span className="font-bold text-[#0F172A]">{formData.mobile} • {formData.email}</span>
                    </div>
                    <div className="flex justify-between border-b border-[#E2E8F0] pb-2">
                      <span className="text-[#64748B]">Care Mode</span>
                      <span className="font-bold text-[#1B4332]">{formData.consultationType}</span>
                    </div>
                    <div className="flex justify-between border-b border-[#E2E8F0] pb-2">
                      <span className="text-[#64748B]">Appointment Slot</span>
                      <span className="font-bold text-[#0F172A]">{formData.preferredDate} at {formData.preferredTime}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-[#64748B]">Clinical Concern</span>
                      <span className="font-bold text-[#0F172A]">{formData.healthConcern}</span>
                    </div>
                  </div>

                  {/* DPDP Act 2023 Consent Checkbox */}
                  <div className="p-4 rounded-xl bg-white border border-[#E2E8F0] space-y-2">
                    <label className="flex items-start gap-2.5 cursor-pointer">
                      <input
                        type="checkbox"
                        required
                        checked={formData.consentAccepted}
                        onChange={(e) => handleFieldChange("consentAccepted", e.target.checked)}
                        className="w-4 h-4 text-[#1B4332] mt-0.5 rounded focus:ring-0"
                      />
                      <span className="text-xs text-[#475569] leading-relaxed">
                        I consent to the processing of my health information under India&apos;s <strong>Digital Personal Data Protection (DPDP) Act 2023</strong> and the <strong>NCISM Telemedicine Guidelines</strong> for clinical triage and prescription generation.
                      </span>
                    </label>
                  </div>
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="pt-6 border-t border-[#F1F5F9] flex items-center justify-between">
                {step > 1 ? (
                  <button
                    type="button"
                    onClick={handlePrev}
                    className="px-4 py-2.5 rounded-xl border border-[#CBD5E1] bg-white text-[#334155] text-xs font-semibold hover:bg-[#F8FAFC] transition"
                  >
                    Back
                  </button>
                ) : (
                  <div />
                )}

                {step < 5 ? (
                  <button
                    type="button"
                    onClick={handleNext}
                    className="px-6 py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-semibold transition shadow-sm"
                  >
                    Continue
                  </button>
                ) : (
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="px-6 py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-bold transition shadow-sm disabled:opacity-50 flex items-center gap-2"
                  >
                    {isSubmitting ? "Generating Appointment Token..." : "Confirm & Book Appointment"}
                  </button>
                )}
              </div>
            </form>
          </div>
        )}

      </div>
    </PublicWebsiteShell>
  );
}

export default function BookAppointmentPage() {
  return (
    <Suspense fallback={<div className="min-h-[50vh] flex items-center justify-center text-xs text-[#64748B]">Loading booking gateway...</div>}>
      <BookContent />
    </Suspense>
  );
}
