import re

def build_upgraded_header():
    return '''  <!-- ===================================================================== -->
  <!-- TOP PLATFORM APPLICATION BAR (EXECUTIVE & CLINICAL RUNTIME) -->
  <!-- ===================================================================== -->
  <header class="backdrop-blur-md bg-[#0F172A]/95 border-b border-emerald-500/20 px-4 md:px-8 py-3 sticky top-0 z-50 shadow-xl transition-all">
    <div class="max-w-7xl mx-auto flex flex-col lg:flex-row justify-between items-start lg:items-center gap-3">
      
      <!-- Facility & Product Brand with Executive IP Attribution -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-[#0A0F1D] border border-emerald-500/40 flex items-center justify-center p-1 shadow-md overflow-hidden shrink-0">
          <img src="zayvora-logo.png" alt="ZAYVORA" class="w-full h-full object-contain" onerror="this.onerror=null; this.src='/zayvora-logo.png';" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-extrabold tracking-tight text-lg text-white">ZAYVORA Health OS™</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
              Enterprise Clinical OS v5.0
            </span>
          </div>
          <p class="text-[11px] text-slate-300 flex items-center gap-1.5">
            <span>🏥 ZAYVORA Healthcare System</span>
            <span class="text-slate-600">&bull;</span>
            <span class="text-emerald-400 font-medium">Hakeem Dr. Irfan Ashraf (Founder &amp; Chief Architect)</span>
          </p>
        </div>
      </div>

      <!-- Center / Fast Navigation Quicklinks -->
      <div class="hidden xl:flex items-center gap-1 text-xs font-semibold text-slate-300 bg-[#1E293B]/60 p-1 rounded-xl border border-slate-800">
        <button onclick="viewWebsitePage('home')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">🏠 Home</button>
        <button onclick="viewWebsitePage('services')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">🩺 Services</button>
        <button onclick="viewWebsitePage('products')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">🌿 Products</button>
        <button onclick="viewWebsitePage('research')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">🔬 Research</button>
        <button onclick="viewWebsitePage('philosophy')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">📜 Philosophy</button>
        <button onclick="viewWebsitePage('clinics')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">🏥 Clinics</button>
        <button onclick="viewWebsitePage('doctors')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">👨‍⚕️ Doctors</button>
        <button onclick="viewWebsitePage('contact')" class="px-2.5 py-1 rounded-lg hover:text-white hover:bg-[#0F172A] transition">📞 Contact</button>
      </div>

      <!-- Persona Switcher, Actions & Real-Time Telemetry Badges -->
      <div class="flex flex-wrap items-center gap-2.5 w-full lg:w-auto justify-between lg:justify-end">
        
        <!-- Grouped Persona Selector -->
        <div class="flex items-center gap-2 bg-[#0A0F1D] px-3 py-1.5 rounded-xl border border-slate-800 focus-within:border-emerald-500/50 transition">
          <span class="text-[11px] text-slate-400 font-medium hidden sm:inline">Role:</span>
          <select id="role-selector" onchange="switchRole(this.value)" class="bg-transparent text-xs font-semibold text-emerald-400 focus:outline-none cursor-pointer max-w-[210px] sm:max-w-xs truncate">
            <optgroup label="🌐 Public Website &amp; Portals" class="bg-[#0F172A] text-slate-300 font-bold">
              <option value="website" selected>🌐 ZAYVORA Health™ Public Website</option>
              <option value="herbals">🌿 ZAYVORA Herbals (10-Product Store)</option>
              <option value="mobile">📱 ZAYVORA Mobile App Simulator</option>
            </optgroup>
            <optgroup label="🩺 Clinical Practice Cockpits" class="bg-[#0F172A] text-slate-300 font-bold">
              <option value="doctor">🩺 Hakeem Dr. Irfan Ashraf (Chief Clinician &amp; Architect)</option>
              <option value="patient">👤 Hamza Farooqi (Patient Health 360 &amp; Regimen)</option>
              <option value="clinic">🏥 Sana Khan (Clinic Reception &amp; OPD Queue)</option>
            </optgroup>
            <optgroup label="💊 Pharmacy, Manufacturing &amp; Lab" class="bg-[#0F172A] text-slate-300 font-bold">
              <option value="pharmacy">💊 Zainab Ali (Clinical Pharmacist &amp; FEFO)</option>
              <option value="manufacturing">🏭 Dr. Arshad Qureshi (Manufacturing QA/QC &amp; BMR)</option>
              <option value="hardware">🔬 Clinical Hardware &amp; IoT Telemetry Lab</option>
            </optgroup>
            <optgroup label="🏢 Governance, Research &amp; Administration" class="bg-[#0F172A] text-slate-300 font-bold">
              <option value="enterprise">🏢 Hakeem Dr. Irfan Ashraf (Founder, Chairman &amp; IP Owner)</option>
              <option value="research">🔬 Dr. K. Saxena (Clinical Researcher &amp; RWE)</option>
              <option value="admin">🛡️ Platform Administrator (System Admin &amp; IT)</option>
            </optgroup>
          </select>
        </div>

        <!-- Fast OPD Booking CTA Button -->
        <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { switchRole('clinic'); }" class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-md shadow-emerald-950/40 transition">
          <span>🎫</span> <span class="hidden md:inline">OPD Token</span>
        </button>

        <div class="flex items-center gap-1.5">
          <!-- Help Modal Trigger -->
          <button onclick="toggleHelpModal()" class="px-2.5 py-1.5 rounded-xl border border-slate-800 text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition" title="Clinical Guidance &amp; Safety Guidelines">
            Help
          </button>

          <!-- Search Command Trigger (⌘K) -->
          <button onclick="toggleSearchModal()" class="px-2.5 py-1.5 rounded-xl bg-[#0A0F1D] border border-slate-800 text-xs text-slate-300 hover:border-emerald-400 flex items-center gap-1.5 transition" title="Search Patients, Rx, Protocols (⌘K)">
            <span>🔍</span> <kbd class="px-1 py-0.5 rounded bg-[#1E293B] text-[9px] font-mono text-emerald-400">⌘K</kbd>
          </button>

          <!-- Notification Bell Trigger -->
          <button onclick="toggleNotificationsModal()" class="relative p-1.5 rounded-xl bg-[#0A0F1D] border border-slate-800 text-xs hover:border-emerald-400 transition" title="System Alerts &amp; Clinical Notifications">
            🔔<span id="header-notif-badge" class="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-rose-500 text-white font-bold text-[8px] flex items-center justify-center">3</span>
          </button>

          <!-- Language Selector -->
          <div class="flex items-center bg-[#0A0F1D] rounded-xl border border-slate-800 p-0.5 text-[10px] font-bold">
            <button id="lang-btn-en" onclick="switchLanguage('en')" class="px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-300">EN</button>
            <button id="lang-btn-hi" onclick="switchLanguage('hi')" class="px-2 py-0.5 rounded-lg text-slate-400 hover:text-white">HI</button>
            <button id="lang-btn-ur" onclick="switchLanguage('ur')" class="px-2 py-0.5 rounded-lg text-slate-400 hover:text-white">UR</button>
          </div>

          <!-- Live DB Health Status Badge -->
          <div id="live-db-badge" class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-950/80 text-emerald-300 border border-emerald-500/40 shrink-0" title="Connected to zayvora_live.db SQLite Relational Store">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span id="live-db-text">LIVE REST API</span>
          </div>
        </div>

      </div>

    </div>
  </header>'''

