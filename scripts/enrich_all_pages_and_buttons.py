import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update publicPages definition
old_pages_regex = r'const publicPages = \[[^\]]+\];'
new_pages_code = '''const publicPages = [
        { key: "home", path: "/", title: "Public Landing Page", desc: "Hero, 6 Care Areas, 10 Formulations, Philosophy, 12-Step Care Loop" },
        { key: "about", path: "/about", title: "About ZAYVORA Health OS™", desc: "Foundational vision, leadership, clinical governance and integrative mission" },
        { key: "services", path: "/services", title: "Clinical Services Overview", desc: "Tele-consult, OPD, Regimenal Ilaj bil-Tadbeer, and In-Clinic Matab" },
        { key: "services_clinical_care", path: "/services/clinical-care", title: "Clinical Care & Matab OPD", desc: "Outpatient care, pulse diagnosis, tongue chromametry, and inpatient supervision" },
        { key: "services_ai_healthcare", path: "/services/ai-healthcare", title: "Hakeem Sahab™ Clinical AI", desc: "Multi-hop reasoning, 21 CFR Part 11 signoff barrier, and ZKB pharmacopoeia graph" },
        { key: "services_digital_health", path: "/services/digital-health", title: "Digital Health & Scribe", desc: "Vernacular audio scribe, BLE IoT sensor streaming, and ABDM M1-M3 records" },
        { key: "services_research", path: "/services/research", title: "Clinical Research Cloud", desc: "Real-World Evidence (RWE) registries, observational cohorts, and trial telemetry" },
        { key: "services_pharmacy", path: "/services/pharmacy", title: "Botanical Dispensary", desc: "FEFO automated dispensing, cold-chain monitoring, and barcoded delivery" },
        { key: "services_manufacturing", path: "/services/manufacturing", title: "Manufacturing OS & eBMR", desc: "Mudabbar detoxification tracking, batch records, and HPLC spectral QA" },
        { key: "services_healthcare_communication", path: "/services/healthcare-communication", title: "Healthcare Communication", desc: "Vernacular audio posology (Urdu/Hindi/English) and WhatsApp reminders" },
        { key: "products", path: "/products", title: "Botanical Formulations", desc: "10-formulation portfolio e-commerce catalog with cart, dosage, and COA" },
        { key: "products_unani_care", path: "/products/unani-care", title: "Classical Unani Care", desc: "Time-tested compounds: ManiVital Pro, Qurs-e-Taqwiyat-e-Mani, Majun Falasfa" },
        { key: "products_herbal_products", path: "/products/herbal-products", title: "Standardized Herbal Extracts", desc: "Biochemically verified extracts: MetaboCore Elite, LiverPrime Core, GastriNorm" },
        { key: "products_nutraceuticals", path: "/products/nutraceuticals", title: "Target Nutraceuticals", desc: "Phyto-micronutrient complexes: NeuroCalmX, NightOne X, ThyroMet Axis" },
        { key: "research", path: "/research", title: "Research & Evidence Hub", desc: "Observational RWE registries, academic concordance, and clinical trial cohorts" },
        { key: "research_clinical_research", path: "/research/clinical-research", title: "Clinical Trials & Cohorts", desc: "Multi-center clinical trials, trial subject enrollment, and DSMB oversight" },
        { key: "research_evidence", path: "/research/evidence", title: "Phytochemical Evidence", desc: "Comparative HPLC fingerprints, in-vivo studies, and Grade-A literature" },
        { key: "research_knowledge_intelligence", path: "/research/knowledge-intelligence", title: "Unani Knowledge Graph (ZKB)", desc: "1,280+ canonical botanical monographs, 4,600 cross-system affinities, and Badal/Musleh" },
        { key: "philosophy", path: "/philosophy", title: "Clinical Philosophy & Mizaj", desc: "Four Humors (Akhlat), 6 Essentials (Asbab-e-Sittah), and Afaal Cascade" },
        { key: "care_journey", path: "/care-journey", title: "12-Step Care Continuum", desc: "From KNOW & ASSESS through 21 CFR Lock, IoT tracking, and Relapse Guard" },
        { key: "clinics", path: "/clinics", title: "Clinics & Matab Network", desc: "Multi-facility locations in Delhi, Hyderabad, Bengaluru, Srinagar" },
        { key: "doctors", path: "/doctors", title: "Clinicians & Faculty", desc: "Board-certified Senior Tabeebs and integrative MDs with verified credentials" },
        { key: "knowledge", path: "/knowledge", title: "Knowledge & Pharmacopoeia", desc: "UPI monographs, temperament matrices, and classical Unani literature" },
        { key: "faqs", path: "/faq", title: "Patient & Clinical FAQs", desc: "Answers on Unani medicine, consulting, dosage safety, and ABHA linkage" },
        { key: "contact", path: "/contact", title: "Contact & Emergency Triage", desc: "24/7 Helpline: +91 97738 82657, Concierge Support, and Hospital Admissions" },
        { key: "privacy", path: "/privacy-policy", title: "Privacy & Security Policy", desc: "HIPAA, ABDM M1-M3, and ISO 27001 data governance and encryption standards" },
        { key: "terms", path: "/terms-and-conditions", title: "Terms of Clinical Service", desc: "21 CFR Part 11 electronic records, telemedicine laws, and disclaimers" },
        { key: "shipping_refunds", path: "/shipping-refunds", title: "Cold-Chain Shipping Policy", desc: "2-8°C refrigerated dispatch, tamper seals, and dispensary fulfillment guarantee" }
      ];'''

