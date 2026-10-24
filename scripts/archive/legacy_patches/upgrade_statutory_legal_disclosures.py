#!/usr/bin/env python3
"""
Upgrades statutory legal pages and footer disclosures across index.html and docs/index.html:
- Terms of Clinical Service & Platform Use
- DPDP Act 2023 & HIPAA Data Protection & Privacy Policy
- Statutory Medical & Emergency 112 Disclaimer (Zero Cure Guarantees)
- Cancellation & Refund Policy (Payment Gateway / Razorpay & Stripe Compliant)
- Shipping & Cold-Chain Delivery Policy
- Statutory Grievance Redressal Mechanism & Officer (IT Rules 2021)
"""

import os, re, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

NEW_LEGAL_TABS_HTML = '''      // TAB: PRIVACY POLICY (DPDP ACT 2023 & HIPAA COMPLIANT)
      if (state.tab === 'privacy') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Privacy Policy</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Data Protection & Privacy Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Governed under India's Digital Personal Data Protection (DPDP) Act 2023, Information Technology Act 2000, Ayushman Bharat Digital Mission (ABDM) standards, and international health data protection frameworks (HIPAA &amp; DISHA aligned).
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">DPDP Act 2023 Compliant</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">ABDM M1-M3 Data Locker</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">AES-256-GCM Encryption</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Last Revised: September 2026</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  1. Collection of Health & Personal Data
                </h3>
                <p>
                  ZAYVORA Health OS™ collects personal identification data (Name, Date of Birth, Gender, Mobile, ABHA ID) and Sensitive Personal Data or Information (SPDI) strictly essential for clinical consultations, including 10-Ajnas Mizaj physiological vectors, vital signs, chief complaints, pulse waveforms, lab investigation reports, and pharmacotherapy history.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  2. Purpose Specification & Lawful Processing
                </h3>
                <p>
                  Health data is processed exclusively for: (a) formulating clinical Unani and integrative medical evaluations, (b) secure transmission to certified central pharmacies for prescription fulfillment, (c) pharmacovigilance adverse reaction monitoring under AYUSH regulations, and (d) patient-initiated consent sharing via ABDM health lockers. We <strong>never sell, rent, or commercialize</strong> patient biometric or medical records to third-party advertisers.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  3. Cryptographic Storage & Transmission Security
                </h3>
                <p>
                  All Protected Health Information (PHI) is encrypted at rest using enterprise <strong>AES-256-GCM</strong> cipher algorithms and transmitted via strict <strong>TLS 1.3</strong> encrypted tunnels. Prescriptions and medical sign-offs are locked with <strong>21 CFR Part 11 compliant digital signatures</strong> with Merkle-tree tamper-evident audit trails.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  4. Patient Rights Under DPDP Act 2023
                </h3>
                <p>
                  Patients hold full statutory rights to: (a) Request a copy of their comprehensive health summary (Patient 360 profile), (b) Correct inaccurate or outdated demographic and medical details, (c) Revoke consent for digital health record sharing at any time, and (d) Nominate a representative in the event of death or incapacity.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  5. Data Protection Officer (DPO) Contact
                </h3>
                <p>
                  For formal data privacy requests, consent revocation, or compliance queries, contact our Data Protection Officer at:
                </p>
                <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 text-[11px] font-mono space-y-1">
                  <div><strong>Email:</strong> <a href="mailto:privacy@zayvora.com" class="text-emerald-400">privacy@zayvora.com</a></div>
                  <div><strong>Telephone:</strong> +91 97738 82657</div>
                  <div><strong>Office:</strong> ZAYVORA Health OS Legal &amp; Compliance Cell, New Delhi, India</div>
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
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory User Agreement</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Terms of Clinical Telemedicine Service</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Legally binding terms governing teleconsultations, electronic prescriptions, herbal dispensary orders, and interactions across ZAYVORA Health OS™.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Telemedicine Guidelines 2020 Aligned</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">NCISM Act 2020 Registered Clinicians</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Jurisdiction: New Delhi</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  1. Clinical Consultation Scope &amp; Eligibility
                </h3>
                <p>
                  Consultations on this platform are conducted solely by licensed practitioners registered under the <strong>National Commission for Indian System of Medicine (NCISM) Act, 2020</strong>. Telemedicine consultations are subject to Telemedicine Practice Guidelines issued by the Ministry of AYUSH. Patients must be at least 18 years of age or accompanied by a lawful parent/guardian.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  2. Acute Emergency Exclusion
                </h3>
                <p>
                  <strong>Telemedicine is strictly not intended for life-threatening medical emergencies.</strong> If you or someone in your care is experiencing acute chest pain, sudden breathlessness, severe hemorrhage, stroke signs, or severe poisoning, immediately dial national emergency services (<strong>112</strong>) or report to the nearest emergency room.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  3. Electronic Prescriptions &amp; Digital Signatures
                </h3>
                <p>
                  Prescriptions authored through the platform are authentic legal electronic documents under the Information Technology Act, 2000. Prescriptions are locked with <strong>21 CFR Part 11 compliant cryptographic digital signatures</strong> and clinician registration credentials. Prescriptions are valid only for the indicated patient and specified duration.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  4. Patient Truthfulness &amp; Clinical History Disclosure
                </h3>
                <p>
                  Patients bear legal and ethical responsibility to disclose accurate medical histories, known drug/herb allergies, active allopathic medications, pregnancy/lactation status, and prior surgical records. ZAYVORA Health disclaims liability for adverse reactions arising from willful non-disclosure of critical clinical history.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  5. Governing Law &amp; Dispute Resolution
                </h3>
                <p>
                  These Terms are governed by and construed in accordance with the laws of India. Any legal dispute, arbitration, or proceedings shall be subject to the exclusive jurisdiction of the competent courts in <strong>New Delhi, India</strong>.
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
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Governance</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Medical &amp; Clinical Information Disclaimer</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Statutory regulatory disclosures under the Drugs &amp; Magic Remedies (Objectionable Advertisements) Act 1954, Drugs &amp; Cosmetics Act 1940, and Ministry of AYUSH directives.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Zero Guaranteed Cure Claims</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Emergency Alert: 112</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Drugs &amp; Cosmetics Rules 1945</span>
              </div>
            </div>

            <!-- Emergency Alert Notice -->
            <div class="p-5 rounded-2xl bg-rose-950/30 border border-rose-800/60 text-rose-200 space-y-2">
              <h3 class="font-bold text-sm text-rose-300 flex items-center gap-2">
                <span>🚨</span> Acute Medical Emergency Notice — Dial 112 Immediately
              </h3>
              <p class="text-xs text-rose-200/90 leading-relaxed">
                ZAYVORA Health digital services, health tools, and teleconsultations are <strong>not equipped for acute, life-threatening medical emergencies</strong>. In case of acute cardiac distress, respiratory arrest, severe trauma, or acute poisoning, immediately call national emergency (<strong>112</strong>) or report to the nearest hospital emergency department.
              </p>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  1. Prohibition of "100% Safe" or "Guaranteed Cure" Claims
                </h3>
                <p>
                  In compliance with the <strong>Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954</strong>, ZAYVORA Health explicitly disclaims any representation of &quot;guaranteed cure&quot;, &quot;permanent cure&quot;, or &quot;100% risk-free treatment&quot;. Biological responses vary according to individual constitutional humor (<em>Mizaj</em>), disease chronicity, adherence to dietary regimens (<em>Ilaj-bil-Ghiza</em>), and concurrent pharmacotherapy.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  2. Role of Hakeem Sahab AI™ (Assistive Only — Zero Autonomous Prescribing)
                </h3>
                <p>
                  <strong>Hakeem Sahab AI™</strong> functions strictly as a Clinical Decision Support System (CDSS) for qualified doctors. It provides reference citations from the Unani Pharmacopoeia of India (UPI) and botanical safety matrices. <strong>The AI possesses zero autonomous diagnostic or prescribing authority.</strong> Every prescription requires manual review, verification, and digital sealing by a licensed practitioner.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  3. Schedule E(1) Potent Botanicals &amp; Mudabbar Detoxification
                </h3>
                <p>
                  Formulations containing classical Schedule E(1) substances (such as <em>Azaraqi</em> or <em>Suranjan</em>) are subjected to mandatory laboratory detoxification gates (<em>Mudabbar</em>) and cannot be dispensed without verified Certificates of Analysis (CoA) demonstrating non-toxicity.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  4. Independent Clinician Judgment
                </h3>
                <p>
                  The attending clinician exercises complete, autonomous medical judgment. Information on this website does not constitute a doctor-patient relationship prior to an officially scheduled and logged consultation.
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
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Consumer Protection &amp; Billing</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Cancellation &amp; Refund Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Governed under the Consumer Protection (E-Commerce) Rules, 2020. Applicable to all online consultation appointments and dispensary orders processed across ZAYVORA Health.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Refund TAT: 3-5 Working Days</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Consumer Protection 2020</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Razorpay / Stripe Integrated</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  1. Clinical Consultation Cancellations &amp; Rescheduling
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-emerald-400 block text-xs">Cancellation &gt; 4 Hours Before</span>
                    <strong class="text-white text-sm">100% Full Refund</strong>
                    <p class="text-[11px] text-slate-400">Full consultation fee refunded without deductions.</p>
                  </div>
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-teal-400 block text-xs">Cancellation &lt; 4 Hours Before</span>
                    <strong class="text-white text-sm">Free Reschedule</strong>
                    <p class="text-[11px] text-slate-400">Reschedule to any available slot at no additional charge (or 80% refund).</p>
                  </div>
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-amber-400 block text-xs">Clinician Emergency / No-Show</span>
                    <strong class="text-white text-sm">100% Refund + Priority</strong>
                    <p class="text-[11px] text-slate-400">Full refund plus immediate priority booking with senior clinician.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  2. Dispensary Medicine Returns &amp; Replacements
                </h3>
                <p>
                  Under Good Distribution Practices (GDP) and drug safety standards, medicines and sealed herbal preparations once opened cannot be accepted for return due to contamination hazards. However, you are eligible for an <strong>immediate 100% refund or free expedited replacement</strong> under these circumstances:
                </p>
                <ul class="list-disc pl-5 space-y-1 text-slate-300">
                  <li>Parcel arrives visibly damaged, tampered, or with broken security seal.</li>
                  <li>Received product formulation or batch does not match the electronic prescription.</li>
                  <li>Product temperature indicator shows cold-chain deviation upon doorstep inspection.</li>
                </ul>
                <p>
                  To file a damaged parcel claim, email <a href="mailto:dispensary@zayvora.com" class="text-emerald-400">dispensary@zayvora.com</a> with unboxing photos within <strong>48 hours of delivery</strong>.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  3. Refund Mode &amp; Processing Timelines
                </h3>
                <p>
                  Approved refunds are credited back directly to the original payment source (UPI, Debit/Credit Card, Net Banking, or Wallet). Standard settlement turnaround is <strong>3 to 5 business days</strong> depending on your bank's clearing cycle.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: SHIPPING & COLD-CHAIN DELIVERY POLICY
      if (state.tab === 'shipping') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Logistics &amp; Supply</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Shipping &amp; Dispensary Delivery Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                FEFO-controlled pharmacy fulfillment, 2-8°C cold-chain surveillance, and pan-India express courier dispatch.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">24-48h Metro Dispatch</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Active Cold-Chain (2-8°C)</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Live Airway Bill (AWB) Tracking</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  1. Dispatch Timeline &amp; FEFO Verification
                </h3>
                <p>
                  Prescriptions locked by ZAYVORA clinicians undergo dual-pharmacist verification and are dispensed from our central facility under First-Expired, First-Out (FEFO) rules within <strong>24 hours</strong> of physician sign-off.
                </p>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  2. Pan-India Delivery Durations
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-teal-400 block text-xs">Delhi NCR &amp; Metros</span>
                    <strong class="text-white text-sm">24 to 48 Hours</strong>
                    <p class="text-[11px] text-slate-400">Expedited cold-chain priority transit.</p>
                  </div>
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-teal-400 block text-xs">Tier 1 &amp; Tier 2 Cities</span>
                    <strong class="text-white text-sm">2 to 4 Business Days</strong>
                    <p class="text-[11px] text-slate-400">Air courier with live SMS &amp; WhatsApp tracking.</p>
                  </div>
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-teal-400 block text-xs">Rest of India &amp; Remote</span>
                    <strong class="text-white text-sm">4 to 7 Business Days</strong>
                    <p class="text-[11px] text-slate-400">Insulated thermal-barrier protective packaging.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  3. Shipping Charges &amp; Live Tracking
                </h3>
                <p>
                  Standard dispensary orders above <strong>₹999</strong> receive 100% free delivery across India. Once dispatched, an Airway Bill (AWB) tracking number is transmitted via SMS/WhatsApp with live GPS tracking.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: STATUTORY GRIEVANCE REDRESSAL (IT RULES 2021 & CONSUMER PROTECTION)
      if (state.tab === 'grievance') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Statutory Redressal Mechanism</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Grievance Redressal Mechanism</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Appointed pursuant to Rule 3(2) of the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 and the Consumer Protection (E-Commerce) Rules, 2020.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">IT Rules 2021 Rule 3(2)</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Acknowledgement: &lt; 48 Hours</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Resolution SLA: &lt; 15 Days</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  Designated Grievance Redressal Officer
                </h3>
                <p>
                  Any user, patient, or stakeholder may submit complaints, grievances, or legal concerns directly to our designated Grievance Officer:
                </p>
                <div class="p-4 bg-slate-900 rounded-2xl border border-slate-800 space-y-2 text-xs font-mono">
                  <div><strong>Name:</strong> Advocate Tariq Masood (Legal &amp; Regulatory Head)</div>
                  <div><strong>Designation:</strong> Chief Grievance Officer, ZAYVORA Health OS™</div>
                  <div><strong>Official Email:</strong> <a href="mailto:grievance@zayvora.com" class="text-emerald-400">grievance@zayvora.com</a></div>
                  <div><strong>Direct Grievance Helpline:</strong> +91 97738 82657</div>
                  <div><strong>Registered Corporate Address:</strong> ZAYVORA Health OS Headquarters, Central Healthcare Complex, New Delhi, 110025, India</div>
                  <div><strong>Working Hours:</strong> Monday – Saturday, 10:00 AM – 6:00 PM IST</div>
                </div>
              </section>

              <section class="space-y-2">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-emerald-400 rounded-full inline-block"></span>
                  Grievance Escalation &amp; Resolution Timelines
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-emerald-400 block text-xs">Step 1: Acknowledgement</span>
                    <strong class="text-white text-sm">Within 48 Hours</strong>
                    <p class="text-[11px] text-slate-400">Formal unique ticket number issued to complainant.</p>
                  </div>
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <span class="font-bold text-teal-400 block text-xs">Step 2: Investigation &amp; Redressal</span>
                    <strong class="text-white text-sm">Within 15 Calendar Days</strong>
                    <p class="text-[11px] text-slate-400">Comprehensive written resolution and remedial action report.</p>
                  </div>
                </div>
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

    # 1. Replace the existing short privacy and terms tab handling
    pattern_tabs = r"// TAB: PRIVACY POLICY.*?// TAB: TERMS OF SERVICE.*?if \(state\.tab === 'terms'\) \{.*?\n        return;\n      \}"
    if re.search(pattern_tabs, content, re.DOTALL):
        content = re.sub(pattern_tabs, lambda m: NEW_LEGAL_TABS_HTML.strip(), content, flags=re.DOTALL)
        print(f"Replaced legal tabs in {file_path}")
    else:
        print(f"Warning: pattern_tabs not matched by regex in {file_path}, attempting fallback search...")
        # Fallback exact block replacement
        old_block_marker = "if (state.tab === 'privacy') {"
        pos_start = content.find(old_block_marker)
        if pos_start != -1:
            pos_end = content.find("if (state.tab === 'pages25')", pos_start)
            if pos_end != -1:
                content = content[:pos_start] + NEW_LEGAL_TABS_HTML + "\n\n      " + content[pos_end:]
                print(f"Replaced legal tabs via block slice in {file_path}")

    # 2. Replace the bottom copyright and legal links bar in footer
    pattern_footer_bar = r"<!-- Bottom Copyright & Legal Links -->.*?</div>\s*</div>\s*</footer>"
    new_footer_closing = NEW_FOOTER_LEGAL_BAR + "\n\n    </div>\n  </footer>"
    if re.search(pattern_footer_bar, content, re.DOTALL):
        content = re.sub(pattern_footer_bar, lambda m: new_footer_closing, content, flags=re.DOTALL)
        print(f"Replaced footer legal bar in {file_path}")
    else:
        print(f"Warning: pattern_footer_bar not matched in {file_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully saved {file_path}")

if __name__ == "__main__":
    upgrade_file(os.path.join(BASE_DIR, "index.html"))
    upgrade_file(os.path.join(BASE_DIR, "docs", "index.html"))