def build_upgraded_footer():
    return '''  <!-- ===================================================================== -->
  <!-- WORLD-CLASS ENTERPRISE HEALTHCARE FOOTER (25 PAGES ARCHITECTURE) -->
  <!-- ===================================================================== -->
  <footer class="w-full border-t border-slate-800 bg-[#0B1120] text-xs text-slate-400 pt-16 pb-12 px-4 md:px-8 mt-auto">
    <div class="max-w-7xl mx-auto space-y-12">
      
      <!-- Top Brand & Executive IP Showcase -->
      <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 pb-8 border-b border-slate-800/80">
        <div class="space-y-2 max-w-2xl">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-slate-900 border border-emerald-500/30 flex items-center justify-center p-1.5 shadow-md">
              <img src="zayvora-logo.png" alt="ZAYVORA" class="w-full h-full object-contain" onerror="this.onerror=null; this.src='/zayvora-logo.png';" />
            </div>
            <div>
              <span class="font-extrabold tracking-tight text-xl text-white">ZAYVORA Health OS™</span>
              <span class="ml-2 text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                Enterprise Clinical OS v5.0
              </span>
            </div>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Codified Greco-Arab (Unani) clinical science unified with multi-omics diagnostic precision, 
            longitudinal Mizaj profiling, and fail-closed 21 CFR Part 11 clinician governance.
          </p>
          <div class="text-[11px] text-emerald-400/90 font-medium">
            🛡️ Sole Proprietary Intellectual Property of <strong class="text-white">Hakeem Dr. Irfan Ashraf</strong> (Founder, Chairman &amp; Principal Healthcare Architect).
          </div>
        </div>

        <!-- 24/7 Clinical Concierge & Emergency Desk -->
        <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2 min-w-[280px]">
          <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">24/7 Clinical Concierge &amp; Triage</span>
          <div class="text-white font-mono font-bold text-sm flex items-center gap-2">
            <span>📞</span> +91 97738 82657
          </div>
          <div class="text-[11px] text-slate-400">Universal Matab &amp; Emergency Hospital Line</div>
          <div class="pt-1 flex gap-2">
            <button onclick="viewWebsitePage('contact')" class="px-3 py-1.5 bg-emerald-600/30 hover:bg-emerald-600 text-emerald-300 hover:text-white font-semibold text-[11px] rounded-lg border border-emerald-500/30 transition">
              Online Triage Desk &rarr;
            </button>
            <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { switchRole('clinic'); }" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-semibold text-[11px] rounded-lg transition">
              Book OPD Token
            </button>
          </div>
        </div>
      </div>

      <!-- 25 Canonical Pages Organized under 5 Semantic Column Headings -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8 text-xs">
        
        <!-- Column 1: Clinical Services & Care -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800 pb-2">
            <span class="text-emerald-400">🩺</span> Clinical Services
          </h4>
          <ul class="space-y-2 text-[11px]">
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_clinical_care')" class="hover:text-emerald-400 transition-colors block">In-Clinic Matab &amp; OPD Care</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_ai_healthcare')" class="hover:text-emerald-400 transition-colors block">Hakeem Sahab™ Clinical AI</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_digital_health')" class="hover:text-emerald-400 transition-colors block">Digital Health &amp; Tele-Consult</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_pharmacy')" class="hover:text-emerald-400 transition-colors block">Botanical Dispensary (FEFO)</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_manufacturing')" class="hover:text-emerald-400 transition-colors block">Manufacturing OS &amp; eBMR</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_healthcare_communication')" class="hover:text-emerald-400 transition-colors block">Vernacular Posology Audio</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('services')" class="text-emerald-400 font-semibold hover:underline block pt-1">All Clinical Services &rarr;</a></li>
          </ul>
        </div>

        <!-- Column 2: Botanical Formulations -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800 pb-2">
            <span class="text-emerald-400">🌿</span> Botanical Formulations
          </h4>
          <ul class="space-y-2 text-[11px]">
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('products_unani_care')" class="hover:text-emerald-400 transition-colors block">Classical Unani Compounds</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('products_herbal_products')" class="hover:text-emerald-400 transition-colors block">Standardized Herbal Extracts</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('products_nutraceuticals')" class="hover:text-emerald-400 transition-colors block">Target Phyto-Nutraceuticals</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('pharmacy'); switchTab('detox');" class="hover:text-emerald-400 transition-colors block">Schedule E(1) Mudabbar Detox</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('herbals'); switchTab('cart');" class="hover:text-emerald-400 transition-colors block">Dispensary Cart &amp; Checkout</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('herbals'); switchTab('monographs');" class="hover:text-emerald-400 transition-colors block">Batch Certificates (COA)</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('products')" class="text-emerald-400 font-semibold hover:underline block pt-1">Explore 10-Product Store &rarr;</a></li>
          </ul>
        </div>

        <!-- Column 3: Research & Evidence -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800 pb-2">
            <span class="text-emerald-400">🔬</span> Research &amp; Evidence
          </h4>
          <ul class="space-y-2 text-[11px]">
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('research')" class="hover:text-emerald-400 transition-colors block">Research &amp; Evidence Hub</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('research_clinical_research')" class="hover:text-emerald-400 transition-colors block">Clinical Trials &amp; Cohorts</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('research_evidence')" class="hover:text-emerald-400 transition-colors block">Phytochemical HPLC Fingerprints</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('research_knowledge_intelligence')" class="hover:text-emerald-400 transition-colors block">Unani Knowledge Graph (ZKB)</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('research'); switchTab('outcomes');" class="hover:text-emerald-400 transition-colors block">Validated PROMs (WOMAC/VAS)</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('research'); switchTab('adverse');" class="hover:text-emerald-400 transition-colors block">Pharmacovigilance Registry</a></li>
          </ul>
        </div>

        <!-- Column 4: Philosophy & Governance -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800 pb-2">
            <span class="text-emerald-400">📜</span> Philosophy &amp; Doctrine
          </h4>
          <ul class="space-y-2 text-[11px]">
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('philosophy')" class="hover:text-emerald-400 transition-colors block">Four Humors &amp; Temperaments</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('care_journey')" class="hover:text-emerald-400 transition-colors block">12-Step Clinical Continuum</a></li>
            <li><a href="javascript:void(0)" onclick="if (document.getElementById('mizaj-assessment-section')) document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' }); else viewWebsitePage('philosophy');" class="hover:text-emerald-400 transition-colors block">60-Second Mizaj Assessment</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('enterprise'); switchTab('overview');" class="hover:text-emerald-400 transition-colors block">Founder &amp; IP Governance</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('about')" class="hover:text-emerald-400 transition-colors block">Institutional Quorum Board</a></li>
            <li><a href="javascript:void(0)" onclick="switchRole('doctor'); switchTab('tadbeer');" class="hover:text-emerald-400 transition-colors block">16 Modalities (Tadbeer)</a></li>
          </ul>
        </div>

        <!-- Column 5: Network, Doctors & Support -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800 pb-2">
            <span class="text-emerald-400">🏥</span> Clinics &amp; Support
          </h4>
          <ul class="space-y-2 text-[11px]">
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('clinics')" class="hover:text-emerald-400 transition-colors block">14 Clinics &amp; Matab Network</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('doctors')" class="hover:text-emerald-400 transition-colors block">Board-Certified Clinicians</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('knowledge')" class="hover:text-emerald-400 transition-colors block">UPI Monographs Library</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('faqs')" class="hover:text-emerald-400 transition-colors block">Patient &amp; Clinical FAQs</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('contact')" class="hover:text-emerald-400 transition-colors block">Emergency Care &amp; Admissions</a></li>
            <li><a href="javascript:void(0)" onclick="viewWebsitePage('pages25')" class="text-teal-300 font-semibold hover:underline block pt-1">All 25 Canonical Pages &rarr;</a></li>
          </ul>
        </div>

      </div>

      <!-- Regulatory Accreditations & Statutory Compliance Bar -->
      <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-wrap items-center justify-between gap-4 text-[11px]">
        <div class="flex flex-wrap items-center gap-4 text-slate-300">
          <span class="flex items-center gap-1.5"><span class="text-emerald-400">🔒</span> <strong>21 CFR Part 11:</strong> Digital Signatures &amp; Merkle Audit Ledger</span>
          <span class="text-slate-600 hidden sm:inline">&bull;</span>
          <span class="flex items-center gap-1.5"><span class="text-emerald-400">🛡️</span> <strong>ABDM M1-M3:</strong> Ayushman Bharat &amp; FHIR R4 Compliant</span>
          <span class="text-slate-600 hidden sm:inline">&bull;</span>
          <span class="flex items-center gap-1.5"><span class="text-emerald-400">📜</span> <strong>Statutory:</strong> Ministry of AYUSH &amp; NCISM Clinical Standards</span>
          <span class="text-slate-600 hidden sm:inline">&bull;</span>
          <span class="flex items-center gap-1.5"><span class="text-emerald-400">🌿</span> <strong>Schedule E(1):</strong> Verified Mudabbar Non-Toxicity</span>
        </div>
        <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-[10px] font-mono">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>45 CLINICAL ENGINES OPERATIONAL &bull; 100% UPTIME</span>
        </div>
      </div>

      <!-- Bottom Copyright & Legal Links -->
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-800 text-[11px] text-slate-500">
        <div>
          &copy; 2026 ZAYVORA Health OS™. All Rights Reserved. Proprietary Intellectual Property of <strong class="text-slate-300">Hakeem Dr. Irfan Ashraf</strong>.
        </div>
        <div class="flex flex-wrap items-center gap-4 text-slate-400">
          <a href="javascript:void(0)" onclick="viewWebsitePage('privacy')" class="hover:text-white transition-colors">Privacy Policy</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('terms')" class="hover:text-white transition-colors">Terms of Clinical Service</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="viewWebsitePage('shipping_refunds')" class="hover:text-white transition-colors">Cold-Chain Dispatch Policy</a>
          <span>&bull;</span>
          <a href="javascript:void(0)" onclick="showNotification('100% HIPAA, DPDP &amp; DISHA Compliant Healthcare System.', 'info')" class="hover:text-white transition-colors">Data Security</a>
          <span>&bull;</span>
          <span class="text-emerald-400/80 font-medium">WCAG 2.1 AA Certified</span>
        </div>
      </div>

    </div>
  </footer>'''

def upgrade_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Upgrade Header
    idx_hdr_start = text.find('<header')
    idx_hdr_end = text.find('</header>') + len('</header>')
    if idx_hdr_start == -1 or idx_hdr_end == -1:
        print(f"Could not find header in {filepath}")
        return False

    new_header = build_upgraded_header()
    text = text[:idx_hdr_start] + new_header + text[idx_hdr_end:]

    # 2. Upgrade Footer
    idx_ftr_start = text.find('<footer')
    idx_ftr_end = text.find('</footer>') + len('</footer>')
    if idx_ftr_start == -1 or idx_ftr_end == -1:
        print(f"Could not find footer in {filepath}")
        return False

    new_footer = build_upgraded_footer()
    text = text[:idx_ftr_start] + new_footer + text[idx_ftr_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Successfully upgraded header and footer in {filepath}")
    return True

for p in ['index.html', 'docs/index.html']:
    upgrade_file(p)
