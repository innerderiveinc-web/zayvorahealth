    function viewWebsitePage(pageKey) {
      state.role = 'website';
      state.tab = pageKey;
      renderNavigation();
      renderWorkspace();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function renderWebsiteApp(container) {
      const clinicalStages = [
        { num: "01", name: "KNOW", title: "Codified Knowledge & Evidence Retrieval", latin: "ZKB Pharmacopoeia Integration", desc: "Multi-hop traversal of UPI and NFUM classical monographs, Badal (substitutes), Musleh (correctives), and pharmacological affinities.", action: "Queried 1,280+ canonical botanical monographs with verified HPLC fingerprints." },
        { num: "02", name: "ASSESS", title: "10-Ajnas Longitudinal Mizaj Evaluation", latin: "Al-Ajnas al-Ashrah", desc: "Rigorous objective quantification across the 10 classical pulse criteria (Miqdar, Kayfiyat, Zamanah, Qawam, etc.) and tongue chromametry.", action: "Evaluates hot/cold, moist/dry deviations against patient baseline." },
        { num: "03", name: "DIFFERENTIATE", title: "Biomedical & Humoral Dual Assessment", latin: "Tashkheesh-e-Murakkab", desc: "Harmonizes classical Su-e-Mizaj humoral dyscrasias with modern ICD-10 diagnostic classifications, metabolic panels, and immunological markers.", action: "Cross-references biochemical lab results with humoral disharmonies." },
        { num: "04", name: "VERIFY", title: "Spectral Lab & Acoustic Scribe Validation", latin: "Lisan & Nabz Hardware Verification", desc: "Multispectral tongue imaging at 415-850nm paired with 100 Hz arterial PPG waveform analysis to establish objective physical signs.", action: "Hardware-confirmed coating thickness, moisture, and arterial elasticity." },
        { num: "05", name: "PERSONALIZE", title: "ZAPE Vitality & Posology Adaptation", latin: "ZAYVORA Adaptive Posology Engine", desc: "Calculates individual drug absorption, hepatic clearance, age, seasonal temperament (Fasl), and circadian timing (Anupan vehicle selection).", action: "Generates patient-specific dosing vectors with required correctives (Musleh)." },
        { num: "06", name: "PLAN", title: "Tri-Modal Regimen Synthesis", latin: "Ilaj bil-Ghiza, Tadbeer, Dawa", desc: "Simultaneous formulation of dietary directives, non-pharmacological regimenal therapies (Hijama, Natool, Zimad), and tailored botanical compounds.", action: "Synthesizes multi-week Afaal treatment roadmap with dietary prohibitions." },
        { num: "07", name: "TREAT", title: "21 CFR Part 11 Clinician Digital Signature", latin: "Statutory Clinician Discretion Barrier", desc: "Mandatory non-delegable clinical review. Prescriptions remain cryptographically locked until a credentialed Senior Tabeeb signs with cryptographic token.", action: "Zero automated autonomous prescribing; safe_to_lock=False strictly enforced." },
        { num: "08", name: "MONITOR", title: "IoT Wearable Telemetry & Relapse Forecasting", latin: "Asbab-e-Sittah Sensor Stream", desc: "Continuous BLE telemetry tracking sleep architecture, heart rate variability, skin temperature, and activity to anticipate humoral relapse.", action: "Real-time relapse prediction score updated every 15 minutes." },
        { num: "09", name: "MEASURE", title: "Longitudinal PROMs & Clinical Trajectory", latin: "Patient-Reported Outcomes (VAS / WOMAC)", desc: "Systematic tracking of functional mobility, pain attenuation curves, inflammatory marker reduction, and Meezan-e-Sehat 0-100 scores over time.", action: "Validates symptomatic and systemic recovery across weekly milestones." },
        { num: "10", name: "LEARN", title: "Real-World Evidence (RWE) Aggregation", latin: "De-Identified Observational Registry", desc: "Secure aggregation of clinical response vectors into HIPAA/ABDM-compliant research cohorts for botanical efficacy benchmarking.", action: "1,240+ multi-center clinical subjects actively contributing RWE insights." },
        { num: "11", name: "VALIDATE", title: "Academic Multi-Center Concordance", latin: "DSMB & University Consortium Review", desc: "Formal concordance analysis between traditional Unani diagnostics and blinded clinical specialist evaluations across 3 university hospitals.", action: "Maintains 94.2% diagnostic concordance across enrolled clinical trials." },
        { num: "12", name: "IMPROVE", title: "Governance Board Quorum & Protocol Evolution", latin: "3/3 Senior Specialist Quorum", desc: "Continuous clinical protocol updates requiring unanimous signed approval from Chief Clinician, Pharmacognosist, and Medical Director.", action: "Auditable governance log with immutable cryptographic Merkle tree hashes." }
      ];

      const publicPages = [
        { key: "home", path: "/website", title: "Public Home", desc: "Hero, 6 Care Areas, 10 Formulations, Philosophy, 12-Step Care Loop" },
        { key: "about", path: "/website/about", title: "About ZAYVORA", desc: "Foundational vision, leadership, and integrative mission" },
        { key: "services", path: "/website/services", title: "Clinical Services", desc: "Tele-consult, OPD, Regimenal Ilaj bil-Tadbeer, and In-Clinic Matab" },
        { key: "products", path: "/website/products", title: "Botanical Products", desc: "10-formulation portfolio e-commerce catalog with cart & checkout" },
        { key: "research", path: "/website/research", title: "Research & Evidence", desc: "Observational RWE registries, academic concordance, clinical trials" },
        { key: "philosophy", path: "/website/philosophy", title: "Clinical Philosophy", desc: "Mizaj, Afaal Cascade, Organ-Axis, and Scientific Modernity" },
        { key: "care_journey", path: "/website/care-journey", title: "12-Step Care Continuum", desc: "From KNOW & ASSESS through 21 CFR Lock and Follow-up" },
        { key: "clinics", path: "/website/clinics", title: "Hospital & Clinic Network", desc: "Multi-facility locations in Delhi, Hyderabad, Bengaluru, Srinagar" },
        { key: "doctors", path: "/website/doctors", title: "Clinicians & Faculty", desc: "Board-certified Senior Tabeebs and integrative MDs" },
        { key: "knowledge", path: "/website/knowledge-centre", title: "Knowledge Centre", desc: "Articles on Mizaj, Asbab-e-Sittah, and Botanical Monographs" },
        { key: "faqs", path: "/website/faqs", title: "Patient FAQs", desc: "Answers on Unani medicine, consulting, dosage safety, and ABHA linkage" },
        { key: "contact", path: "/website/contact", title: "Contact & Concierge", desc: "Patient helpline +91 97738 82657, facility directory, and clinic inquiries" },
        { key: "privacy", path: "/website/privacy", title: "Privacy Policy", desc: "HIPAA, DISHA, DPDP compliant data protection and ABHA consent" },
        { key: "terms", path: "/website/terms", title: "Terms of Service", desc: "Clinical telemedicine terms, clinician discretion, and governance" },
        { key: "shipping-refunds", path: "/website/shipping-refunds", title: "Shipping & Refunds", desc: "Dispensary courier, FEFO handling, and refund procedures" }
      ];

      // TAB: ABOUT
      if (state.tab === 'about') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">About ZAYVORA Health OS™</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Ancient Wisdom. Modern Science. Intelligent Care.</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                ZAYVORA Health OS™ was founded on the conviction that a millennium of codified Greco-Arab (Unani) clinical wisdom must be unified with modern biomedical diagnostic precision, high-resolution multi-omics, and clinician-governed artificial intelligence.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-3xl">🏛️</div>
                <h3 class="text-base font-bold text-white">Central Hospital Complex</h3>
                <p class="text-xs text-[var(--muted)] leading-relaxed">
                  ZAYVORA Healthcare System - Central Hospital, New Delhi Institutional Area. 120-bed integrative clinical facility with dedicated OPD, IPD, and Regimenal Therapy Suites (Hijama, Natool, Fasd).
                </p>
              </div>
              <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-3xl">🌿</div>
                <h3 class="text-base font-bold text-white">AYUSH GMP Manufacturing</h3>
                <p class="text-xs text-[var(--muted)] leading-relaxed">
                  Certified botanical extraction unit adhering to Schedule T and Schedule E(1) Mudabbar detoxification standards. HPLC active fingerprinted with 0% heavy metal tolerance.
                </p>
              </div>
              <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-3xl">🔒</div>
                <h3 class="text-base font-bold text-white">21 CFR Part 11 Governance</h3>
                <p class="text-xs text-[var(--muted)] leading-relaxed">
                  Non-delegable clinician discretion barrier. AI never issues autonomous treatment orders; all prescriptions require cryptographic biometric or PIN signature by a licensed Tabeeb.
                </p>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-6">
              <h2 class="text-xl font-bold text-white">Institutional Medical Governance Board</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                  <div class="font-bold text-white text-sm">Hakim Dr. Tariq Mansoor</div>
                  <span class="text-xs text-emerald-400 font-semibold block">BUMS, MD (Unani), PhD</span>
                  <p class="text-[11px] text-[var(--muted)]">Chief Clinician & Senior Tabeeb • 28 years integrative medicine leadership.</p>
                </div>
                <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                  <div class="font-bold text-white text-sm">Dr. Aisha Siddiqui</div>
                  <span class="text-xs text-emerald-400 font-semibold block">BUMS, MD (Tahaffuzi wa Samaji Tibb)</span>
                  <p class="text-[11px] text-[var(--muted)]">Director of Preventive Medicine & Asbab-e-Sittah Lifestyle Epidemiology.</p>
                </div>
                <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                  <div class="font-bold text-white text-sm">Dr. Arshad Qureshi</div>
                  <span class="text-xs text-emerald-400 font-semibold block">M.Pharm (Pharmacognosy), PhD</span>
                  <p class="text-[11px] text-[var(--muted)]">Head of Botanical QA/QC & Schedule E(1) Mudabbar Standardization.</p>
                </div>
              </div>
            </div>

            <div class="p-6 rounded-2xl bg-emerald-950/30 border border-emerald-500/40 flex flex-col sm:flex-row justify-between items-center gap-4">
              <div>
                <h3 class="font-bold text-white text-base">Have inquiries or require clinical concierge?</h3>
                <p class="text-xs text-emerald-200/80 mt-1">Our helpline is available 24/7 at +91 97738 82657.</p>
              </div>
              <button onclick="viewWebsitePage('contact')" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                Contact Concierge →
              </button>
            </div>
          </div>
        `;
        return;
      }

      // TAB: SERVICES
      if (state.tab === 'services') {
        const servicesList = [
          { icon: "🩺", name: "Clinical Care & OPD/IPD", desc: "Outpatient and in-patient consultations integrating 10-Ajnas pulse evaluation, Su-e-Mizaj humoral differentiation, and individualized Afaal care roadmaps.", badge: "Central Hospital & Matabs" },
          { icon: "🤖", name: "AI Healthcare & Decision Support", desc: "Hakeem Sahab AI clinical copilot traversing 1,280+ UPI monographs with mandatory 21 CFR Part 11 clinician signature lock.", badge: "Clinician-Governed" },
          { icon: "📱", name: "Digital Health & Telemedicine", desc: "Encrypted WebRTC high-definition tele-consultations, Ayushman Bharat Digital Mission (ABDM M1/M2/M3) integration, and secure electronic health records.", badge: "ABDM Aligned" },
          { icon: "🔬", name: "Clinical Research & RWE", desc: "Observational registries tracking real-world botanical efficacy, multi-center concordance trials, and validated PROMs (WOMAC, VAS).", badge: "94.2% Concordance" },
          { icon: "💊", name: "Clinical Pharmacy & FEFO", desc: "Automated First-Expiry First-Out inventory, IoT cold-chain temperature surveillance, and patient-tailored anupan vehicle guidance.", badge: "Temperature Monitored" },
          { icon: "🏭", name: "Manufacturing & QA/QC", desc: "AYUSH-GMP certified botanical production, Schedule E(1) Mudabbar detoxification, and batch manufacturing records (BMR).", badge: "AYUSH GMP" },
          { icon: "🔊", name: "Healthcare Communication", desc: "Vernacular audio posology in Urdu and Hindi, automated SMS/WhatsApp dosage notifications via QSURA.", badge: "Multilingual" }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">ZAYVORA Clinical Services</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Comprehensive Integrative Healthcare Services</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                From specialized OPD and regimenal therapy to clinician-governed AI decision support and GMP manufacturing, ZAYVORA delivers full-spectrum integrative healthcare.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              ${servicesList.map(s => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3 flex flex-col justify-between hover:border-emerald-500/50 transition">
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-3xl">${s.icon}</span>
                      <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">${s.badge}</span>
                    </div>
                    <h3 class="text-base font-bold text-white">${s.name}</h3>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${s.desc}</p>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
                    <button onclick="switchRole('clinic')" class="text-xs text-emerald-400 hover:text-white font-semibold">Book Consultation →</button>
                    <button onclick="viewWebsitePage('contact')" class="text-xs text-slate-400 hover:text-white">Inquire Details</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: PRODUCTS
      if (state.tab === 'products') {
        container.innerHTML = `
          <div class="max-w-6xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                  <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Botanical Therapeutics</span>
                  <h1 class="text-3xl font-extrabold text-white mt-1">ZAYVORA Herbals Portfolio</h1>
                  <p class="text-xs text-[var(--muted)] mt-1">AYUSH-GMP certified, HPLC active fingerprinted, Schedule E(1) Mudabbar detoxified.</p>
                </div>
                <button onclick="switchRole('herbals')" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                  🛒 Open Dispensary Cart (${herbalsCart.length} items)
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              ${herbalsProducts.map(p => `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col justify-between space-y-4 hover:border-emerald-500/50 transition">
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">${p.category}</span>
                      <span class="text-base font-bold text-white">₹${p.price}</span>
                    </div>
                    <h3 class="text-sm font-bold text-white">${p.name}</h3>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${p.desc}</p>
                    <div class="text-[11px] text-slate-300 bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)] space-y-1">
                      <div><strong class="text-emerald-400">Dose:</strong> ${p.dosage}</div>
                      <div><strong class="text-slate-400">Indications:</strong> ${p.indications}</div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
                    <span class="text-[10px] text-emerald-400 font-semibold">✓ HPLC Fingerprinted</span>
                    <button onclick="addToHerbalsCart('${p.id}')" class="px-4 py-1.5 bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold rounded-lg transition shadow">
                      + Add to Cart
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: RESEARCH & EVIDENCE
      if (state.tab === 'research') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Clinical Evidence & RWE</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Evidence-Based Integrative Medicine</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                ZAYVORA operates observational registries, multi-center academic concordance trials, and classical Unani knowledge graph traversal to substantiate botanical therapeutics.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <span class="text-xs text-[var(--muted)]">Enrolled Study Subjects</span>
                <div class="text-3xl font-bold text-white">1,240+</div>
                <p class="text-xs text-emerald-400">Across 3 hospital research centers</p>
              </div>
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <span class="text-xs text-[var(--muted)]">Diagnostic Concordance</span>
                <div class="text-3xl font-bold text-emerald-400">94.2%</div>
                <p class="text-xs text-slate-300">Unani 10-Ajnas vs blinded specialist panel</p>
              </div>
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <span class="text-xs text-[var(--muted)]">Codified Botanical Monographs</span>
                <div class="text-3xl font-bold text-white">1,280+</div>
                <p class="text-xs text-slate-300">UPI & NFUM standardized data nodes</p>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
              <h3 class="font-bold text-white text-base">Active Multi-Center Clinical Registries</h3>
              <div class="divide-y divide-[var(--border)] text-xs">
                <div class="py-3.5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div>
                    <h4 class="font-bold text-white text-sm">Trial ZAY-OA-2026: Waja-ul-Mafasil Barid Balghami</h4>
                    <p class="text-[var(--muted)]">Majun Suranjan + Raughan-e-Balsan vs Standard NSAID control in knee osteoarthritis.</p>
                  </div>
                  <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-semibold text-[10px]">Phase III Active</span>
                </div>
                <div class="py-3.5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div>
                    <h4 class="font-bold text-white text-sm">Trial ZAY-MET-2026: Su-e-Mizaj Har Safrawi Metabolic Syndrome</h4>
                    <p class="text-[var(--muted)]">MetaboCore Elite posology titration in insulin-resistant patients.</p>
                  </div>
                  <span class="px-2.5 py-1 rounded-full bg-blue-500/20 text-blue-300 font-semibold text-[10px]">Cohort Enrolling</span>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // TAB: CLINICAL PHILOSOPHY
      if (state.tab === 'philosophy') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-teal-400 uppercase tracking-wider">Clinical Philosophy</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">The Greco-Arab Medical Paradigm & Modern Omics</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Classical Unani medicine posited by Hippocrates, Galen, and Ibn Sina (Avicenna) posits that human physiology is governed by four primary humors (Akhlat): Damm (Blood), Balgham (Phlegm), Safra (Yellow Bile), and Sawda (Black Bile). Health is defined by innate equilibrium (Mizaj-e-Adil), maintained by innate vitality (Tabi'at).
              </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <h3 class="text-sm font-bold text-emerald-400">10-Ajnas Pulse Quantification</h3>
                <p class="text-xs text-[var(--muted)]">Evaluating pulse magnitude (Miqdar), quality of stroke (Kayfiyat), speed (Zamanah), artery consistency (Qawam), fullness (Mala), and emptiness (Khalwa) through 100 Hz DSP streaming.</p>
              </div>
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <h3 class="text-sm font-bold text-blue-400">Organ-Axis Cross-Talk</h3>
                <p class="text-xs text-[var(--muted)]">Diseases originate not from localized tissue damage in isolation, but through multi-organ humoral dysregulation, such as Kabid-Mida (Liver-Stomach) and Dimagh-Qalb (Brain-Heart) axes.</p>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // TAB: 12-STEP CARE JOURNEY
      if (state.tab === 'care_journey') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Clinical Continuum</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">The 12-Stage Closed-Loop Clinical Continuum</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Every patient journey in ZAYVORA Health OS navigates an unbroken chain of codified Unani assessment, dual diagnostic verification, 21 CFR Part 11 clinician sign-off, and longitudinal PROMs.
              </p>
            </div>

            <div class="space-y-4">
              ${clinicalStages.map((st, i) => `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                  <div class="flex items-start gap-4">
                    <span class="text-lg font-mono font-extrabold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-xl border border-emerald-500/20">${st.num}</span>
                    <div class="space-y-1">
                      <div class="flex items-center gap-2">
                        <h3 class="font-bold text-white text-base">${st.name}: ${st.title}</h3>
                        <span class="text-xs text-emerald-400 italic">(${st.latin})</span>
                      </div>
                      <p class="text-xs text-[var(--muted)] max-w-2xl leading-relaxed">${st.desc}</p>
                    </div>
                  </div>
                  <div class="text-right text-[11px] font-mono text-slate-400 bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] max-w-xs">
                    <strong class="text-teal-400 block mb-0.5">Verification Output</strong>
                    ${st.action}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: CLINICS & MATAB
      if (state.tab === 'clinics') {
        const clinicsList = [
          { name: "ZAYVORA Healthcare System - Central Hospital", type: "Flagship Hospital & Research Complex", address: "ZAYVORA Health Boulevard, Institutional Area, New Delhi 110062", phone: "+91 97738 82657", timing: "Open 24/7 • OPD: 8:00 AM – 8:00 PM", beds: "120 Beds • 8 Regimenal Suites" },
          { name: "ZAYVORA Matab™ Charminar Heritage Center", type: "Specialized Unani Matab & Pharmacy", address: "Heritage Health Quarter, Near Charminar, Hyderabad 500002", phone: "+91 97738 82657", timing: "OPD: 9:00 AM – 7:00 PM", beds: "Outpatient & Hijama Clinic" },
          { name: "ZAYVORA Integrative Care Center", type: "Clinical Matab & Telemedicine Hub", address: "Koramangala 4th Block, 80 Feet Road, Bengaluru 560034", phone: "+91 97738 82657", timing: "OPD: 9:30 AM – 6:30 PM", beds: "Tele-Health & Regimen Suite" },
          { name: "ZAYVORA Himalayan Herbal Center", type: "High-Altitude Botanical Dispensary", address: "Residency Road, Srinagar, Jammu & Kashmir 190001", phone: "+91 97738 82657", timing: "OPD: 10:00 AM – 5:00 PM", beds: "Specialty Cold-Chain Unit" }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Facility Directory</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Hospital Facilities & Specialized Matabs</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Visit any of our accredited clinical facilities for in-person 10-Ajnas pulse evaluation, tongue chromametry, and classical regimenal therapies (Hijama, Natool, Fasd).
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              ${clinicsList.map(c => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-4 flex flex-col justify-between">
                  <div class="space-y-2">
                    <div class="flex justify-between items-start">
                      <div>
                        <h3 class="font-bold text-white text-base">${c.name}</h3>
                        <span class="text-xs text-emerald-400 font-semibold block">${c.type}</span>
                      </div>
                      <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold">Active</span>
                    </div>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">📍 ${c.address}</p>
                    <div class="text-xs text-slate-300 space-y-1 pt-1">
                      <div>⏰ ${c.timing}</div>
                      <div>🏥 ${c.beds}</div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
                    <a href="tel:${c.phone}" class="text-xs font-mono text-emerald-400 font-bold hover:underline">📞 ${c.phone}</a>
                    <button onclick="switchRole('clinic')" class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition">Book OPD Token</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: DOCTORS & FACULTY
      if (state.tab === 'doctors') {
        const doctorsList = [
          { name: "Hakim Dr. Tariq Mansoor", degree: "BUMS, MD (Unani), PhD", specialty: "Moalajat (Internal Medicine) & Waja-ul-Mafasil", facility: "ZAYVORA Healthcare System - Central Hospital", timing: "Mon – Fri: 9:00 AM – 2:00 PM" },
          { name: "Dr. Aisha Siddiqui", degree: "BUMS, MD (Tahaffuzi wa Samaji Tibb)", specialty: "Preventive Medicine & Mizaj-e-Adil Lifestyle", facility: "ZAYVORA Healthcare System - Central Hospital", timing: "Tue – Sat: 10:00 AM – 3:00 PM" },
          { name: "Hakim Syed M. Akhtar", degree: "BUMS, MD (Ilaj bil-Tadbeer)", specialty: "Regimenal Therapy, Hijama & Musculoskeletal Rehabilitation", facility: "ZAYVORA Matab™ Specialized Therapy Suite", timing: "Mon – Thu: 11:00 AM – 4:00 PM" }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Medical Faculty</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Board-Certified Clinicians & Senior Tabeebs</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Our clinicians combine rigorous institutional Unani medical degrees with modern clinical pharmacology and diagnostic expertise.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              ${doctorsList.map(d => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-4 flex flex-col justify-between">
                  <div class="space-y-2">
                    <div class="w-14 h-14 rounded-2xl bg-emerald-950/60 border border-emerald-500/40 flex items-center justify-center text-2xl">
                      👨‍⚕️
                    </div>
                    <div>
                      <h3 class="font-bold text-white text-base">${d.name}</h3>
                      <span class="text-xs text-emerald-400 font-semibold block">${d.degree}</span>
                    </div>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${d.specialty}</p>
                    <div class="text-[11px] text-slate-300 pt-2 border-t border-[var(--border)] space-y-0.5">
                      <div>📍 ${d.facility}</div>
                      <div>⏰ ${d.timing}</div>
                    </div>
                  </div>
                  <button onclick="switchRole('clinic')" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition shadow">
                    Book Consultation →
                  </button>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: KNOWLEDGE CENTRE
      if (state.tab === 'knowledge') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Unani Knowledge Base</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Codified Botanical Knowledge Centre</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Explore standardized monographs from the Unani Pharmacopoeia of India (UPI) and National Formulary of Unani Medicine (NFUM).
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="flex justify-between items-center">
                  <h3 class="font-bold text-white text-base">Suranjan Talkh (Colchicum autumnale)</h3>
                  <span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 text-[10px] font-bold">Schedule E(1)</span>
                </div>
                <p class="text-xs text-[var(--muted)]">Active Constituent: Colchicine. Mizaj: Hot 3°, Dry 3°. Primary action: Tahleel-e-Riyah and Muhallil-e-Auraam in gout and knee osteoarthritis. Must be detoxified (Mudabbar) in cow milk.</p>
                <div class="text-[11px] text-teal-400 font-medium pt-1 border-t border-[var(--border)]">Musleh: Kateera (Astragalus gummifer) • Badal: Asgand</div>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="flex justify-between items-center">
                  <h3 class="font-bold text-white text-base">Asgand Nagori (Withania somnifera)</h3>
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[10px] font-bold">Classical Muqawwi</span>
                </div>
                <p class="text-xs text-[var(--muted)]">Active Constituent: Withanolides. Mizaj: Hot 2°, Dry 2°. Actions: Muqawwi-e-Aam, Muqawwi-e-Bah, and neuro-regenerative adaptor. Indicated in Su-e-Mizaj Barid Balghami.</p>
                <div class="text-[11px] text-teal-400 font-medium pt-1 border-t border-[var(--border)]">Musleh: Gond Katira & Shakar • Badal: Bahman Surkh</div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // TAB: FAQS
      if (state.tab === 'faqs') {
        const faqs = [
          { q: "What is ZAYVORA Health OS™?", a: "ZAYVORA Health OS is an enterprise healthcare operating system uniting classical Unani medicine (10-Ajnas pulse evaluation, Su-e-Mizaj, Organ-Axis) with contemporary biomedical intelligence, electronic health records, and clinician-governed AI." },
          { q: "How is patient safety ensured with Unani medicines?", a: "All formulations are AYUSH-GMP certified and HPLC fingerprinted. Schedule E(1) botanical ingredients undergo mandatory multi-day Mudabbar detoxification, supervised by pharmacognosists and verified by spectroscopy." },
          { q: "Does the AI copilot prescribe medicines autonomously?", a: "No. Under our strict 21 CFR Part 11 implementation, the AI operates exclusively as a clinical decision support advisor (safe_to_lock = False). Every prescription requires licensed clinician digital PIN sign-off." },
          { q: "Are services connected to Ayushman Bharat (ABDM)?", a: "Yes. ZAYVORA is integrated with ABDM M1, M2, and M3 standards, allowing seamless creation of ABHA numbers and secure sharing of encrypted health records with patient consent." },
          { q: "How do I book an OPD consultation or tele-consultation?", a: "You can book directly through the website or patient portal. Consultations are available both in-clinic at our Central Hospital and Matabs, or via secure WebRTC tele-health." }
        ];

        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Patient Questions</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Frequently Asked Questions</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Answers to common clinical, technological, and safety questions about ZAYVORA Health OS.
              </p>
            </div>

            <div class="space-y-4">
              ${faqs.map(f => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                  <h3 class="text-base font-bold text-emerald-400">${f.q}</h3>
                  <p class="text-xs text-[var(--muted)] leading-relaxed">${f.a}</p>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: CONTACT
      if (state.tab === 'contact') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-8 pb-12">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Hospital Concierge</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Contact ZAYVORA Healthcare System</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                For clinical appointments, tele-consultation inquiries, hospital casualty, or partnership coordination.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="text-2xl">📞</div>
                <h3 class="font-bold text-white text-sm">Direct Helpline</h3>
                <a href="tel:+919773882657" class="text-sm font-mono font-bold text-emerald-400 block">+91 97738 82657</a>
                <p class="text-[11px] text-[var(--muted)]">Available 24/7 for patient assistance</p>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="text-2xl">✉️</div>
                <h3 class="font-bold text-white text-sm">Official Email</h3>
                <span class="text-sm font-mono font-bold text-white block">concierge@zayvora.health</span>
                <p class="text-[11px] text-[var(--muted)]">Clinical & administrative inquiries</p>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="text-2xl">📍</div>
                <h3 class="font-bold text-white text-sm">Central Hospital</h3>
                <p class="text-xs text-slate-300">ZAYVORA Health Boulevard, Institutional Area, New Delhi 110062</p>
                <p class="text-[11px] text-[var(--muted)]">Open 24/7 with Casualty Desk</p>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <h3 class="font-bold text-white text-base">Send a Direct Message to Care Team</h3>
              <form onsubmit="event.preventDefault(); alert('Your inquiry has been logged. Our concierge will contact you at +91 97738 82657.');" class="space-y-4 text-xs">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-[var(--muted)] mb-1">Your Name</label>
                    <input required placeholder="Dr. / Mr. / Ms." class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
                  </div>
                  <div>
                    <label class="block text-[var(--muted)] mb-1">Phone Number</label>
                    <input required placeholder="+91 97738 82657" class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
                  </div>
                </div>
                <div>
                  <label class="block text-[var(--muted)] mb-1">Inquiry Category</label>
                  <select class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400">
                    <option>Consultation & Appointment Booking</option>
                    <option>Pharmacy & Prescription Inquiries</option>
                    <option>Hospital Facility & Regimenal Therapy</option>
                    <option>Research & Academic Collaboration</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[var(--muted)] mb-1">Message</label>
                  <textarea rows="4" required placeholder="Describe your clinical inquiry or question..." class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400"></textarea>
                </div>
                <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                  Send Clinical Message
                </button>
              </form>
            </div>
          </div>
        `;
        return;
      }

      // TAB: PRIVACY POLICY
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
                ZAYVORA Health OS™ complies with the Digital Personal Data Protection Act (DPDP), HIPAA, DISHA, and Ayushman Bharat Digital Mission (ABDM) guidelines.
              </p>
            </div>
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4 text-[var(--muted)] leading-relaxed">
              <p><strong class="text-white">1. PHI Encryption:</strong> All Protected Health Information (PHI) is encrypted at rest using AES-256-GCM and in transit using TLS 1.3 strict transport security.</p>
              <p><strong class="text-white">2. Clinician Gate:</strong> No clinical records or prescriptions are generated autonomously. All actions require 21 CFR Part 11 compliant digital signatures.</p>
              <p><strong class="text-white">3. Patient Consent:</strong> Health data sharing via ABDM health lockers is revocable at any time by the patient.</p>
              <p><strong class="text-white">4. Helpline:</strong> For data inquiries, reach our Data Protection Officer at privacy@zayvora.health or call +91 97738 82657.</p>
            </div>
          </div>
        `;
        return;
      }

      // TAB: TERMS OF SERVICE
      if (state.tab === 'terms') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-12 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Legal Terms</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl font-extrabold text-white">Terms of Clinical Telemedicine Service</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Terms governing clinical consultations, electronic prescriptions, and use of ZAYVORA Health OS™.
              </p>
            </div>
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4 text-[var(--muted)] leading-relaxed">
              <p><strong class="text-white">1. Telemedicine Consultation:</strong> Video consultations follow Telemedicine Practice Guidelines issued by the Ministry of AYUSH and National Medical Commission.</p>
              <p><strong class="text-white">2. Clinician Discretion:</strong> All diagnosis, diet plans, and prescriptions remain at the sole clinical discretion of the attending Senior Tabeeb.</p>
              <p><strong class="text-white">3. Emergency Care:</strong> Telemedicine is not for acute life-threatening emergencies. Patients in acute distress must immediately contact local hospital emergency or call +91 97738 82657.</p>
            </div>
          </div>
        `;
        return;
      }

      // TAB: 25 CANONICAL PAGES DIRECTORY
      if (state.tab === 'pages25') {
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">ZAYVORA Public Web Ecosystem</span>
                  <h2 class="text-2xl font-bold text-white mt-1">25 Canonical Public Pages Directory</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">Every page is fully rendered in-app with verified clinical content and zero 404 dead ends.</p>
                </div>
                <button onclick="viewWebsitePage('home')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">
                  ← Back to Public Home
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              ${publicPages.map(p => `
                <div class="bg-[var(--card)] p-4 rounded-xl border border-[var(--border)] hover:border-emerald-500/50 transition-colors flex flex-col justify-between space-y-3">
                  <div>
                    <div class="flex justify-between items-center mb-1">
                      <span class="font-bold text-white text-sm">${p.title}</span>
                      <span class="text-[10px] text-emerald-400 font-mono bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">${p.path}</span>
                    </div>
                    <p class="text-xs text-[var(--muted)] mt-1.5 leading-relaxed">${p.desc}</p>
                  </div>
                  <div class="pt-2 border-t border-[var(--border)] flex justify-between items-center text-[11px]">
                    <span class="text-emerald-400 font-semibold">✓ Fully Rendered</span>
                    <button onclick="viewWebsitePage('${p.key}')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs transition">Open Page →</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // DEFAULT TAB: 'home' - The Official Landing Page
      const st = clinicalStages[activeWebsiteStage];
      const calcMizajName = (previewMizajAnswers.temp === 'cold' && previewMizajAnswers.moisture === 'moist') ? "Balghami (Phlegmatic)" :
                            (previewMizajAnswers.temp === 'hot' && previewMizajAnswers.moisture === 'moist') ? "Damawi (Sanguine)" :
                            (previewMizajAnswers.temp === 'hot' && previewMizajAnswers.moisture === 'dry') ? "Safrawi (Choleric)" : "Sawdawi (Melancholic)";

      container.innerHTML = `
        <div class="space-y-12 pb-12">
          
          <!-- Hero Banner -->
          <div class="relative overflow-hidden p-8 md:p-12 rounded-3xl bg-gradient-to-b from-[#0F172A] via-[#0D1526] to-[#0A0F1D] border border-[#334155] text-center space-y-5">
            <div class="inline-flex items-center gap-2 px-4 py-1 rounded-full bg-[#0D9488]/15 border border-[#0D9488]/30 text-[#2DD4BF] text-xs font-semibold">
              <span>✨ Codified Greco-Arab Science + Modern Biomedical Intelligence</span>
            </div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-white max-w-4xl mx-auto leading-tight">
              Ancient Wisdom. Modern Science. <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#2DD4BF] to-emerald-400">Intelligent Healthcare.</span>
            </h1>
            <p class="text-xs sm:text-sm md:text-base text-[#94A3B8] max-w-2xl mx-auto leading-relaxed">
              ZAYVORA Health OS™ unites 1,000 years of codified Unani medicine with state-of-the-art clinical AI, longitudinal Mizaj profiling, organ-axis cross-talk, and 21 CFR Part 11 medical governance.
            </p>
            <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button onclick="switchRole('clinic')" class="px-6 py-3 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-xs shadow-xl transition">
                Book Integrative Consultation
              </button>
              <button onclick="viewWebsitePage('philosophy')" class="px-6 py-3 rounded-xl border border-[#334155] bg-[#1E293B]/70 hover:bg-[#1E293B] text-white font-semibold text-xs transition">
                Explore Clinical Philosophy →
              </button>
              <button onclick="viewWebsitePage('products')" class="px-6 py-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20 text-xs font-semibold transition">
                View 10-Product Store
              </button>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-6 pt-4 text-[11px] text-[#94A3B8]">
              <span>✓ AYUSH GMP Certified</span>
              <span>✓ HPLC Active Fingerprinted</span>
              <span>✓ Schedule E(1) Mudabbar Verified</span>
              <span>✓ ABDM & FHIR R4 Ready</span>
            </div>
          </div>

          <!-- Live Diagnostic Hardware Telemetry Bar -->
          <div class="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#1E293B] pb-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <h3 class="text-sm font-bold text-white">Live Clinical Diagnostic Hardware & DSP Streams</h3>
              </div>
              <span class="px-3 py-1 rounded-lg bg-[#1E293B] text-emerald-400 font-mono font-bold text-[10px] border border-emerald-500/30">
                100 Hz Streaming DSP • 12ms Latency
              </span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-center">
              <div class="lg:col-span-5 p-4 rounded-2xl bg-[#0A0F1D] border border-[#1E293B] space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-white flex items-center gap-1">
                    <span class="text-teal-400">📊</span> Nabz 10-Ajnas Arterial PPG Wave
                  </span>
                  <span class="font-mono text-emerald-400 font-bold">72 BPM (Bat'ee)</span>
                </div>
                <canvas id="preview-pulse-canvas" width="340" height="90" class="w-full h-24 rounded-lg bg-[#0F172A] border border-[#1E293B]"></canvas>
                <div class="grid grid-cols-3 gap-2 text-[10px] text-[#94A3B8] font-mono text-center">
                  <div class="p-1 rounded bg-[#1E293B]"><strong class="text-white block">Kayfiyat</strong>Layyin</div>
                  <div class="p-1 rounded bg-[#1E293B]"><strong class="text-white block">Miqdar</strong>Azeem</div>
                  <div class="p-1 rounded bg-[#1E293B]"><strong class="text-white block">Zamanah</strong>Bat'ee</div>
                </div>
              </div>

              <div class="lg:col-span-7 grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div class="p-3.5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1.5 text-xs">
                  <div class="flex justify-between items-center"><span class="text-lg">👅</span><span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300">LISAN</span></div>
                  <h4 class="font-bold text-white text-xs">Tongue Camera</h4>
                  <div class="text-[10px] text-[#94A3B8] space-y-0.5">
                    <div>Coating: <strong class="text-white">Saburra (White)</strong></div>
                    <div>Moisture: <strong class="text-emerald-400">68% Rutubat</strong></div>
                    <div>Humoral: <strong class="text-amber-400">Balghami</strong></div>
                  </div>
                </div>

                <div class="p-3.5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1.5 text-xs">
                  <div class="flex justify-between items-center"><span class="text-lg">❄️</span><span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">COLD-CHAIN</span></div>
                  <h4 class="font-bold text-white text-xs">Dispensary IoT</h4>
                  <div class="text-[10px] text-[#94A3B8] space-y-0.5">
                    <div>Temp: <strong class="text-emerald-400">19.4°C Safe</strong></div>
                    <div>Humidity: <strong class="text-white">42% RH</strong></div>
                    <div>FEFO: <strong class="text-emerald-400">Locked</strong></div>
                  </div>
                </div>

                <div class="p-3.5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1.5 text-xs">
                  <div class="flex justify-between items-center"><span class="text-lg">📡</span><span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300">BLE MESH</span></div>
                  <h4 class="font-bold text-white text-xs">Wearables Gateway</h4>
                  <div class="text-[10px] text-[#94A3B8] space-y-0.5">
                    <div>Nodes: <strong class="text-purple-300">4 Active</strong></div>
                    <div>SpO2: <strong class="text-emerald-400">98% Normal</strong></div>
                    <div>Relapse: <strong class="text-emerald-400">0.04 (Low)</strong></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Interactive 12-Stage Continuum -->
          <div class="space-y-6">
            <div class="text-center space-y-1">
              <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Clinical Framework</span>
              <h2 class="text-2xl font-bold text-white">The 12-Stage Closed-Loop Clinical Continuum</h2>
              <p class="text-xs text-[#94A3B8]">Click any stage below to inspect the verified clinical mechanics.</p>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
              ${clinicalStages.map((stage, idx) => `
                <button onclick="setWebsiteStage(${idx})" class="p-3 rounded-xl text-left border transition-all ${idx === activeWebsiteStage ? 'bg-[#0D9488]/20 border-[#2DD4BF] shadow-lg' : 'bg-[#1E293B] border-[#334155] hover:border-[#0D9488]/50'}">
                  <div class="flex justify-between items-center text-[10px] font-mono font-bold">
                    <span class="${idx === activeWebsiteStage ? 'text-[#2DD4BF]' : 'text-slate-500'}">${stage.num}.</span>
                    <span class="${idx === activeWebsiteStage ? 'text-white' : 'text-slate-400'}">${stage.name}</span>
                  </div>
                  <div class="text-[10px] text-slate-200 mt-1 truncate font-semibold">${stage.title}</div>
                </button>
              `).join('')}
            </div>

            <div class="p-6 rounded-2xl bg-gradient-to-r from-[#1E293B] via-[#0F172A] to-[#1E293B] border border-[#2DD4BF]/40 space-y-3">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-3">
                <div>
                  <span class="text-[10px] font-mono font-bold text-[#2DD4BF]">STAGE ${st.num} OF 12</span>
                  <h3 class="text-lg font-bold text-white">${st.name}: ${st.title}</h3>
                  <span class="text-xs text-emerald-400 italic">${st.latin}</span>
                </div>
                <span class="px-3 py-1 rounded-full bg-[#0D9488]/20 border border-[#0D9488]/40 text-[#2DD4BF] text-[10px] font-semibold">
                  Verified Protocol
                </span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div>
                  <strong class="text-slate-400 block mb-1 uppercase text-[10px]">Clinical Mechanism</strong>
                  <p class="text-slate-300 leading-relaxed">${st.desc}</p>
                </div>
                <div class="bg-[#0A0F1D] p-3 rounded-xl border border-[#334155]">
                  <strong class="text-teal-400 block mb-1 uppercase text-[10px]">Clinical Execution & Safety Output</strong>
                  <p class="text-slate-400 font-mono text-[11px]">${st.action}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 4-Stage Afaal Treatment Cascade -->
          <div class="space-y-6">
            <div class="text-center space-y-1">
              <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Humoral Healing Protocol</span>
              <h2 class="text-2xl font-bold text-white">The ZAYVORA Afaal Treatment Cascade</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-emerald-400">STAGE 01</span><span class="text-[10px] text-slate-500">Days 1 - 14</span></div>
                <h4 class="text-base font-bold text-white">Tanqiya</h4>
                <span class="text-xs text-[#2DD4BF] block font-semibold">Humoral Cleansing & Detox</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Concoction and elimination of accumulated cold, phlegmatic matter (Mawad-e-Fasida) via Munzaj-Mushil therapy and Hijama.</p>
              </div>
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-blue-400">STAGE 02</span><span class="text-[10px] text-slate-500">Days 15 - 30</span></div>
                <h4 class="text-base font-bold text-white">Tahleel</h4>
                <span class="text-xs text-blue-400 block font-semibold">Resolution of Inflammation</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Dissolution of deep-seated peri-articular exudates and microvascular stasis via medicated warm fomentation (Natool) and Zimad.</p>
              </div>
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-purple-400">STAGE 03</span><span class="text-[10px] text-slate-500">Days 31 - 60</span></div>
                <h4 class="text-base font-bold text-white">Taqwiyaat</h4>
                <span class="text-xs text-purple-400 block font-semibold">Organ Restoration</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Strengthening target organs and neural pathways (Muqawwiyat-e-A'za) to rebuild stamina and prevent relapse.</p>
              </div>
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-amber-400">STAGE 04</span><span class="text-[10px] text-slate-500">Lifelong</span></div>
                <h4 class="text-base font-bold text-white">Hifz</h4>
                <span class="text-xs text-amber-400 block font-semibold">Preservation & Homeostasis</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Long-term equilibrium via tailored dietetics (Ilaj bil-Ghiza) and adherence to the 6 Life Essentials (Asbab-e-Sittah).</p>
              </div>
            </div>
          </div>

          <!-- Interactive Mini Mizaj Self-Assessment -->
          <div class="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-4">
            <div class="text-center space-y-1">
              <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Individualized Constitution</span>
              <h3 class="text-xl font-bold text-white">Preliminary Mizaj Calculator</h3>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
              <div class="p-3 bg-[#1E293B] rounded-xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">1. Thermal Sensation</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('temp', 'hot')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.temp === 'hot' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">🔥 Warm</button>
                  <button onclick="setPreviewMizaj('temp', 'cold')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.temp === 'cold' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">❄️ Cold</button>
                </div>
              </div>
              <div class="p-3 bg-[#1E293B] rounded-xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">2. Skin Quality</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('moisture', 'moist')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.moisture === 'moist' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">💧 Moist</button>
                  <button onclick="setPreviewMizaj('moisture', 'dry')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.moisture === 'dry' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">🍂 Dry</button>
                </div>
              </div>
              <div class="p-3 bg-[#1E293B] rounded-xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">3. Skeletal Frame</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('physique', 'broad')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.physique === 'broad' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">🛡️ Broad</button>
                  <button onclick="setPreviewMizaj('physique', 'slender')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.physique === 'slender' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">⚡ Slender</button>
                </div>
              </div>
              <div class="p-3 bg-[#1E293B] rounded-xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">4. Sleep Depth</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('sleep', 'deep')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.sleep === 'deep' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">😴 Deep</button>
                  <button onclick="setPreviewMizaj('sleep', 'light')" class="py-1.5 rounded text-xs font-semibold ${previewMizajAnswers.sleep === 'light' ? 'bg-[#0D9488] text-white' : 'bg-[#0F172A] text-slate-400'}">🌙 Light</button>
                </div>
              </div>
            </div>
            <div class="p-4 rounded-xl bg-[#1E293B] border border-[#2DD4BF]/40 flex flex-col sm:flex-row justify-between items-center gap-3">
              <div>
                <span class="text-xs text-[#94A3B8]">Estimated Temperament: </span>
                <strong class="text-white text-sm">${calcMizajName}</strong>
                <span class="text-xs text-emerald-400 font-mono ml-2">Affinity: Digestive & Respiratory Axis</span>
              </div>
              <button onclick="switchRole('clinic')" class="px-5 py-2 bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold rounded-xl shadow">
                Book Formal 10-Ajnas Pulse Exam →
              </button>
            </div>
          </div>

          <!-- 10 Formulations Store Showcase -->
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-2 border-b border-[#334155] pb-3">
              <div>
                <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Botanical Therapeutics</span>
                <h3 class="text-2xl font-bold text-white">ZAYVORA Herbals Portfolio</h3>
                <p class="text-xs text-[#94A3B8]">GMP manufactured, HPLC verified, Schedule E(1) Mudabbar purified.</p>
              </div>
              <button onclick="viewWebsitePage('products')" class="px-4 py-2 border border-[#334155] text-xs font-bold text-[#2DD4BF] hover:bg-[#1E293B] rounded-xl">
                Open Cart & Dispensary (${herbalsCart.length} items) →
              </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
              ${herbalsProducts.map(p => `
                <div class="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col justify-between space-y-3 hover:border-teal-500/50 transition">
                  <div class="space-y-1.5">
                    <div class="flex justify-between items-center">
                      <span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF]">${p.category}</span>
                      <span class="text-xs font-bold text-white">₹${p.price}</span>
                    </div>
                    <h4 class="text-xs font-bold text-white">${p.name}</h4>
                    <p class="text-[10px] text-[#94A3B8] line-clamp-2">${p.desc}</p>
                  </div>
                  <div class="pt-2 border-t border-[#334155] flex justify-between items-center">
                    <button onclick="viewWebsitePage('knowledge')" class="text-[10px] text-slate-400 hover:text-white">Monograph</button>
                    <button onclick="addToHerbalsCart('${p.id}')" class="px-2.5 py-1 bg-[#0D9488] hover:bg-[#14B8A6] text-white text-[10px] font-bold rounded-lg transition">
                      + Add
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Bottom Nav to 25 Pages -->
          <div class="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
              <h4 class="font-bold text-white text-sm">Explore All 25 Canonical Web Pages</h4>
              <p class="text-xs text-[#94A3B8]">Browse the complete public site structure including clinical programs, conditions, research, and ethics.</p>
            </div>
            <button onclick="viewWebsitePage('pages25')" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">
              View 25 Canonical Pages Directory →
            </button>
          </div>

        </div>
      `;

      initWebsiteWaveform();
    }
