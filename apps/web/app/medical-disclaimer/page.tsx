"use client";

import React from "react";
import Link from "next/link";

export default function MedicalDisclaimerPage() {
  return (
    <div className="min-h-screen bg-[#0A101D] text-slate-100 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-10">
        
        {/* Breadcrumb & Header */}
        <div className="border-b border-slate-800 pb-6 space-y-3">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Link href="/" className="hover:text-teal-400 transition">ZAYVORA Health</Link>
            <span>/</span>
            <span className="text-teal-400 font-medium">Statutory Governance</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Medical &amp; Clinical Information Disclaimer
          </h1>
          <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 font-mono">
            <span>Last Reviewed: 20 September 2026</span>
            <span>•</span>
            <span>Next Review: 20 March 2027</span>
            <span>•</span>
            <span className="text-emerald-400 font-bold">Version 5.0 (NCISM &amp; AYUSH Aligned)</span>
          </div>
        </div>

        {/* Emergency Alert Box */}
        <div className="p-6 rounded-2xl bg-rose-950/30 border border-rose-800/60 text-rose-200 space-y-2 shadow-lg">
          <h2 className="font-bold text-base flex items-center gap-2 text-rose-300">
            <span>🚨</span> Acute Medical Emergency Notice — Dial 112 Immediately
          </h2>
          <p className="text-xs sm:text-sm leading-relaxed text-rose-200/90">
            The digital services, health library, assessments, and teleconsultation features provided by ZAYVORA Health are <strong>strictly not designed or equipped for acute, life-threatening medical emergencies</strong>. If you or someone in your care is experiencing acute chest pain, sudden severe breathlessness, hemoptysis, severe uncontrolled bleeding, stroke-like symptoms (sudden unilateral numbness, facial drooping, speech difficulty), anaphylaxis, or acute trauma, immediately call national emergency services (<strong>112</strong> in India) or report to the nearest tertiary-care multi-specialty emergency department. Do not rely on digital tele-health tools during an acute medical crisis.
          </p>
        </div>

        {/* Structured Sections */}
        <div className="space-y-8 text-xs sm:text-sm text-slate-300 leading-relaxed">
          
          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">1.</span> Purpose and Scope of Health Information
            </h2>
            <p>
              All materials published across ZAYVORA Health digital properties—including clinical monographs, educational articles, constitutional assessment questionnaires, interactive diagnostic cross-talk explorers, and botanical compound indices—are published solely for general educational, health literacy, and clinical reference purposes.
            </p>
            <p>
              Content is formulated upon classical Greco-Arab Unani medical treatises (including the <em>Canon of Medicine / Al-Qanun fi al-Tibb</em> of Ibn Sina, <em>Kitab al-Kulliyat</em> of Ibn Rushd, and the <em>Unani Pharmacopoeia of India - UPI</em>) paired with modern biomedical and translational research. Information on this platform is not intended to serve as individual medical advice, diagnostic determination, or treatment instruction without a direct clinical consultation.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">2.</span> Not a Substitute for Professional Medical Advice
            </h2>
            <p>
              Information obtained through ZAYVORA Health does not establish a doctor-patient relationship prior to a formal, logged, and confirmed clinical consultation with a board-certified practitioner. Users are strongly cautioned against attempting self-diagnosis, self-medication, or modifying their current prescription medications without the direct supervision of their treating physician.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">3.</span> Clinician Responsibility &amp; Statutory Registration (NCISM Act, 2020)
            </h2>
            <p>
              All consultations conducted under the ZAYVORA Health umbrella are delivered exclusively by qualified healthcare practitioners holding recognized qualifications under the <strong>National Commission for Indian System of Medicine (NCISM) Act, 2020</strong> (which repealed and superseded the Indian Medicine Central Council Act, 1970) and registered with the National Board of Examination or State AYUSH Medical Councils.
            </p>
            <p>
              The attending clinician exercises independent, autonomous clinical judgement in assessing the patient&apos;s condition, establishing a differential diagnosis, evaluating constitutional temperament (<em>Mizaj</em>), and formulating therapeutic regimens.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">4.</span> Clinical AI Decision Support (Hakeem Sahab AI™) Transparency &amp; Boundaries
            </h2>
            <p>
              <strong>Hakeem Sahab AI™</strong> operates strictly as an assistive Clinical Decision Support System (CDSS) for licensed clinicians. It synthesizes classical pharmacopeial literature, drug-herb interaction matrices, and verified dosage parameters to provide informational suggestions.
            </p>
            <ul className="list-disc pl-5 space-y-1 text-slate-400">
              <li><strong>Zero Autonomous Prescribing:</strong> The AI system does not possess diagnostic or prescribing authority. No prescription or treatment recommendation is ever issued without explicit, manual review and a cryptographically logged digital signature by a licensed clinician under 21 CFR Part 11 standards.</li>
              <li><strong>Human Responsibility:</strong> The attending clinician remains 100% legally and ethically responsible for all diagnostic decisions, prescription authoring, and clinical outcomes.</li>
              <li><strong>Uncertainty Indicators:</strong> When clinical inputs fall outside established pharmacopeial guidelines or validated clinical guidelines, the system indicates an active caution state and demands clinical escalation.</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">5.</span> Prescription Formulation &amp; Schedule E(1) Mudabbar Dispensing Gates
            </h2>
            <p>
              Herbal prescriptions (<em>Nuskha</em>) authored within ZAYVORA Health are tailored to individual constitutional imbalances (<em>Su-e-Mizaj</em>) and multi-organ functional axes. Formulations containing potent botanical or mineral ingredients governed under Schedule E(1) of the Drugs and Cosmetics Rules, 1945 (such as <em>Suranjan</em>, <em>Azaraqi</em>, and <em>Bhilawan</em>) are subject to mandatory electronic detoxification (<em>Mudabbar</em>) verification gates and cannot be dispensed without verified Certificates of Analysis (CoA).
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">6.</span> Botanical Formulations Regulatory Status &amp; Disclaimer of Marketing Overclaims
            </h2>
            <p>
              In strict accordance with Ministry of AYUSH regulatory advisories and statutory frameworks:
            </p>
            <ul className="list-disc pl-5 space-y-1 text-slate-400">
              <li><strong>No &quot;Ministry Certification&quot; Claims:</strong> The Ministry of AYUSH does not directly grant individual drug manufacturing licenses or endorse specific commercial products. Manufacturing licenses (Form 25-D) and classical/proprietary approvals under Rule 158B of the Drugs and Cosmetics Rules, 1945 are granted by the designated State Licensing Authorities (SLA).</li>
              <li><strong>Prohibition of &quot;100% Safe&quot; or &quot;Guaranteed Cure&quot; Claims:</strong> ZAYVORA Health expressly disclaims any assertion of &quot;100% safety&quot;, &quot;zero adverse effects&quot;, or &quot;guaranteed treatment&quot;. While Greco-Arab Unani formulations have centuries of documented traditional usage, all bioactive substances have potential contraindications, dosage limits, and individual sensitivity thresholds.</li>
              <li><strong>Good Manufacturing Practices (GMP):</strong> Products are compounded in facilities certified under Schedule T (Good Manufacturing Practice for Ayurveda, Siddha and Unani Medicines) of the Drugs and Cosmetics Rules, 1945.</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">7.</span> Individual Biological Response &amp; Temperamental Variability
            </h2>
            <p>
              Therapeutic response varies substantially across individual temperamental humors (<em>Damawi</em>, <em>Balghami</em>, <em>Safrawi</em>, <em>Saudawi</em>), chronicity of illness, metabolic status, adherence to dietary guidelines (<em>Ilaj-bil-Ghiza / Parhez</em>), and concurrent allopathic pharmacotherapy. No outcome timeline can be guaranteed.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">8.</span> Teleconsultation Statutory Limitations
            </h2>
            <p>
              Teleconsultations conducted via encrypted audio/video channels are subject to inherent physical diagnostic limitations. They cannot replace in-person palpation, detailed 10-Ajnas arterial pulse (<em>Nabz</em>) diagnosis, or physical systemic examinations where clinically indicated. The attending clinician reserves the absolute right to terminate a teleconsultation and refer the patient for urgent in-person clinical evaluation or hospital admission.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">9.</span> Distinction Between Clinical Care and Research Simulations
            </h2>
            <p>
              Digital tools identified as research simulations, N-of-1 trial cohorts, or Real-World Evidence (RWE) observational analyses represent investigational and academic methodologies. Such exploratory algorithms are segregated from verified clinical care protocols and are never deployed for frontline diagnosis without dedicated institutional ethics committee (IEC) clearance.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">10.</span> Patient Data Governance &amp; DPDP Act Alignment
            </h2>
            <p>
              Patient health records and teleconsultation transcripts are governed under the <strong>Digital Personal Data Protection (DPDP) Act, 2023</strong> and the <strong>DPDP Rules, 2025</strong> (incorporating staged commencement provisions), adhering to end-to-end cryptographic hashing, patient-mediated consent, and Ayushman Bharat Digital Mission (ABDM M1-M3) interoperability guidelines.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400">11.</span> Clinical Governance Secretariat &amp; Review Contacts
            </h2>
            <p>
              For statutory, medical governance, or content verification queries, please contact:
            </p>
            <div className="bg-[#0F172A] p-5 rounded-2xl border border-slate-800 space-y-2 text-xs">
              <div className="text-white font-bold">Clinical Governance &amp; Legal Regulatory Secretariat — ZAYVORA Health</div>
              <div className="text-slate-400">Attn: Office of Clinical Affairs &amp; Regulatory Compliance</div>
              <div className="text-slate-400">Institutional Healthcare Complex, New Delhi - 110062, India</div>
              <div className="text-teal-400 font-mono">Email: clinical-governance@zayvora.com • Regulatory Desk: +91 97738 82657</div>
              <div className="text-[11px] text-slate-500 pt-2 border-t border-slate-800">
                Responsible Clinical Reviewer: <strong>Hakeem Dr. Irfan Ashraf</strong>, Founder, Chairman &amp; Chief Architect (BUMS, MD Unani, Academic Director CP-AFUM)
              </div>
            </div>
          </section>

        </div>

        {/* Footer Navigation */}
        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs">
          <Link href="/" className="text-teal-400 hover:underline flex items-center gap-1.5">
            <span>←</span> Return to Homepage
          </Link>
          <div className="flex items-center gap-3">
            <Link href="/privacy-policy" className="text-slate-400 hover:text-white transition">
              Privacy Policy
            </Link>
            <span className="text-slate-700">•</span>
            <Link href="/terms-and-conditions" className="text-slate-400 hover:text-white transition">
              Terms of Service
            </Link>
            <span className="text-slate-700">•</span>
            <Link href="/book" className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold transition">
              Book Consultation →
            </Link>
          </div>
        </div>

      </div>
    </div>
  );
}
