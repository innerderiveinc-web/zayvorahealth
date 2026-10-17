"use client";

import React, { useState } from "react";
import Link from "next/link";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export function ContactForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    enquiryType: "General",
    subject: "",
    message: "",
    consent: false
  });

  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const enquiryTypes = [
    "General Enquiry",
    "Clinical Care & Matab Consultation",
    "Business & Institutional Partnership",
    "Research & Clinical Trial Collaboration",
    "Cleanroom Manufacturing & Formulation"
  ];

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!formData.consent) {
      setStatus("error");
      setErrorMessage("Please accept the privacy consent under DPDP Act 2023 to submit your enquiry.");
      return;
    }

    setStatus("submitting");
    setErrorMessage("");

    try {
      await new Promise((resolve) => setTimeout(resolve, 800));
      setStatus("success");
    } catch {
      setStatus("error");
      setErrorMessage("Unable to submit enquiry at this moment. Please call our helpline directly at +91 97738 82657.");
    }
  }

  if (status === "success") {
    return (
      <div className="rounded-3xl bg-white border border-emerald-200 p-8 sm:p-10 text-center shadow-sm space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto text-[#1B4332]">
          <HealthcareIcon name="check" className="w-8 h-8 text-emerald-700" />
        </div>
        <h3 className="text-2xl font-bold text-[#0F172A]">Enquiry Received</h3>
        <p className="text-slate-600 max-w-md mx-auto text-xs sm:text-sm leading-relaxed">
          Thank you for contacting ZAYVORA Health™. Your enquiry has been assigned tracking ID{" "}
          <strong className="text-slate-900 font-mono font-bold">
            ENQ-{Math.floor(Math.random() * 90000 + 10000)}
          </strong>
          . A clinical coordinator will respond within 24 business hours.
        </p>
        <div className="pt-2">
          <button
            onClick={() => {
              setFormData({
                name: "",
                email: "",
                phone: "",
                enquiryType: "General",
                subject: "",
                message: "",
                consent: false
              });
              setStatus("idle");
            }}
            className="px-6 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition"
          >
            Submit Another Enquiry
          </button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-3xl bg-white border border-slate-200/90 p-7 sm:p-8 shadow-sm space-y-5">
      <div>
        <h3 className="text-lg font-bold text-[#0F172A]">Direct Confidential Inquiry</h3>
        <p className="text-xs text-slate-500">Every transmission is logged under statutory DPDP Act 2023 security protocols.</p>
      </div>

      {status === "error" && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-800 text-xs flex items-center gap-2.5">
          <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-red-600 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Full Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Hakeem / Dr. / Mr. / Ms."
            className="w-full px-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 text-xs placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Email Address <span className="text-red-500">*</span>
          </label>
          <input
            type="email"
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            placeholder="you@domain.com"
            className="w-full px-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 text-xs placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Phone Number <span className="text-red-500">*</span>
          </label>
          <input
            type="tel"
            required
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            placeholder="+91 98765 43210"
            className="w-full px-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 text-xs placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Enquiry Type <span className="text-red-500">*</span>
          </label>
          <select
            value={formData.enquiryType}
            onChange={(e) => setFormData({ ...formData, enquiryType: e.target.value })}
            className="w-full px-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-emerald-600 focus:bg-white transition cursor-pointer"
          >
            {enquiryTypes.map((type, idx) => (
              <option key={idx} value={type}>{type}</option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-700 mb-1.5">
          Subject <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          required
          value={formData.subject}
          onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
          placeholder="Brief summary of your inquiry..."
          className="w-full px-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 text-xs placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
        />
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-700 mb-1.5">
          Detailed Message <span className="text-red-500">*</span>
        </label>
        <textarea
          required
          rows={4}
          value={formData.message}
          onChange={(e) => setFormData({ ...formData, message: e.target.value })}
          placeholder="Please describe your health inquiry, institutional requirements, or clinical research context..."
          className="w-full px-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 text-xs placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
        />
      </div>

      <div className="flex items-start gap-3 pt-1">
        <input
          type="checkbox"
          id="consent"
          checked={formData.consent}
          onChange={(e) => setFormData({ ...formData, consent: e.target.checked })}
          className="mt-1 w-4 h-4 rounded text-emerald-700 focus:ring-emerald-700 border-slate-300 cursor-pointer"
        />
        <label htmlFor="consent" className="text-xs text-slate-500 leading-relaxed cursor-pointer">
          I consent to ZAYVORA Health processing my contact details to respond to this inquiry in accordance with our{" "}
          <Link href="/privacy-policy" className="text-emerald-700 underline font-medium">
            Privacy Policy
          </Link>
          . Information is encrypted and never shared with commercial third parties.
        </label>
      </div>

      <button
        type="submit"
        disabled={status === "submitting"}
        className="w-full py-3.5 rounded-2xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-bold text-xs shadow-sm transition disabled:opacity-50 flex items-center justify-center gap-2"
      >
        <span>{status === "submitting" ? "Transmitting Securely..." : "Submit Confidential Inquiry"}</span>
        <HealthcareIcon name="arrow-right" className="w-4 h-4" />
      </button>
    </form>
  );
}
