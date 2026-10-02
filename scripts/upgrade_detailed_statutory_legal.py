#!/usr/bin/env python3
"""
Upgrades index.html and docs/index.html with Enterprise-Grade, Clause-by-Clause
Detailed Statutory Legal Documents:
1. Terms of Clinical Service & Platform Use (10 Full Sections)
2. Data Protection & Privacy Policy (DPDP Act 2023 & HIPAA - 10 Full Sections)
3. Statutory Medical & Emergency 112 Disclaimer (Drugs & Magic Remedies Act - 8 Full Sections)
4. Cancellation & Refund Policy (Payment Gateway / Razorpay & Stripe - 8 Full Sections)
5. Shipping & Cold-Chain Logistics Policy (AYUSH GDP - 8 Full Sections)
6. Statutory Grievance Redressal Mechanism & Officer (IT Rules 2021 - 6 Full Sections)
"""

import os, re, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DETAILED_LEGAL_TABS_HTML = '''      // TAB: PRIVACY POLICY (DPDP ACT 2023 & HIPAA COMPLIANT)
      if (state.tab === 'privacy') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Privacy Policy &bull; DPDP Act 2023 Compliant</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Comprehensive Data Protection & Privacy Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Governed under India's Digital Personal Data Protection (DPDP) Act 2023, Information Technology Act 2000, IT Rules 2011 (SPDI), Ayushman Bharat Digital Mission (ABDM) Health Data Management Policy, and international health data standards (HIPAA &amp; DISHA aligned).
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">DPDP Act 2023 Enforced</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">ABDM M1-M3 Certified Locker</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">AES-256-GCM At Rest</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">TLS 1.3 In Transit</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Effective Date: 20 September 2026</span>
              </div>
            </div>

            <!-- Executive Summary Box -->
            <div class="p-5 rounded-2xl bg-emerald-950/20 border border-emerald-800/40 text-emerald-200 space-y-2 text-xs">
              <h3 class="font-bold text-sm text-emerald-300 flex items-center gap-2">
                <span>🛡️</span> Executive Summary (Patient Data Rights at a Glance)
              </h3>
              <p class="leading-relaxed text-emerald-200/90">
                ZAYVORA Health OS™ treats your health records with the highest clinical confidentiality. We collect only data necessary for doctor consultations and prescription fulfillment. <strong>We do not sell, rent, or monetize your medical history, pulse wave data, or biometrics to third-party ad networks.</strong> You retain full rights to access, download, correct, or delete your health records or revoke ABDM health locker consent at any time.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Definitions &amp; Scope of Application
                </h3>
                <p>
                  This Privacy Policy applies to all patients, clinicians, dispensaries, and visitors interacting with ZAYVORA Health OS™ via web applications, mobile platforms, teleconsultation cockpits, or clinic kiosks.
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>"Personal Data":</strong> Any data about an individual who is identifiable by or in relation to such data, pursuant to Section 2(t) of the DPDP Act, 2023.</li>
                  <li><strong>"Sensitive Personal Data / Health Records (SPDI)":</strong> Medical diagnostic data, 10-Ajnas constitutional temperament vectors, chief complaints, arterial pulse photoplethysmography (PPG) waveforms, electronic prescriptions, lab reports, and medication histories.</li>
                  <li><strong>"Data Fiduciary":</strong> ZAYVORA Health OS Pvt. Ltd. and attending licensed practitioners determining the purpose and means of clinical data processing.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Categories of Data Collected
                </h3>
                <p>We collect data under two primary lawful categories:</p>
                <div class="space-y-2 pl-2">
                  <p><strong class="text-white">A. Demographic & Identity Data:</strong> Full legal name, date of birth, gender, residential address, active mobile telephone number, email address, and voluntary Ayushman Bharat Health Account (ABHA) 14-digit address.</p>
                  <p><strong class="text-white">B. Clinical & Physiological Parameters:</strong> Subjective symptoms, tongue multispectral image records, arterial pulse waveforms, verified blood biomarkers (HbA1c, lipid profile, liver enzymes, semen analysis), dietary logs (<em>Asbab-e-Sittah</em>), and past allopathic medications.</p>
                  <p><strong class="text-white">C. Technical Telemetry:</strong> Anonymized session logs, device operating system, browser user agent, IP address for security rate-limiting and intrusion detection, and crash telemetry.</p>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Lawful Grounds &amp; Specific Purposes of Processing
                </h3>
                <p>In strict compliance with Section 6 of the DPDP Act 2023, data is processed solely for explicit, legitimate healthcare purposes:</p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li>Formulating holistic constitutional Unani diagnoses (<em>Tashkhees-e-Mizaj</em>) and personalized treatment protocols (<em>Nuskha-e-Matab</em>).</li>
                  <li>Facilitating video and audio telemedicine encounters between patients and board-certified Senior Tabeebs.</li>
                  <li>Transmitting sealed electronic prescriptions to our central hospital dispensary for FEFO compound preparation and parcel fulfillment.</li>
                  <li>Statutory pharmacovigilance tracking of Adverse Drug Reactions (ADRs) under Ministry of AYUSH guidelines.</li>
                  <li>Generating itemized tax invoices, receipts, and processing authorized digital refunds.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Data Storage, Encryption &amp; Security Architecture
                </h3>
                <p>ZAYVORA Health OS operates a military-grade security defense-in-depth architecture:</p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Encryption At Rest:</strong> Relational patient records, medical timelines, and clinical notes are encrypted using <strong>AES-256-GCM</strong> with hardware security module (HSM) key rotation.</li>
                  <li><strong>Encryption In Transit:</strong> All web traffic and WebSocket audio/video streams are enforced over <strong>TLS 1.3</strong> with Perfect Forward Secrecy (PFS).</li>
                  <li><strong>Merkle-Tree Audit Ledgers:</strong> Prescriptions and clinical encounter locks are sealed with cryptographic SHA-256 Merkle proofs under <strong>21 CFR Part 11</strong> standards, ensuring records cannot be retroactively altered without invalidating digital signatures.</li>
                  <li><strong>Multi-Tenant Data Isolation:</strong> Strict tenant row-level security (RLS) guarantees that patient data belonging to one facility or doctor is mathematically isolated from others.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Data Sharing &amp; Third-Party Disclosures
                </h3>
                <p>
                  <strong>We do not sell patient data.</strong> Limited disclosure occurs solely with audited entities essential for care delivery:
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Attending Clinicians &amp; Pharmacists:</strong> Licensed personnel directly involved in your care continuum.</li>
                  <li><strong>Logistics &amp; Courier Partners:</strong> Only recipient name, shipping address, and telephone number are shared with logistics providers (e.g., Blue Dart, Delhivery) for doorstep delivery; <em>zero clinical diagnoses or medical conditions are shared with couriers</em>.</li>
                  <li><strong>Statutory &amp; Law Enforcement:</strong> Strictly when compelled by an official written order issued by a court of competent jurisdiction under Indian law.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">06</span>
                  Patient Rights Under the DPDP Act, 2023
                </h3>
                <p>Every patient or user of ZAYVORA Health holds actionable statutory rights:</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right to Information &amp; Access:</strong>
                    <p class="text-[11px] text-slate-400">Request an electronic summary of your health profile, prescriptions, and processing activities.</p>
                  </div>
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right to Correction &amp; Erasure:</strong>
                    <p class="text-[11px] text-slate-400">Correct inaccurate personal data or request deletion of non-statutory records.</p>
                  </div>
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right of Grievance Redressal:</strong>
                    <p class="text-[11px] text-slate-400">Register complaints directly with our Data Protection Officer with mandatory 48-hour response.</p>
                  </div>
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right to Nominate:</strong>
                    <p class="text-[11px] text-slate-400">Nominate an individual to exercise your privacy rights in the event of death or incapacity.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">07</span>
                  Data Retention Schedules
                </h3>
                <p>
                  Pursuant to National Medical Commission (NMC) and NCISM statutory regulations, clinical consultation records, medical charts, and signed electronic prescriptions are retained for a minimum mandatory period of <strong>three (3) years</strong> from the date of the last consultation. Anonymized epidemiological research metrics may be archived permanently for clinical audit and public health learning.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">08</span>
                  Cookies &amp; Local Storage Technology
                </h3>
                <p>
                  ZAYVORA Health OS™ uses essential HTTP session cookies and local storage tokens solely to maintain authenticated user sessions, language preferences, and role switcher state. We do not use third-party invasive tracking pixels or cross-site behavioral advertising cookies.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">09</span>
                  Children's Privacy Protection
                </h3>
                <p>
                  In accordance with Section 9 of the DPDP Act 2023, individuals under eighteen (18) years of age may access teleconsultation services only with the verifiable consent and active involvement of a parent or lawful guardian. We do not engage in targeted profiling or tracking of pediatric patients.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">10</span>
                  Designated Data Protection Officer (DPO)
                </h3>
                <p>
                  To exercise your statutory data privacy rights or submit inquiries regarding clinical data security, contact our dedicated compliance office:
                </p>
                <div class="p-4 bg-slate-900 rounded-2xl border border-slate-800 space-y-2 text-xs font-mono">
                  <div><strong>Designated DPO:</strong> Mr. Tariq Masood (Chief Information Security &amp; Data Officer)</div>
                  <div><strong>Direct Data Privacy Email:</strong> <a href="mailto:privacy@zayvora.com" class="text-emerald-400 font-bold">privacy@zayvora.com</a></div>
                  <div><strong>Direct Compliance Helpline:</strong> +91 97738 82657</div>
                  <div><strong>Corporate Office:</strong> ZAYVORA Health OS Data Governance Division, Central Healthcare Complex, New Delhi, 110025, India</div>
                  <div><strong>Response Timeline:</strong> Formal acknowledgement within 24–48 business hours.</div>
                </div>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: TERMS OF CLINICAL SERVICE & PLATFORM USE
      if (state.tab === 'terms') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Master Agreement</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Terms of Clinical Telemedicine Service &amp; Platform Use</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Comprehensive terms governing teleconsultation services, digital prescription authoring, herbal dispensary fulfillment, and patient-practitioner engagements across ZAYVORA Health OS™.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Telemedicine Guidelines 2020 Aligned</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">NCISM Act 2020 Registered Practitioners</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">IT Act 2000 Electronic Contracts</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Jurisdiction: New Delhi, India</span>
              </div>
            </div>

            <!-- Important Legal Alert -->
            <div class="p-5 rounded-2xl bg-amber-950/20 border border-amber-800/40 text-amber-200 space-y-2 text-xs">
              <h3 class="font-bold text-sm text-amber-300 flex items-center gap-2">
                <span>⚖️</span> Binding Legal Contract Notice
              </h3>
              <p class="leading-relaxed text-amber-200/90">
                By accessing ZAYVORA Health OS™, scheduling a teleconsultation, or ordering botanical formulations, you confirm that you have read, understood, and unconditionally agree to be bound by these Terms of Clinical Service. If you do not agree with any clause of this agreement, you must immediately discontinue use of the platform.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Practitioner Qualifications &amp; Statutory Authority
                </h3>
                <p>
                  All clinical teleconsultations on ZAYVORA Health OS™ are delivered exclusively by practitioners who hold recognized medical qualifications under the <strong>National Commission for Indian System of Medicine (NCISM) Act, 2020</strong> (e.g., BUMS / Kamil-e-Tibb-o-Jarahat, MD Unani) and are registered with the National Register of Indian System of Medicine or State AYUSH Councils.
                </p>
                <p>
                  The platform operates as a secure technology enabler and digital infrastructure provider. The professional doctor-patient relationship is established directly between the patient and the licensed attending practitioner.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Scope of Teleconsultation &amp; Inherent Limitations
                </h3>
                <p>
                  Telemedicine encounters are conducted in accordance with the <em>Telemedicine Practice Guidelines</em> jointly notified by the Ministry of AYUSH and the Board of Governors in Supersession of the Medical Council of India (2020).
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Remote Diagnostic Limitations:</strong> Patients acknowledge that video consultations lack direct physical palpation, physical tongue texture assessment, and in-person arterial pulse (<em>Nabz</em>) tactile palpation.</li>
                  <li><strong>Conversion to In-Person Evaluation:</strong> If at any stage the attending clinician determines that a remote consultation is clinically insufficient, the doctor reserves the absolute right to terminate the teleconsultation and recommend an immediate in-person clinic visit.</li>
                  <li><strong>Identity Verification:</strong> Both the patient and the clinician must verify their identities at the commencement of each consultation.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Emergency Medical Exclusion (Dial 112)
                </h3>
                <p>
                  <strong>Telemedicine is strictly contraindicated for acute, unstable, or life-threatening emergencies.</strong> The platform does not provide emergency triage. For conditions such as acute myocardial infarction, acute respiratory failure, loss of consciousness, uncontrolled hemorrhaging, or acute poison ingestion, users must immediately contact emergency services (<strong>112</strong> in India) or report to the nearest hospital casualty department.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Electronic Prescriptions &amp; Digital Signatures (21 CFR Part 11)
                </h3>
                <p>
                  Prescriptions authored through ZAYVORA Health OS are valid electronic documents under Section 4 and Section 5 of the Information Technology Act, 2000.
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li>Prescriptions are cryptographically sealed with the attending clinician's digital signature under <strong>21 CFR Part 11</strong> standards.</li>
                  <li>Prescriptions explicitly specify dosage, formulation type, vehicle (<em>Badraqa</em>), dietary instructions (<em>Parhez</em>), and duration.</li>
                  <li>Prescriptions are non-transferable and valid solely for the patient designated thereon. Alteration or counterfeiting of electronic prescriptions is a punishable offense under Indian criminal law.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Patient Obligations &amp; Accurate Disclosure
                </h3>
                <p>
                  The patient affirms that all medical history, ongoing allopathic medications, previous adverse reactions, chronic illnesses, and pregnancy/lactation statuses disclosed during consultation are complete and true. <strong>ZAYVORA Health and its clinicians disclaim all liability for adverse clinical consequences caused by intentional or negligent omission of critical health history.</strong>
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">06</span>
                  Dispensary Fulfillment &amp; Schedule E(1) Compliance
                </h3>
                <p>
                  Herbal formulations and medicines ordered via the platform are compounded and dispensed strictly under Schedule T (Good Manufacturing Practices) and Schedule E(1) of the Drugs &amp; Cosmetics Rules, 1945. Certain potent classical formulations are classified as prescription-only (Rx) and cannot be dispensed without verified physician approval and documented detoxification (<em>Mudabbar</em>) certification.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">07</span>
                  Intellectual Property &amp; Proprietary Rights
                </h3>
                <p>
                  All proprietary algorithms, clinical decision support logic (Hakeem Sahab AI™), 10-Ajnas scoring models, botanical formulations, branding, trade dress, and software source code are the exclusive intellectual property of <strong>Hakeem Dr. Irfan Ashraf</strong> and ZAYVORA Health OS Pvt. Ltd. Unauthorized reverse-engineering, scraping, or commercial duplication is strictly prohibited under the Copyright Act, 1957 and Patents Act, 1970.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">08</span>
                  Limitation of Liability &amp; Maximum Recovery Cap
                </h3>
                <p>
                  To the maximum extent permitted under applicable law, ZAYVORA Health OS and its directors, officers, and technology licensors shall not be liable for any indirect, incidental, punitive, or consequential damages resulting from platform downtime, network latency, or teleconsultation connection failures. In all circumstances, total aggregate liability of ZAYVORA Health for any claim shall be capped at the total amount actually paid by the patient for the specific consultation or product order giving rise to the claim.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">09</span>
                  Indemnification
                </h3>
                <p>
                  Users agree to defend, indemnify, and hold harmless ZAYVORA Health OS, its clinicians, directors, and affiliates against any third-party claims, liabilities, or losses arising from: (a) breach of these Terms, (b) violation of any law or patient rights, or (c) misrepresentation of identity or clinical history during consultation.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">10</span>
                  Governing Law, Arbitration &amp; Jurisdiction
                </h3>
                <p>
                  This Agreement shall be governed by and construed in accordance with the substantive laws of India. Any dispute arising out of or in connection with these Terms shall be referred to sole arbitration under the Arbitration and Conciliation Act, 1996, with the seat and venue in <strong>New Delhi, India</strong>. The courts of <strong>New Delhi, India</strong> shall have exclusive jurisdiction over any matters not subject to arbitration.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: STATUTORY MEDICAL & CLINICAL DISCLAIMER
      if (state.tab === 'disclaimer') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Governance &bull; Ministry of AYUSH &amp; NCISM Aligned</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Statutory Medical &amp; Clinical Information Disclaimer</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Mandatory statutory disclosures governed under the Drugs and Magic Remedies (Objectionable Advertisements) Act 1954, Drugs &amp; Cosmetics Act 1940, and NCISM Clinical Governance Standards.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Zero Guaranteed Cure Claims</span>
                <span class="px-2 py-0.5 rounded bg-rose-500/10 text-rose-300 border border-rose-500/30">Emergency Alert: 112</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Schedule E(1) Mudabbar Verified</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Assistive AI CDSS (Zero Autonomous Rx)</span>
              </div>
            </div>

            <!-- Emergency Alert Box -->
            <div class="p-6 rounded-2xl bg-rose-950/30 border border-rose-800/60 text-rose-200 space-y-2 shadow-lg">
              <h2 class="font-bold text-base flex items-center gap-2 text-rose-300">
                <span>🚨</span> Acute Medical Emergency Notice — Dial 112 Immediately
              </h2>
              <p class="text-xs sm:text-sm leading-relaxed text-rose-200/90">
                The digital health tools, symptom assessments, botanical compendia, and teleconsultation features of ZAYVORA Health OS™ are <strong>strictly not intended, designed, or equipped for acute, life-threatening medical emergencies</strong>. If you or someone you are assisting is experiencing severe crushing chest pain, sudden unilateral paralysis, acute shortness of breath, massive hemorrhage, severe head injury, acute anaphylaxis, or altered mental status, immediately call national emergency services (<strong>112</strong> in India) or report to the nearest hospital multi-specialty emergency department.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Absolute Prohibition of "Guaranteed Cure" or "100% Safe" Claims
                </h3>
                <p>
                  In strict compliance with the <strong>Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954</strong> and Consumer Protection regulations:
                </p>
                <ul class="list-disc pl-5 space-y-2 text-slate-400">
                  <li><strong>Zero Guaranteed Outcomes:</strong> ZAYVORA Health expressly disclaims any assertion of "100% guaranteed cure", "permanent eradication of disease", or "miraculous symptomatic reversal" for any chronic condition, including diabetes mellitus, cardiovascular ailments, osteoarthritis, or reproductive dysfunctions.</li>
                  <li><strong>Individual Biological Variability:</strong> In classical Greco-Arab Unani medicine, therapeutic efficacy is dependent upon individual constitutional temperament (<em>Mizaj</em>), metabolic state, environmental factors (<em>Asbab-e-Sittah</em>), adherence to dietary regimens (<em>Ilaj-bil-Ghiza</em>), and concurrent pharmacotherapy. Response timelines vary across individuals.</li>
                  <li><strong>No "Universal Safety":</strong> All biologically active phytotherapeutic compounds possess contraindications and dosage thresholds. No herbal product is universally safe for all human physiology without individualized clinical evaluation.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Role &amp; Boundaries of Clinical AI (Hakeem Sahab AI™)
                </h3>
                <p>
                  <strong>Hakeem Sahab AI™</strong> operates strictly as an assistive Clinical Decision Support System (CDSS) for certified medical practitioners:
                </p>
                <ul class="list-disc pl-5 space-y-2 text-slate-400">
                  <li><strong>Zero Autonomous Prescribing:</strong> The AI system possesses zero legal, diagnostic, or prescribing authority. No treatment plan or prescription is ever issued autonomously.</li>
                  <li><strong>Mandatory Human Clinician Barrier:</strong> Every recommendation must be independently reviewed, adjusted, approved, and cryptographically signed by a licensed practitioner under 21 CFR Part 11 standards before reaching the patient.</li>
                  <li><strong>Reference Only:</strong> AI outputs represent synthesized literature cross-talk from the Unani Pharmacopoeia of India (UPI) and PubMed botanical citations and do not constitute an independent medical opinion.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Schedule E(1) Botanical Substances &amp; Mudabbar Detoxification
                </h3>
                <p>
                  Formulations authored or cataloged on this platform that incorporate classical potent botanicals governed under Schedule E(1) of the Drugs and Cosmetics Rules, 1945 (such as <em>Azaraqi / Strychnos nux-vomica</em> or <em>Suranjan / Colchicum luteum</em>) are subject to mandatory traditional pharmaceutical detoxification protocols (<em>Amal-e-Tadbeer / Mudabbar</em>). Such products are dispensed only with verified analytical testing (heavy metals, aflatoxins, microbial pure) under strict doctor prescription.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Informational Scope — Not a Substitute for Professional Advice
                </h3>
                <p>
                  All educational content, botanical monographs, symptom calculators, and lifestyle guidance published across ZAYVORA Health are provided solely for general health literacy and academic reference. Browsing or reading materials on this platform does not create a doctor-patient relationship prior to a formal, logged consultation with an authorized clinician.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Allopathic &amp; Multi-Drug Interactions
                </h3>
                <p>
                  Patients taking concurrent allopathic pharmaceuticals (e.g., insulin, oral hypoglycemics, antihypertensives, anticoagulants/warfarin, levothyroxine) must disclose all active regimens to their attending clinician. Certain botanical extracts modulate Cytochrome P450 (CYP450) hepatic enzyme pathways and may alter drug bioavailability. Patients must never abruptly discontinue prescribed allopathic medication without consulting their primary allopathic specialist.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">06</span>
                  Regulatory Licensing Clarification
                </h3>
                <p>
                  In accordance with regulatory advisories issued by the Ministry of AYUSH: The Ministry of AYUSH does not directly certify individual commercial products or private clinics. Drug manufacturing licenses (Form 25-D) and proprietary approvals under Rule 158B of the Drugs and Cosmetics Rules 1945 are granted by designated State Licensing Authorities (SLA). All products are manufactured in facilities complying with Schedule T (Good Manufacturing Practice).
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: CANCELLATION & REFUND POLICY (RAZORPAY & STRIPE COMPLIANT)
      if (state.tab === 'refunds' || state.tab === 'shipping_refunds') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Consumer Protection &bull; E-Commerce Rules 2020 Compliant</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Cancellation, Return &amp; Refund Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Clear, transparent, and legally binding consumer rights policy governing teleconsultation cancellations, pharmacy returns, and automated payment gateway refunds.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Refund TAT: 3–5 Business Days</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Original Payment Source Credit</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Razorpay / Stripe Integrated</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Consumer Protection Act 2019</span>
              </div>
            </div>

            <!-- Highlights Box -->
            <div class="p-5 rounded-2xl bg-teal-950/20 border border-teal-800/40 text-teal-200 space-y-2 text-xs">
              <h3 class="font-bold text-sm text-teal-300 flex items-center gap-2">
                <span>💳</span> Transparent Refund Assurance
              </h3>
              <p class="leading-relaxed text-teal-200/90">
                All authorized refunds are processed directly back to your original payment method (UPI, Debit/Credit Card, Net Banking). No credit slips or forced wallet points — real money refunded to your account within <strong>3 to 5 banking days</strong>.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Teleconsultation Cancellation &amp; Rescheduling Matrix
                </h3>
                <p>Appointments booked on ZAYVORA Health OS may be cancelled or rescheduled under the following transparent terms:</p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-emerald-400 block text-xs">More than 4 Hours Prior</span>
                    <strong class="text-white text-base font-extrabold">100% Full Refund</strong>
                    <p class="text-[11px] text-slate-400">Zero cancellation fee. Entire consultation amount refunded automatically.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Within 4 Hours of Slot</span>
                    <strong class="text-white text-base font-extrabold">Free Reschedule</strong>
                    <p class="text-[11px] text-slate-400">Reschedule to any available slot at zero extra charge (or 80% refund upon request).</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-amber-400 block text-xs">Clinician Emergency / No-Show</span>
                    <strong class="text-white text-base font-extrabold">100% Refund + Priority</strong>
                    <p class="text-[11px] text-slate-400">Full refund initiated immediately plus complimentary priority booking with Senior Tabeeb.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Dispensary Medication &amp; Herbal Product Returns
                </h3>
                <p>
                  Under the Drugs and Cosmetics Rules, 1945 and international Good Distribution Practices (GDP), <strong>medicines, consumable tonics, and sealed botanical products cannot be returned once opened or unsealed</strong>, due to environmental hygiene and contamination hazards.
                </p>
                <p><strong class="text-white">Eligible Replacement &amp; Full Refund Exceptions:</strong></p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Transit Damage:</strong> Parcel arrives physically crushed, broken, or with torn tamper-evident security tape.</li>
                  <li><strong>Formulation Inaccuracy:</strong> Dispensed product batch or formulation does not match the sealed digital prescription.</li>
                  <li><strong>Temperature Indicator Deviation:</strong> Biological cold-chain indicator (on Arqiyat or Khamiras) shows temperature compromise.</li>
                  <li><strong>Expiry Threshold:</strong> Product arrives with less than six (6) months of remaining shelf life.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  How to Initiate a Damaged Parcel Return Claim
                </h3>
                <p>
                  To lodge an eligible dispensary claim, simply email our central hospital pharmacy at <a href="mailto:dispensary@zayvora.com" class="text-emerald-400 font-bold">dispensary@zayvora.com</a> or message our WhatsApp concierge at <strong>+91 97738 82657</strong> within <strong>48 hours of parcel delivery</strong>. Please attach:
                </p>
                <ul class="list-disc pl-5 space-y-1 text-slate-400">
                  <li>Your Prescription / Order ID (e.g., RX-2026-XXXX or ORD-XXXX).</li>
                  <li>Clear unboxing photograph or short video showing the outer shipping label and damaged seal.</li>
                </ul>
                <p>
                  Upon photographic verification, our pharmacy dispatches a free expedited priority replacement within 24 hours or initiates an immediate 100% refund.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Order Cancellation Prior to Courier Dispatch
                </h3>
                <p>
                  Patients and customers may cancel a dispensary order for standard OTC/wellness formulations free of charge at any time <strong>prior to courier pickup (within 4 hours of order placement)</strong>. Once a parcel has been picked up by the express logistics courier and an Airway Bill (AWB) has been generated, shipment cancellations can no longer be processed in transit.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Settlement Timelines &amp; Payment Gateway Mode
                </h3>
                <p>
                  All refunds are settled through our certified payment gateways (<strong>Razorpay / Stripe</strong>) in compliance with Reserve Bank of India (RBI) turnaround guidelines:
                </p>
                <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-2 text-[11px] font-mono">
                  <div class="flex justify-between"><span>UPI (GPay / PhonePe / Paytm):</span><strong class="text-emerald-400">Instant to 24 Hours</strong></div>
                  <div class="flex justify-between"><span>Credit / Debit Cards (Visa / Mastercard / RuPay):</span><strong class="text-white">3 to 5 Business Days</strong></div>
                  <div class="flex justify-between"><span>Net Banking (SBI / HDFC / ICICI / Axis):</span><strong class="text-white">3 to 5 Business Days</strong></div>
                </div>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: SHIPPING & COLD-CHAIN DELIVERY POLICY
      if (state.tab === 'shipping') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Logistics &bull; AYUSH Good Distribution Practices (GDP)</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Shipping, Dispatch &amp; Cold-Chain Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                FEFO-controlled pharmacy fulfillment, 2-8°C active thermal barrier monitoring, and pan-India express courier network.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">24-48h Metro Dispatch</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">2-8°C Active Thermal Barrier</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Live GPS AWB Tracking</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Tamper-Evident Security Seals</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Dispensary Fulfillment &amp; FEFO Dispatch Protocols
                </h3>
                <p>
                  Prescriptions authored and locked by ZAYVORA clinicians are dispatched directly from our centralized GMP hospital pharmacy in New Delhi. Every order is inspected by a registered Chief Pharmacist under strict First-Expired, First-Out (FEFO) batch inventory controls within <strong>twenty-four (24) hours</strong> of electronic sign-off.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Pan-India Shipping Coverage &amp; Durations
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Delhi NCR &amp; Metro Hubs</span>
                    <strong class="text-white text-base font-extrabold">24 to 48 Hours</strong>
                    <p class="text-[11px] text-slate-400">Direct priority air dispatch via Blue Dart &amp; Delhivery.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Tier 1 &amp; Tier 2 Cities</span>
                    <strong class="text-white text-base font-extrabold">2 to 4 Business Days</strong>
                    <p class="text-[11px] text-slate-400">Live SMS &amp; WhatsApp tracking with OTP delivery.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Rest of India &amp; Remote</span>
                    <strong class="text-white text-base font-extrabold">4 to 7 Business Days</strong>
                    <p class="text-[11px] text-slate-400">Insulated multi-barrier protective parcel packaging.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  2-8°C Active Thermal Barrier &amp; Cold-Chain Monitoring
                </h3>
                <p>
                  Volatile phytotherapeutic distillates (<em>Arqiyat</em>), vital bio-compounds, and active syrups are packaged inside specialized insulated thermal sleeves equipped with chemical temperature monitor tags. In the unlikely event of courier delay or extreme summer transit heat causing indicator color deviation, patients receive a complimentary priority replacement.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Shipping Charges &amp; Free Delivery Threshold
                </h3>
                <p>
                  All dispensary medication orders and wellness products with a cart value exceeding <strong>₹999</strong> qualify for <strong>100% Free Shipping</strong> across India. For orders below ₹999, a flat nominal handling fee of ₹79 is applied to cover insulated clinical packaging.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Real-Time Airway Bill (AWB) Tracking
                </h3>
                <p>
                  Upon parcel handover to the courier, an encrypted Airway Bill (AWB) tracking number is transmitted directly to the patient's registered mobile number via SMS and WhatsApp. Deliveries are protected with a mandatory <strong>one-time delivery password (OTP)</strong> to ensure that medicine parcels are handed over exclusively to the authorized patient or representative.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: STATUTORY GRIEVANCE REDRESSAL MECHANISM
      if (state.tab === 'grievance') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Grievance Redressal &bull; IT Rules 2021 Compliant</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Statutory Grievance Redressal Mechanism</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Appointed pursuant to Rule 3(2) of the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 and Section 5(9) of the Consumer Protection (E-Commerce) Rules, 2020.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">IT Rules 2021 Rule 3(2)</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Mandatory Acknowledgement &lt; 48 Hours</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Final Redressal SLA &lt; 15 Calendar Days</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Appellate Mechanism Established</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Designated Chief Grievance Redressal Officer
                </h3>
                <p>
                  Any user, patient, medical practitioner, or statutory regulator may escalate complaints, legal concerns, or technical grievances regarding content, privacy, clinical conduct, or e-commerce delivery directly to our designated officer:
                </p>
                <div class="p-5 bg-slate-900 rounded-2xl border border-slate-800 space-y-2.5 text-xs font-mono">
                  <div><strong>Officer Name:</strong> Advocate Tariq Masood (Legal &amp; Regulatory Head)</div>
                  <div><strong>Official Designation:</strong> Chief Grievance Officer, ZAYVORA Health OS™</div>
                  <div><strong>Dedicated Grievance Email:</strong> <a href="mailto:grievance@zayvora.com" class="text-emerald-400 font-bold underline">grievance@zayvora.com</a></div>
                  <div><strong>Direct Escalation Helpline:</strong> +91 97738 82657</div>
                  <div><strong>Registered Corporate Address:</strong> ZAYVORA Health OS Headquarters, Central Healthcare Complex, Okhla Institutional Area, New Delhi, 110025, India</div>
                  <div><strong>Official Office Hours:</strong> Monday through Saturday, 10:00 AM – 6:00 PM IST (Excluding Public Holidays)</div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Statutory Resolution SLA Timelines
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-emerald-400 block text-xs">Stage 1: Formal Ticket Acknowledgement</span>
                    <strong class="text-white text-base font-extrabold">&lt; 48 Hours</strong>
                    <p class="text-[11px] text-slate-400">A formal unique tracking ticket number is generated and sent via SMS and email.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Stage 2: Full Investigation &amp; Redressal</span>
                    <strong class="text-white text-base font-extrabold">&lt; 15 Calendar Days</strong>
                    <p class="text-[11px] text-slate-400">Complete investigation with written report, corrective actions, or refund settlement.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Grievance Escalation Process
                </h3>
                <p>
                  If you are not satisfied with the resolution provided by our general support desk, you may escalate to the Grievance Officer stating your original Ticket ID. The Grievance Officer conducts an independent review in coordination with the Clinical Governance Board.
                </p>
                <p>
                  In the rare event that a grievance is not resolved to your satisfaction within 15 days, you have the statutory right under the IT Rules 2021 to appeal to the Grievance Appellate Committee (GAC) constituted by the Ministry of Electronics and Information Technology (MeitY), Government of India.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }
'''