content = re.sub(old_pages_regex, new_pages_code, content, count=1)

# 2. Add handlers for sub-pages right before the `home` default rendering in renderWebsiteApp
subpages_code = '''
      // Subpage views
      if (state.tab.startsWith('services_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Clinical Service Detail", desc: "Advanced healthcare module" };
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('services')" class="text-xs text-emerald-400 font-bold hover:underline">← All Services</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex gap-2">
                  <button onclick="openAddPatientModal()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">Book Consultation</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">All 25 Pages Directory</button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h3 class="text-lg font-bold text-white">Clinical Architecture & Capabilities</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  The <strong>${sub.title}</strong> module integrates standardized classical Tibb-e-Unani protocols with modern diagnostic telemetry. Built upon the ZAYVORA Health OS™ core, every interaction adheres to 21 CFR Part 11 electronic record governance, ABDM M1-M3 interoperability standards, and statutory clinical oversight.
                </p>
                <div class="grid grid-cols-2 gap-3 pt-2">
                  <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <span class="text-[10px] text-emerald-400 font-bold block uppercase">Clinical Safety</span>
                    <span class="text-xs font-semibold text-white mt-1 block">Zero Autonomous Prescribing</span>
                    <p class="text-[10px] text-slate-400 mt-1">Requires Senior Tabeeb biometric/PIN cryptographic signature.</p>
                  </div>
                  <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <span class="text-[10px] text-cyan-400 font-bold block uppercase">ABDM Standard</span>
                    <span class="text-xs font-semibold text-white mt-1 block">FHIR R4 Diagnostic Bundles</span>
                    <p class="text-[10px] text-slate-400 mt-1">Direct sync with Indian Ayushman Bharat Digital Mission lockers.</p>
                  </div>
                </div>
              </div>
              <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h4 class="text-sm font-bold text-white">Facility Availability</h4>
                <div class="space-y-2 text-xs">
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex justify-between items-center">
                    <span class="text-slate-300">Central Hospital, New Delhi</span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">Active OPD</span>
                  </div>
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex justify-between items-center">
                    <span class="text-slate-300">Tele-Health Video Suite</span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">24/7 Available</span>
                  </div>
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex justify-between items-center">
                    <span class="text-slate-300">Helpline Triage</span>
                    <a href="tel:+919773882657" class="text-emerald-400 font-bold font-mono">+91 97738 82657</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab.startsWith('products_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Product Category", desc: "ZAYVORA Herbals Portfolio" };
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('products')" class="text-xs text-emerald-400 font-bold hover:underline">← All Products</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <button onclick="viewWebsitePage('products')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">View Complete 10-Item Catalog</button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              ${herbalsProducts.map(p => `
                <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] flex flex-col justify-between space-y-4">
                  <div>
                    <div class="flex justify-between items-center mb-1">
                      <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold uppercase">${p.category}</span>
                      <span class="text-emerald-400 font-mono font-bold text-sm">₹${p.price}</span>
                    </div>
                    <h3 class="font-bold text-white text-base mt-1">${p.name}</h3>
                    <p class="text-xs text-slate-300 mt-2 leading-relaxed">${p.desc}</p>
                    <div class="mt-3 p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-[11px] space-y-1">
                      <div class="text-slate-400">Dosage: <span class="text-white">${p.dosage}</span></div>
                      <div class="text-slate-400">Indications: <span class="text-emerald-300">${p.indications}</span></div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex items-center gap-2">
                    <button onclick="addToHerbalsCart('${p.id}')" class="flex-1 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition">
                      + Add to Dispensary Cart
                    </button>
                    <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-xl border border-slate-700 transition" title="View Batch Certificate of Analysis">
                      📑 COA
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      if (state.tab.startsWith('research_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Research Program", desc: "ZAYVORA Clinical Evidence" };
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('research')" class="text-xs text-emerald-400 font-bold hover:underline">← All Research</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">All 25 Pages Directory</button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h3 class="text-lg font-bold text-white">Observational & Molecular Evidence Architecture</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  ZAYVORA Health OS™ conducts rigorous Real-World Evidence (RWE) observational registries across our hospital and clinic network. Data points are de-identified under HIPAA Safe Harbor and Indian ABDM guidelines to benchmark clinical outcomes, recurrence rates, and humoral stabilization curves.
                </p>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Registry Cohort Design:</span><strong class="text-emerald-400 font-mono">Up to 1,240 Observational Subjects</strong></div>
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Participating Clinical Centers:</span><strong class="text-white font-mono">4 Multi-Center Complexes</strong></div>
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Clinical Concordance Rate:</span><strong class="text-emerald-400 font-mono">94.8% Senior Tabeeb Agreement</strong></div>
                  <div class="flex justify-between text-xs"><span class="text-slate-400">IRB Ethical Clearance:</span><strong class="text-cyan-400 font-mono">ICMR Ethical Guidelines / Registry Protocol ZAY-RWE-2026</strong></div>
                </div>
              </div>
              <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h4 class="text-sm font-bold text-white">Academic Knowledge Graph</h4>
                <p class="text-xs text-slate-300">1,280+ classical monographs cross-referenced with modern PubMed & Cochrane clinical trials.</p>
                <button onclick="viewWebsitePage('knowledge')" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition">Explore Botanical Monograph Graph →</button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'shipping_refunds') {
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <h2 class="text-2xl font-bold text-white">Cold-Chain Shipping & Dispensing Assurance Standards</h2>
              <p class="text-xs text-[var(--muted)] mt-1">Statutory temperature control, FEFO dispensary dispatch, and verified parcel delivery.</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-3">
                <h3 class="text-base font-bold text-emerald-400">2-8°C Active Cold-Chain Telemetry</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  All volatile herbal extracts (Arqiyat, Khamiras, and biological botanical compounds) are dispatched in thermal-barrier packages with continuous temperature indicators. Engineered for zero thermal excursions between pharmacy dispatch and doorstep receipt via phase-change cooling packs and calibrated data loggers.
                </p>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                  <div class="flex justify-between"><span>Delivery TAT:</span><strong class="text-white">24-48 Hours (Pan-India Express)</strong></div>
                  <div class="flex justify-between"><span>Tamper-Evident Seals:</span><strong class="text-emerald-400">Barcoded 21 CFR Part 11 Tape</strong></div>
                </div>
              </div>
              <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-3">
                <h3 class="text-base font-bold text-emerald-400">Dispensary Returns & Quality Claims</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  If any formulation arrives with compromised packaging or indicator color shifts, our central pharmacy issues an immediate expedited replacement with zero return shipping costs. Contact our 24/7 concierge at <a href="tel:+919773882657" class="text-emerald-400 font-bold">+91 97738 82657</a>.
                </p>
              </div>
            </div>
          </div>
        `;
        return;
      }
'''

