#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Public Web Ecosystem Architecture & Page Integration
Integrates all 25 public pages into 5 coherent Medical Hubs:
1. Clinical Services Hub (/services)
2. Botanical Formulations Hub (/products)
3. Research, Evidence & Knowledge Institute (/research)
4. Clinical Philosophy & Care Journey (/philosophy)
5. Hospital Network, Faculty & Governance (/clinics, /about, /contact)

Eliminates the scattered directory feeling by:
- Adding interactive contextual Sub-Navigation Pills to each Hub
- Upgrading subpages with rich clinical domain content and parent hub tabs
- Transforming 'pages25' into a world-class Executive System Architecture Blueprint
- Synchronizing both index.html and docs/index.html
"""
import re
import sys

def generate_subnav_js():
    return '''    function getWebsiteHubSubnav(currentTab) {
      // 1. Clinical Services Hub
      if (currentTab === 'services' || currentTab.startsWith('services_')) {
        const items = [
          { key: 'services', label: '📋 All Services Overview' },
          { key: 'services_clinical_care', label: '🩺 Matab & OPD Care' },
          { key: 'services_ai_healthcare', label: '🤖 Hakeem Sahab™ AI' },
          { key: 'services_digital_health', label: '📱 Digital Health & Scribe' },
          { key: 'services_pharmacy', label: '💊 Dispensary (FEFO)' },
          { key: 'services_manufacturing', label: '🏭 Manufacturing OS' },
          { key: 'services_healthcare_communication', label: '🔊 Posology Audio' },
          { key: 'services_research', label: '🔬 Research Cloud' }
        ];
        return `
          <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-8 shadow-lg">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">🩺 Clinical Care &amp; Services Hub</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">7 Integrated Modules</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-slate-400 hover:text-emerald-400 transition flex items-center gap-1 font-semibold">
                <span>🗺️</span> Architecture Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-950/50' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 2. Botanical Formulations Hub
      if (currentTab === 'products' || currentTab.startsWith('products_') || currentTab === 'shipping_refunds') {
        const items = [
          { key: 'products', label: '🌿 All 10 Formulations' },
          { key: 'products_unani_care', label: '🏺 Classical Unani' },
          { key: 'products_herbal_products', label: '🧪 Standardized Extracts' },
          { key: 'products_nutraceuticals', label: '🧬 Target Nutraceuticals' },
          { key: 'shipping_refunds', label: '📦 Cold-Chain Shipping' }
        ];
        return `
          <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-8 shadow-lg">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">🌿 Botanical Therapeutics Hub</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">AYUSH-GMP Certified</span>
              </div>
              <div class="flex items-center gap-3">
                <button onclick="switchRole('herbals'); switchTab('cart');" class="text-[11px] text-emerald-400 font-bold hover:underline">
                  🛒 Cart (${herbalsCart.length})
                </button>
                <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-slate-400 hover:text-emerald-400 transition font-semibold">
                  🗺️ System Map
                </button>
              </div>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-950/50' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 3. Research & Knowledge Institute
      if (currentTab === 'research' || currentTab.startsWith('research_') || currentTab === 'knowledge') {
        const items = [
          { key: 'research', label: '🔬 Evidence Hub' },
          { key: 'research_clinical_research', label: '📊 Clinical Trials & Cohorts' },
          { key: 'research_evidence', label: '🧪 HPLC Fingerprints' },
          { key: 'research_knowledge_intelligence', label: '🕸️ Unani Knowledge Graph (ZKB)' },
          { key: 'knowledge', label: '📚 UPI Pharmacopoeia Library' }
        ];
        return `
          <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-8 shadow-lg">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">🔬 Research, Evidence &amp; Knowledge Institute</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">RWE &amp; Multi-Center Trials</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-slate-400 hover:text-emerald-400 transition font-semibold">
                🗺️ System Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-950/50' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 4. Clinical Philosophy & Care Continuum
      if (currentTab === 'philosophy' || currentTab === 'care_journey') {
        const items = [
          { key: 'philosophy', label: '⚖️ Four Humors (Akhlat) & Mizaj' },
          { key: 'care_journey', label: '🔄 12-Step Closed-Loop Care' }
        ];
        return `
          <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-8 shadow-lg">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">📜 Greco-Arab Philosophy &amp; Continuum</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">Mizaj &amp; 12-Stage Care</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-slate-400 hover:text-emerald-400 transition font-semibold">
                🗺️ System Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-950/50' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 5. Hospital Network, Faculty & Patient Governance
      if (currentTab === 'clinics' || currentTab === 'doctors' || currentTab === 'about' || currentTab === 'faqs' || currentTab === 'contact' || currentTab === 'privacy' || currentTab === 'terms') {
        const items = [
          { key: 'clinics', label: '🏥 14 Clinics & Matabs' },
          { key: 'doctors', label: '👨‍⚕️ Medical Faculty' },
          { key: 'about', label: '🏛️ Vision & Founder IP' },
          { key: 'faqs', label: '❓ Patient FAQs' },
          { key: 'contact', label: '📞 Triage & Contact' },
          { key: 'privacy', label: '🔒 Privacy Policy' },
          { key: 'terms', label: '📜 Terms of Service' }
        ];
        return `
          <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-8 shadow-lg">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">🏥 Healthcare Network &amp; Support Hub</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">24/7 Clinical Desk</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-slate-400 hover:text-emerald-400 transition font-semibold">
                🗺️ System Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-950/50' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      return '';
    }
'''

def build_architecture_map_html():
    return '''      // TAB: SYSTEM ARCHITECTURE & INTEGRATED SITEMAP
      if (state.tab === 'pages25') {
        const architectureDomains = [
          {
            title: "Domain I: 🩺 Clinical Services & Care Continuum",
            badge: "Clinical Care",
            desc: "Full-spectrum integrative healthcare services unifying 10-Ajnas pulse telemetry, clinical copilot AI, ambient scribe, and certified manufacturing.",
            modules: [
              { key: "services", title: "Clinical Services Overview", path: "/services", desc: "Tele-consult, OPD, Regimenal Ilaj bil-Tadbeer, and In-Clinic Matab." },
              { key: "services_clinical_care", title: "In-Clinic Matab & OPD Care", path: "/services/clinical-care", desc: "10-Ajnas pulse evaluation, tongue chromametry, and inpatient supervision." },
              { key: "services_ai_healthcare", title: "Hakeem Sahab™ Clinical AI", path: "/services/ai-healthcare", desc: "Multi-hop reasoning with mandatory 21 CFR Part 11 clinician signature barrier." },
              { key: "services_digital_health", title: "Digital Health & Ambient Scribe", path: "/services/digital-health", desc: "Vernacular audio scribe, BLE IoT sensor streaming, and ABDM M1-M3 records." },
              { key: "services_pharmacy", title: "Botanical Dispensary (FEFO)", path: "/services/pharmacy", desc: "Automated FEFO inventory, IoT cold-chain surveillance, and barcoded delivery." },
              { key: "services_manufacturing", title: "Manufacturing OS & eBMR", path: "/services/manufacturing", desc: "Schedule E(1) Mudabbar detoxification, batch records, and HPLC spectral QA." },
              { key: "services_healthcare_communication", title: "Vernacular Posology Audio", path: "/services/healthcare-communication", desc: "Posology voice instructions in Urdu, Hindi, and English with WhatsApp alerts." }
            ]
          },
          {
            title: "Domain II: 🌿 Botanical Therapeutics & Dispensary",
            badge: "Herbal Formulary",
            desc: "AYUSH Schedule T compliant botanical formulations, classical Unani compounds, standardized extracts, and verified cold-chain dispatch protocols.",
            modules: [
              { key: "products", title: "10-Formulation Portfolio", path: "/products", desc: "Interactive herbal catalog with dosage, indications, cart, and batch COA." },
              { key: "products_unani_care", title: "Classical Unani Care", path: "/products/unani-care", desc: "Time-tested compounds: ManiVital Pro, Qurs-e-Taqwiyat-e-Mani, Majun Falasfa." },
              { key: "products_herbal_products", title: "Standardized Herbal Extracts", path: "/products/herbal-products", desc: "Biochemically verified extracts: MetaboCore Elite, LiverPrime Core, GastriNorm." },
              { key: "products_nutraceuticals", title: "Target Phyto-Nutraceuticals", path: "/products/nutraceuticals", desc: "Targeted complexes: NeuroCalmX, NightOne X, and ThyroMet Axis." },
              { key: "shipping_refunds", title: "Cold-Chain Shipping Policy", path: "/shipping-refunds", desc: "2-8°C active thermal packaging, tamper seals, and cold-chain compliance standards." }
            ]
          },
          {
            title: "Domain III: 🔬 Research, Evidence & Knowledge Institute",
            badge: "Empirical Science",
            desc: "Empirical validation of Greco-Arab medicine through multi-center concordance trials, real-world evidence registries, and knowledge graphs.",
            modules: [
              { key: "research", title: "Research & Evidence Hub", path: "/research", desc: "Observational RWE registries, academic concordance, and clinical trial cohorts." },
              { key: "research_clinical_research", title: "Clinical Trials & Cohorts", path: "/research/clinical-research", desc: "Multi-center clinical trials, patient enrollment, and DSMB governance." },
              { key: "research_evidence", title: "Phytochemical HPLC Fingerprints", path: "/research/evidence", desc: "Comparative chromatographic spectra, active marker quantification, and assays." },
              { key: "research_knowledge_intelligence", title: "Unani Knowledge Graph (ZKB)", path: "/research/knowledge-intelligence", desc: "1,280+ canonical botanical monographs, 4,600 affinities, and Badal/Musleh rules." },
              { key: "knowledge", title: "UPI Pharmacopoeia Library", path: "/knowledge", desc: "Standardized single drug monographs and classical Unani pharmacopoeia references." }
            ]
          },
          {
            title: "Domain IV: 📜 Greco-Arab Philosophy & Patient Journey",
            badge: "Clinical Doctrine",
            desc: "Classical foundational doctrine unifying the 4 humors (Akhlat), longitudinal Mizaj constitution, and the 12-stage closed-loop clinical continuum.",
            modules: [
              { key: "philosophy", title: "Four Humors (Akhlat) & Mizaj", path: "/philosophy", desc: "Damm, Balgham, Safra, and Sawda balance, 6 Essentials, and Afaal progression." },
              { key: "care_journey", title: "12-Step Clinical Continuum", path: "/care-journey", desc: "From KNOW & ASSESS through 21 CFR Lock, IoT tracking, and Relapse Guard." }
            ]
          },
          {
            title: "Domain V: 🏥 Healthcare Network, Faculty & Governance",
            badge: "Hospital & Governance",
            desc: "Accredited clinical facilities, board-certified senior clinicians, intellectual property stewardship, and statutory patient data protection.",
            modules: [
              { key: "clinics", title: "14 Hospital & Matab Network", path: "/clinics", desc: "Flagship hospital in New Delhi and specialized Matabs across major cities." },
              { key: "doctors", title: "Board-Certified Faculty & Clinicians", path: "/doctors", desc: "Senior Tabeebs and integrative MDs with verified institutional credentials." },
              { key: "about", title: "About ZAYVORA & Founder IP", path: "/about", desc: "Institutional vision, governance board, and Hakeem Dr. Irfan Ashraf IP stewardship." },
              { key: "faqs", title: "Patient & Clinical FAQs", path: "/faq", desc: "Answers regarding treatment safety, consultation booking, and ABHA integration." },
              { key: "contact", title: "24/7 Helpline & Emergency Triage", path: "/contact", desc: "Universal triage line +91 97738 82657, casualty desk, and direct messaging." },
              { key: "privacy", title: "Data Protection & Privacy Policy", path: "/privacy-policy", desc: "HIPAA, ABDM M1-M3, and DPDP cryptographic health data protection standards." },
              { key: "terms", title: "Terms of Clinical Service", path: "/terms-and-conditions", desc: "21 CFR Part 11 digital records, telemedicine guidelines, and clinical disclaimers." }
            ]
          }
        ];

        container.innerHTML = `
          <div class="space-y-10 pb-16">
            
            <!-- Architecture Blueprint Header -->
            <div class="bg-gradient-to-r from-[#0F172A] via-[#131D31] to-[#0A0F1D] p-8 rounded-3xl border border-emerald-500/30 space-y-4 shadow-xl">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">ZAYVORA Health OS™ Architecture</span>
                  </div>
                  <h1 class="text-2xl md:text-3xl font-extrabold text-white mt-1">Interactive System Architecture Map</h1>
                  <p class="text-xs md:text-sm text-slate-300 mt-1.5 max-w-3xl leading-relaxed">
                    Unified architectural blueprint organizing all 25 canonical pages into 5 interconnected clinical, botanical, research, and governance domains.
                  </p>
                </div>
                <button onclick="viewWebsitePage('home')" class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition shrink-0 flex items-center gap-2">
                  <span>←</span> Back to Flagship Home
                </button>
              </div>
            </div>

            <!-- Domain Sections -->
            <div class="space-y-10">
              ${architectureDomains.map((dom, domIdx) => `
                <div class="bg-[var(--card)] p-6 md:p-8 rounded-3xl border border-[var(--border)] space-y-5">
                  <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 pb-4 border-b border-slate-800">
                    <div>
                      <h2 class="text-lg md:text-xl font-bold text-white">${dom.title}</h2>
                      <p class="text-xs text-[var(--muted)] mt-1">${dom.desc}</p>
                    </div>
                    <span class="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-mono text-xs font-bold border border-emerald-500/20 shrink-0">
                      ${dom.modules.length} Connected Modules
                    </span>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    ${dom.modules.map(m => `
                      <div class="p-4 rounded-2xl bg-[#0F172A]/80 border border-slate-800 hover:border-emerald-500/50 transition-all flex flex-col justify-between space-y-3 group">
                        <div>
                          <div class="flex justify-between items-start gap-2 mb-1.5">
                            <span class="font-bold text-white text-xs group-hover:text-emerald-300 transition-colors">${m.title}</span>
                            <span class="text-[9px] text-emerald-400 font-mono bg-emerald-500/10 px-1.5 py-0.5 rounded shrink-0">${m.path}</span>
                          </div>
                          <p class="text-[11px] text-slate-300 leading-relaxed">${m.desc}</p>
                        </div>
                        <div class="pt-2 border-t border-slate-800 flex justify-between items-center text-[11px]">
                          <span class="text-emerald-400 font-medium flex items-center gap-1">
                            <span>●</span> Active Module
                          </span>
                          <button onclick="viewWebsitePage('${m.key}')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs transition">
                            Explore Module &rarr;
                          </button>
                        </div>
                      </div>
                    `).join('')}
                  </div>
                </div>
              `).join('')}
            </div>

          </div>
        `;
        return;
      }'''

def upgrade_codebase(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Insert getWebsiteHubSubnav function before renderWebsiteApp
    if "function getWebsiteHubSubnav(" not in text:
        idx = text.find("function renderWebsiteApp(container) {")
        if idx != -1:
            subnav_js = generate_subnav_js() + "\n    "
            text = text[:idx] + subnav_js + text[idx:]
            print(f"Inserted getWebsiteHubSubnav into {file_path}")

    # 2. Update roleNavs website tabs label for pages25
    text = text.replace("{ id: 'pages25', label: '📑 All 25 Pages Directory' }",
                        "{ id: 'pages25', label: '🗺️ System Architecture' }")
    text = text.replace("{ id: 'pages25', label: '📑 All 25 Pages' }",
                        "{ id: 'pages25', label: '🗺️ System Architecture' }")

    # 3. Replace the old pages25 render block with the new architecture map
    pattern_pages25 = r"// TAB: 25 CANONICAL PAGES DIRECTORY.*?return;\s*\}"
    m = re.search(pattern_pages25, text, re.DOTALL)
    if m:
        new_arch_html = build_architecture_map_html()
        text = text[:m.start()] + new_arch_html + text[m.end():]
        print(f"Replaced pages25 render block with Architecture Map in {file_path}")
    else:
        print(f"Could not match pages25 pattern in {file_path}")

    # 4. Integrate getWebsiteHubSubnav into services, products, research, philosophy, clinics, doctors, about, faqs, contact
    # In services view:
    text = text.replace("if (state.tab === 'services') {\n        const servicesList =",
                        "if (state.tab === 'services') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        const servicesList =")
    text = text.replace("<div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "<div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In services_* subpage view:
    old_sub_services = """      if (state.tab.startsWith('services_')) {
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
            </div>"""

    new_sub_services = """      if (state.tab.startsWith('services_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Clinical Service Detail", desc: "Advanced healthcare module" };
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('services')" class="text-xs text-emerald-400 font-bold hover:underline">← Clinical Services Hub</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex gap-2">
                  <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { switchRole('clinic'); }" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">Book Consultation</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">🗺️ System Map</button>
                </div>
              </div>
            </div>"""
    text = text.replace(old_sub_services, new_sub_services)

    # In products view:
    text = text.replace("if (state.tab === 'products') {\n        container.innerHTML = `\n          <div class=\"max-w-6xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'products') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-6xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In products_* subpage view:
    old_sub_products = """      if (state.tab.startsWith('products_')) {
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
            </div>"""

    new_sub_products = """      if (state.tab.startsWith('products_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Product Category", desc: "ZAYVORA Herbals Portfolio" };
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('products')" class="text-xs text-emerald-400 font-bold hover:underline">← Botanical Formulations Hub</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="viewWebsitePage('products')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">View All 10 Formulations</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">🗺️ System Map</button>
                </div>
              </div>
            </div>"""
    text = text.replace(old_sub_products, new_sub_products)

    # In research view:
    text = text.replace("if (state.tab === 'research') {\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'research') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In research_* subpage view:
    old_sub_research = """      if (state.tab.startsWith('research_')) {
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
            </div>"""

    new_sub_research = """      if (state.tab.startsWith('research_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Research Program", desc: "ZAYVORA Clinical Evidence" };
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('research')" class="text-xs text-emerald-400 font-bold hover:underline">← Research &amp; Evidence Hub</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="viewWebsitePage('research')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">Evidence Overview</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">🗺️ System Map</button>
                </div>
              </div>
            </div>"""
    text = text.replace(old_sub_research, new_sub_research)

    # In philosophy view:
    text = text.replace("if (state.tab === 'philosophy') {\n        container.innerHTML = `\n          <div class=\"max-w-4xl mx-auto space-y-6 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'philosophy') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-4xl mx-auto space-y-6 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In care_journey view:
    text = text.replace("if (state.tab === 'care_journey') {\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'care_journey') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In clinics view:
    text = text.replace("if (state.tab === 'clinics') {\n        const clinicsList =",
                        "if (state.tab === 'clinics') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        const clinicsList =")
    text = text.replace("if (state.tab === 'clinics') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        const clinicsList = [\n          { name: \"ZAYVORA Healthcare System - Central Hospital\"",
                        "if (state.tab === 'clinics') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        const clinicsList = [\n          { name: \"ZAYVORA Healthcare System - Central Hospital\"")

    text = text.replace("<div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3\">\n              <div class=\"flex justify-between items-center\">\n                <span class=\"text-xs font-bold text-emerald-400 uppercase tracking-wider\">Facility Directory</span>",
                        "<div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3\">\n              <div class=\"flex justify-between items-center\">\n                <span class=\"text-xs font-bold text-emerald-400 uppercase tracking-wider\">Facility Directory</span>")

    # In doctors view:
    text = text.replace("if (state.tab === 'doctors') {\n        const doctorsList =",
                        "if (state.tab === 'doctors') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        const doctorsList =")
    text = text.replace("<div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3\">\n              <div class=\"flex justify-between items-center\">\n                <span class=\"text-xs font-bold text-emerald-400 uppercase tracking-wider\">Medical Faculty</span>",
                        "<div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3\">\n              <div class=\"flex justify-between items-center\">\n                <span class=\"text-xs font-bold text-emerald-400 uppercase tracking-wider\">Medical Faculty</span>")

    # In about view:
    text = text.replace("if (state.tab === 'about') {\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'about') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In faqs view:
    text = text.replace("if (state.tab === 'faqs') {\n        const faqs =",
                        "if (state.tab === 'faqs') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        const faqs =")
    text = text.replace("<div class=\"max-w-4xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3\">\n              <div class=\"flex justify-between items-center\">\n                <span class=\"text-xs font-bold text-emerald-400 uppercase tracking-wider\">Patient Questions</span>",
                        "<div class=\"max-w-4xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3\">\n              <div class=\"flex justify-between items-center\">\n                <span class=\"text-xs font-bold text-emerald-400 uppercase tracking-wider\">Patient Questions</span>")

    # In contact view:
    text = text.replace("if (state.tab === 'contact') {\n        container.innerHTML = `\n          <div class=\"max-w-4xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'contact') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-4xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In knowledge view:
    text = text.replace("if (state.tab === 'knowledge') {\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl",
                        "if (state.tab === 'knowledge') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"max-w-5xl mx-auto space-y-8 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-8 rounded-3xl")

    # In shipping_refunds view:
    text = text.replace("if (state.tab === 'shipping_refunds') {\n        container.innerHTML = `\n          <div class=\"space-y-6 pb-12\">\n            <div class=\"bg-[var(--card)] p-6 rounded-2xl",
                        "if (state.tab === 'shipping_refunds') {\n        const subnav = getWebsiteHubSubnav(state.tab);\n        container.innerHTML = `\n          <div class=\"space-y-6 pb-12\">\n            ${subnav}\n            <div class=\"bg-[var(--card)] p-6 rounded-2xl")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Successfully integrated public pages into {file_path}")

if __name__ == "__main__":
    for fp in ["index.html", "docs/index.html"]:
        upgrade_codebase(fp)