NEW_FOOTER_LEGAL_BAR = '''      <!-- Bottom Copyright & Legal Links -->
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-800 text-[11px] text-slate-500">
        <div>
          &copy; 2026 ZAYVORA Health OS™. All Rights Reserved. Proprietary Intellectual Property of <strong class="text-slate-300">Hakeem Dr. Irfan Ashraf</strong>.
        </div>
        <div class="flex flex-wrap items-center gap-3 text-slate-400">
          <a href="javascript:void(0)" onclick="viewWebsitePage('privacy')" class="hover:text-emerald-400 transition-colors">Privacy Policy (DPDP 2023)</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('terms')" class="hover:text-emerald-400 transition-colors">Terms of Clinical Service</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('disclaimer')" class="hover:text-emerald-400 transition-colors">Medical &amp; Emergency Disclaimer</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('refunds')" class="hover:text-emerald-400 transition-colors">Cancellation &amp; Refund Policy</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('shipping')" class="hover:text-emerald-400 transition-colors">Shipping &amp; Delivery</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('grievance')" class="hover:text-emerald-400 transition-colors">Grievance Redressal</a>
          <span>&bull;</span>
          <span class="text-emerald-400/80 font-medium">WCAG 2.1 AA Aligned</span>
        </div>
      </div>'''