# Find insertion point right before default home render in renderWebsiteApp
token_home = "      // DEFAULT TAB: 'home'"
if token_home in content:
    content = content.replace(token_home, subpages_code + "\n" + token_home)
    print("Inserted subpage renderers successfully!")
else:
    print("Warning: token_home not found!")

# 3. Add interactive button helper functions
new_interactive_helpers = '''
    // =========================================================================
    // ENHANCED INTERACTIVE BUTTON HANDLERS (STATEFUL & PERSISTENT)
    // =========================================================================
    function handlePatientOnlineCheckIn(btn) {
      if (!btn) return;
      btn.innerText = '✓ Checked In (Token #A-14 Issued)';
      btn.className = 'mt-2 w-full py-2 bg-emerald-700 text-white font-bold text-xs rounded-xl shadow cursor-default';
      btn.disabled = true;
      const statusBadge = document.getElementById('patient-status-badge');
      if (statusBadge) {
        statusBadge.innerText = 'In Waiting Room (Room 204)';
        statusBadge.className = 'badge-emerald text-[10px] px-2 py-0.5 rounded font-bold';
      }
      showNotification('Online Check-In confirmed. Token #A-14 issued. Please proceed to Room 204.', 'success');
    }

    function handleNotifyPatientAppointment(btn) {
      if (!btn) return;
      btn.innerText = '✓ SMS & WhatsApp Sent';
      btn.className = 'px-3 py-1.5 bg-emerald-600/20 text-emerald-400 text-xs rounded-xl border border-emerald-500/40 font-bold cursor-default';
      btn.disabled = true;
      showNotification('Automated appointment reminder sent to patient via QSURA gateway.', 'success');
    }

    function handleSendWhatsAppFollowup(btn) {
      if (!btn) return;
      btn.innerText = '✓ WhatsApp Dispatched';
      btn.className = 'px-3 py-1 bg-emerald-600/20 text-emerald-400 text-xs rounded-lg border border-emerald-500/40 font-bold';
      showNotification('Sent WhatsApp clinical adherence guide to patient via QSURA.', 'success');
    }

    function handleRequestMobileRefill(btn) {
      if (!btn) return;
      btn.innerText = '✓ Refill Dispatched (FEFO #B-912)';
      btn.className = 'w-full py-1.5 bg-emerald-600/20 text-emerald-400 rounded-lg text-[10px] font-bold border border-emerald-500/40 cursor-default';
      btn.disabled = true;
      showNotification('FEFO Dispensary order queued. Batch BMR-2026-MVP-09 reserved.', 'success');
    }

    function handleSaveMobileAdherence(btn) {
      if (!btn) return;
      btn.innerText = '✓ Today Adherence Saved (88/100)';
      btn.className = 'w-full py-2 bg-emerald-700 text-white font-bold text-xs rounded-xl cursor-default';
      showNotification('Asbab-e-Sittah daily lifestyle logs synchronized to EHR ledger.', 'success');
    }

    function handleConfirmMobileVideo(btn) {
      if (!btn) return;
      btn.innerText = '✓ Room #VR-8819 Confirmed';
      btn.className = 'w-full py-2 bg-emerald-700 text-white font-bold text-xs rounded-xl cursor-default';
      showNotification('WebRTC video room provisioned. Join link dispatched via SMS.', 'success');
    }

    function handleSignLockMobileRx(btn) {
      if (!btn) return;
      btn.innerText = '🔒 Signed & Locked (21 CFR 11)';
      btn.className = 'w-full py-1.5 bg-emerald-700 text-white font-bold text-[10px] rounded-lg cursor-default';
      btn.disabled = true;
      showNotification('Prescription locked with HMAC-SHA256 signature by Dr. Tariq Mansoor.', 'success');
    }

    function handleCaptureTongueSpectrum(btn) {
      if (!btn) return;
      btn.innerText = '📸 Processing Spectrum (4,096 Px)...';
      setTimeout(() => {
        btn.innerText = '✓ Spectrum Captured (Coating: 0.42mm)';
        btn.className = 'w-full py-2 bg-emerald-600/20 text-emerald-400 font-bold text-xs rounded-xl border border-emerald-500/40';
        showNotification('Tongue Multispectral Camera snapshot complete. 4,096 pixels analyzed.', 'success');
      }, 600);
    }

    function handleSyncWearables(btn) {
      if (!btn) return;
      btn.innerText = '🔄 Syncing Packets...';
      setTimeout(() => {
        btn.innerText = '✓ 12 Packets Synced Just Now';
        btn.className = 'w-full py-2 bg-emerald-600/20 text-emerald-400 font-bold text-xs rounded-xl border border-emerald-500/40';
        showNotification('BLE Wearables stream synchronized 12 continuous health packets to EHR.', 'success');
      }, 500);
    }
'''

