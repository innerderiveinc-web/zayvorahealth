"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { HEALTH_LIBRARY_ARTICLES } from "@/lib/data/healthLibrary";

export default function HealthLibraryArticlePage() {
  const params = useParams();
  const slug = params?.slug as string;

  const article = HEALTH_LIBRARY_ARTICLES.find((a) => a.slug === slug);
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(null);

  if (!article) {
    return (
      <PublicWebsiteShell>
        <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
          <HealthcareIcon name="alert-triangle" className="w-12 h-12 text-slate-400 mx-auto" />
          <h1 className="text-2xl font-bold text-[#0F172A]">Article Not Found</h1>
          <p className="text-slate-500 text-xs">The requested health library article could not be located in our certified repository.</p>
          <div className="pt-2">
            <Link
              href="/health-library"
              className="px-6 py-2.5 rounded-xl bg-[#1B4332] text-white font-medium text-xs hover:bg-[#2D6A4F] transition"
            >
              Back to Health Library
            </Link>
          </div>
        </div>
      </PublicWebsiteShell>
    );
  }

  return (
    <PublicWebsiteShell>
      {/* Article Header & Breadcrumbs */}
      <div className="bg-white border-b border-slate-200/80 py-12">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <nav className="flex items-center gap-2 text-xs text-slate-400">
            <Link href="/" className="hover:text-slate-700">Home</Link>
            <span>/</span>
            <Link href="/health-library" className="hover:text-slate-700">Health Library</Link>
            <span>/</span>
            <span className="text-[#1B4332] font-semibold">{article.category}</span>
          </nav>

          <div className="flex flex-wrap items-center gap-3">
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-[#1B4332] border border-emerald-200">
              {article.category}
            </span>
            <span className="text-xs text-slate-500 flex items-center gap-1 font-medium">
              <HealthcareIcon name="clock" className="w-3.5 h-3.5 text-slate-400" />
              <span>{article.readingTimeMinutes} min read</span>
            </span>
            <span className="text-xs text-slate-400 font-mono">Monograph v{article.version}</span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold text-[#0F172A] leading-tight">
            {article.title}
          </h1>

          <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-4xl">
            {article.summary}
          </p>

          {/* Clinical Governance & Review Credentials Panel */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-5 rounded-2xl bg-slate-50 border border-slate-200/80">
            {/* Author */}
            <div className="flex items-center gap-3.5">
              <div className="w-10 h-10 rounded-xl bg-slate-200/80 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0">
                AU
              </div>
              <div>
                <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Author</p>
                <p className="text-xs sm:text-sm font-bold text-slate-900">{article.author.name}</p>
                <p className="text-[11px] text-slate-500">{article.author.qualification} • {article.author.role}</p>
              </div>
            </div>

            {/* Clinical Reviewer */}
            <div className="flex items-center gap-3.5 border-t md:border-t-0 md:border-l border-slate-200/80 pt-3 md:pt-0 md:pl-5">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-200 text-[#1B4332] flex items-center justify-center text-xs font-bold shrink-0">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-emerald-700" />
              </div>
              <div>
                <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Senior Clinical Reviewer</p>
                <p className="text-xs sm:text-sm font-bold text-slate-900">{article.clinicalReviewer.name}</p>
                <p className="text-[11px] text-slate-500">
                  NCISM Reg: <span className="text-emerald-800 font-mono font-medium">{article.clinicalReviewer.ncismRegNumber}</span> • Certified: {article.clinicalReviewer.reviewDate}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Body */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          
          {/* Article Main Column */}
          <div className="lg:col-span-2 space-y-10">
            
            {/* Red-Flag Emergency Box */}
            {article.redFlagEmergencySigns.length > 0 && (
              <div className="p-6 rounded-3xl bg-red-50 border border-red-200 space-y-3">
                <div className="flex items-center gap-2">
                  <HealthcareIcon name="alert-triangle" className="w-5 h-5 text-red-600 shrink-0" />
                  <h2 className="text-sm font-bold text-red-950">When to Seek Immediate Emergency Medical Attention</h2>
                </div>
                <p className="text-xs text-red-800 leading-relaxed">
                  Do not rely on home measures or scheduled outpatient consultations if you experience any of the following acute symptoms:
                </p>
                <ul className="space-y-2 pt-1">
                  {article.redFlagEmergencySigns.map((sign, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-red-900 font-medium">
                      <span className="text-red-600 font-bold mt-0.5">•</span>
                      <span>{sign}</span>
                    </li>
                  ))}
                </ul>
                <div className="mt-3 pt-3 border-t border-red-200/80 flex items-center justify-between">
                  <span className="text-[11px] text-red-800">National Emergency Ambulance Service</span>
                  <span className="text-xs font-bold text-white bg-red-700 px-3 py-1 rounded-lg">Dial 112</span>
                </div>
              </div>
            )}

            {/* Content Sections */}
            {article.contentSections.map((sec, idx) => (
              <section key={idx} className="space-y-4 bg-white p-7 rounded-3xl border border-slate-200/90 shadow-sm">
                <h2 className="text-xl font-bold text-[#0F172A] border-b border-slate-100 pb-3">
                  {sec.heading}
                </h2>
                <div className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
                  {sec.body}
                </div>

                {/* Classical Unani Humoral Perspective Callout */}
                {sec.unaniPerspective && (
                  <div className="p-5 rounded-2xl bg-emerald-50/70 border border-emerald-200/80 mt-4 space-y-2">
                    <div className="flex items-center gap-2">
                      <HealthcareIcon name="leaf" className="w-4 h-4 text-emerald-800" />
                      <h4 className="text-xs font-bold text-emerald-950 uppercase tracking-wider">
                        Classical Unani Tibb Perspective (Humoral Etiology)
                      </h4>
                    </div>
                    <p className="text-xs text-emerald-900 leading-relaxed italic">
                      "{sec.unaniPerspective}"
                    </p>
                  </div>
                )}
              </section>
            ))}

            {/* Codified Evidence Sources */}
            <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-4">
              <div className="flex items-center gap-2">
                <HealthcareIcon name="book" className="w-5 h-5 text-slate-500" />
                <h3 className="text-sm font-bold text-[#0F172A] uppercase tracking-wider">
                  Authoritative Clinical References & Sources
                </h3>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">
                This monograph is codified against classical Unani pharmacopoeial treatises and verified modern peer-reviewed randomized controlled trials:
              </p>
              <ul className="space-y-2.5">
                {article.sources.map((source, sIdx) => (
                  <li key={sIdx} className="flex items-start gap-2.5 text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                    <span className="text-[#1B4332] font-bold">[{sIdx + 1}]</span>
                    <span>{source}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Frequently Asked Questions */}
            {article.faqs.length > 0 && (
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-[#0F172A]">Frequently Asked Questions</h3>
                <div className="space-y-3">
                  {article.faqs.map((faq, fIdx) => (
                    <div
                      key={fIdx}
                      className="rounded-2xl bg-white border border-slate-200/90 shadow-sm overflow-hidden"
                    >
                      <button
                        onClick={() => setOpenFaqIndex(openFaqIndex === fIdx ? null : fIdx)}
                        className="w-full text-left p-5 flex items-center justify-between text-xs sm:text-sm font-bold text-[#0F172A] hover:bg-slate-50 transition"
                      >
                        <span>{faq.question}</span>
                        <HealthcareIcon
                          name={openFaqIndex === fIdx ? "chevron-left" : "chevron-down"}
                          className="w-4 h-4 text-slate-400"
                        />
                      </button>
                      {openFaqIndex === fIdx && (
                        <div className="p-5 pt-0 text-xs text-slate-600 leading-relaxed border-t border-slate-100 bg-slate-50/50">
                          {faq.answer}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar CTA & Metadata */}
          <div className="space-y-6">
            {/* Direct Consultation Card */}
            <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-[#1B4332]">
                <HealthcareIcon name="heart-pulse" className="w-6 h-6 text-emerald-700" />
              </div>
              <h3 className="text-lg font-bold text-[#0F172A]">Individualized Clinical Evaluation</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Connect with our senior faculty for pulse diagnostics (10-Ajnas Nabz), organ-axis mapping, and customized Nuskha care.
              </p>
              <div className="pt-2">
                <Link
                  href="/contact"
                  className="w-full block text-center py-3 px-4 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-bold text-xs shadow-sm transition"
                >
                  Schedule Consultation
                </Link>
              </div>
            </div>

            {/* Article Quality Metadata Box */}
            <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
              <h4 className="text-xs font-bold text-[#0F172A] uppercase tracking-wider">Editorial Audit Log</h4>
              <div className="text-xs space-y-2 text-slate-500">
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span>Standard:</span>
                  <span className="text-slate-800 font-medium">NHS Digital / NCISM</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span>Last Review:</span>
                  <span className="text-slate-800 font-medium">{article.clinicalReviewer.reviewDate}</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span>Next Audit:</span>
                  <span className="text-slate-800 font-medium">{article.clinicalReviewer.nextReviewDate}</span>
                </div>
                <div className="flex justify-between">
                  <span>Version:</span>
                  <span className="text-slate-800 font-mono font-medium">{article.version}</span>
                </div>
              </div>
            </div>

            {/* Statutory Disclaimer */}
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 text-[11px] text-slate-500 leading-relaxed">
              <strong className="text-slate-700">Statutory Clinical Notice:</strong> This monograph is compiled for informational and clinical literacy purposes under NCISM clinical governance protocols. It does not replace an in-person clinical diagnosis by a registered medical practitioner.
            </div>
          </div>

        </div>
      </div>
    </PublicWebsiteShell>
  );
}