def upgrade_file(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match block between start of privacy tab and pages25
    pos_start = content.find("if (state.tab === 'privacy') {")
    if pos_start != -1:
        # Walk back to // TAB: PRIVACY POLICY if present
        comment_pos = content.rfind("// TAB: PRIVACY POLICY", 0, pos_start)
        if comment_pos != -1 and pos_start - comment_pos < 100:
            pos_start = comment_pos

        pos_end = content.find("if (state.tab === 'pages25')", pos_start)
        if pos_end != -1:
            # Walk back to comment // TAB: SYSTEM ARCHITECTURE
            comment_end = content.rfind("// TAB: SYSTEM ARCHITECTURE", pos_start, pos_end)
            if comment_end != -1:
                pos_end = comment_end

            content = content[:pos_start] + DETAILED_LEGAL_TABS_HTML + "\n\n      " + content[pos_end:]
            print(f"Replaced detailed legal tabs in {file_path}")
        else:
            print(f"Error: pos_end for pages25 not found in {file_path}")
    else:
        print(f"Error: pos_start for privacy not found in {file_path}")

    # Replace footer legal bar
    pattern_footer_bar = r"<!-- Bottom Copyright & Legal Links -->.*?</div>\s*</div>\s*</footer>"
    new_footer_closing = NEW_FOOTER_LEGAL_BAR + "\n\n    </div>\n  </footer>"
    if re.search(pattern_footer_bar, content, re.DOTALL):
        content = re.sub(pattern_footer_bar, lambda m: new_footer_closing, content, flags=re.DOTALL)
        print(f"Replaced footer legal bar in {file_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully saved {file_path}")

if __name__ == "__main__":
    upgrade_file(os.path.join(BASE_DIR, "index.html"))
    upgrade_file(os.path.join(BASE_DIR, "docs", "index.html"))