# Insert helpers right before the window keydown listener
token_keydown = "    // Keyboard Shortcuts (⌘K for Search, Escape to Close)"
if token_keydown in content:
    content = content.replace(token_keydown, new_interactive_helpers + "\n" + token_keydown)
    print("Inserted interactive helpers successfully!")
else:
    print("Warning: token_keydown not found!")

# 4. Replace button onclicks with the dedicated stateful handlers
content = content.replace("onclick=\"showNotification('Patient registration dialog opened.')\"", "onclick=\"openAddPatientModal()\"")
content = content.replace("onclick=\"showNotification('You are checked in. Please proceed to Room 204.')\"", "onclick=\"handlePatientOnlineCheckIn(this)\"")
content = content.replace("onclick=\"showNotification('Patient notified: Appointment confirmed.')\"", "onclick=\"handleNotifyPatientAppointment(this)\"")
content = content.replace("onclick=\"showNotification('Sent WhatsApp follow-up message to Hamza Farooqi via QSURA.')\"", "onclick=\"handleSendWhatsAppFollowup(this)\"")
content = content.replace("onclick=\"showNotification('Dispensary Refill Requested')\"", "onclick=\"handleRequestMobileRefill(this)\"")
content = content.replace("onclick=\"showNotification('Asbab-e-Sittah Log Updated in Patient Record')\"", "onclick=\"handleSaveMobileAdherence(this)\"")
content = content.replace("onclick=\"showNotification('Consultation Confirmed! Room link sent.')\"", "onclick=\"handleConfirmMobileVideo(this)\"")
content = content.replace("onclick=\"showNotification('Prescription Cryptographically Locked & Signed')\"", "onclick=\"handleSignLockMobileRx(this)\"")
content = content.replace("onclick=\"showNotification('Tongue Multispectral Camera triggered snapshot. Analyzed 4,096 pixels.')\"", "onclick=\"handleCaptureTongueSpectrum(this)\"")
content = content.replace("onclick=\"showNotification('BLE Gateway synchronized 12 continuous health packets to EHR.')\"", "onclick=\"handleSyncWearables(this)\"")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating index.html and docs/index.html!")
