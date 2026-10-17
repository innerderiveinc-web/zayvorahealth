    // ===== THEME MANAGEMENT =====
    function updateThemeSwitcherUI(currentTheme) {
      const darkBtn = document.getElementById('theme-btn-dark');
      const lightBtn = document.getElementById('theme-btn-light');
      const container = document.getElementById('theme-pill-container');
      if (!darkBtn || !lightBtn) return;
      if (currentTheme === 'light') {
        lightBtn.className = 'px-2.5 py-1 rounded-lg bg-[#165B44] text-white font-bold flex items-center gap-1 shadow-sm transition-all cursor-pointer';
        darkBtn.className = 'px-2.5 py-1 rounded-lg text-[#5F707E] hover:text-[#1B242A] flex items-center gap-1 transition-all cursor-pointer';
        if (container) container.className = 'flex items-center bg-[#E4DDCF] rounded-xl border border-[#D0C8B7] p-0.5 text-[11px] font-bold shadow-inner';
      } else {
        darkBtn.className = 'px-2.5 py-1 rounded-lg bg-slate-800 text-emerald-300 font-bold flex items-center gap-1 shadow-sm transition-all cursor-pointer';
        lightBtn.className = 'px-2.5 py-1 rounded-lg text-slate-400 hover:text-white flex items-center gap-1 transition-all cursor-pointer';
        if (container) container.className = 'flex items-center bg-[#0B0F17] rounded-xl border border-slate-800 p-0.5 text-[11px] font-bold shadow-sm';
      }
    }

    function setAppTheme(theme, save = true) {
      const mode = (theme === 'dark') ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', mode);
      if (save) {
        try {
          localStorage.setItem('zayvora-theme-v2', mode);
          localStorage.setItem('zayvora-theme', mode);
        } catch (e) {}
      }
      const metaTheme = document.querySelector('meta[name="theme-color"]');
      if (metaTheme) metaTheme.setAttribute('content', mode === 'light' ? '#faf8f5' : '#0B1120');
      updateThemeSwitcherUI(mode);
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setAppTheme(next, true);
    }

    (function initializeTheme() {
      // 1. Check URL query params (?theme=light or ?theme=dark)
      let detectedTheme = null;
      try {
        const urlParams = new URLSearchParams(window.location.search);
        detectedTheme = urlParams.get('theme');
        if (!detectedTheme && window.location.hash) {
          if (window.location.hash.toLowerCase().includes('dark')) detectedTheme = 'dark';
          if (window.location.hash.toLowerCase().includes('light')) detectedTheme = 'light';
        }
      } catch (e) {}

      // 2. Fall back to zayvora-theme-v2, defaulting to 'light'
      const activeTheme = detectedTheme || localStorage.getItem('zayvora-theme-v2') || 'light';
      setAppTheme(activeTheme, true);

      // 3. Purge all legacy service worker caches to prevent stale view
      if ('caches' in window) {
        caches.keys().then(keys => {
          keys.forEach(k => {
            caches.delete(k);
          });
        }).catch(() => {});
      }

      // Ensure switcher UI reflects state after DOM loads
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => updateThemeSwitcherUI(activeTheme));
      } else {
        updateThemeSwitcherUI(activeTheme);
      }
    })();

    // ===== STATE STORE =====
    const state = {
      lang: 'en',
      unreadAlerts: 3,
      alerts: [
        { id: 'ALT-1', level: 'CRITICAL', title: 'Azaraqi (Mudabbar) + CNS Sedative Warning', desc: 'Patient Hamza Farooqi: Must not co-administer without 6h spacing and Kateera corrective.', acknowledged: false },
        { id: 'ALT-2', level: 'LAB', title: 'Elevated Fasting Blood Glucose (118 mg/dL)', desc: 'Patient Hamza Farooqi: Su-e-Mizaj Barid Balghami correlation noted. Dietary parhez issued.', acknowledged: false },
        { id: 'ALT-3', level: 'INVENTORY', title: 'Batch Expiring in 60 Days: Majun Suranjan', desc: 'Dispensary Batch BATCH-MS-2026-0441 has 142 units remaining. Prioritize FEFO dispatch.', acknowledged: false }
      ],
      encounterId: 'ENC-2026-0814',
      afaalStage: 'TANQIYA',
      afaalDays: 7,
      hakeemDrawerOpen: false,
      role: 'website',
      tab: 'home',
      patient: {
        id: 'PAT-774901',
        mrn: 'MRN-2026-0814',
        name: 'Hamza Farooqi',
        age: 44,
        gender: 'Male',
        phone: '+91-9876543210',
        email: 'hamza.farooqi@example.com',
        allergies: 'Sonf (Foeniculum vulgare)',
        mizaj: 'Su-e-Mizaj Barid Balghami (Cold-Phlegmatic)',
        primaryComplaint: 'Bilateral knee pain and morning stiffness for 3 weeks',
        nextAppointment: { time: 'Today, 10:30 AM', doctor: 'Hakeem Dr. Irfan Ashraf', facility: 'ZAYVORA Healthcare System - Central Hospital' }
      },
      appointments: [
        {
          id: 'APT-104',
          token: 'T-104',
          patientName: 'Hamza Farooqi',
          mrn: 'MRN-2026-0814',
          doctorName: 'Hakeem Dr. Irfan Ashraf',
          scheduledTime: 'Today, 10:30 AM',
          type: 'Integrative Outpatient Consultation',
          complaint: 'Bilateral knee joint stiffness and cold weather discomfort',
          status: 'Waiting in Room 204'
        },
        {
          id: 'APT-105',
          token: 'T-105',
          patientName: 'Ayesha Siddiqui',
          mrn: 'MRN-2026-0819',
          doctorName: 'Hakeem Dr. Irfan Ashraf',
          scheduledTime: 'Today, 11:15 AM',
          type: 'Follow-up Evaluation',
          complaint: 'Chronic dyspepsia and post-prandial heaviness',
          status: 'Confirmed'
        }
      ],
      prescriptions: [
        {
          id: 'RX-2026-0441',
          patientName: 'Hamza Farooqi',
          mrn: 'MRN-2026-0814',
          date: 'September 12, 2026',
          prescriber: 'Hakeem Dr. Irfan Ashraf',
          signature: 'SHA-256: 8a4c10... SEALED (21 CFR Part 11)',
          diagnosis: 'Waja-ul-Mafasil Barid Balghami (Knee Osteoarthritis)',
          medicines: [
            { name: 'Majun Suranjan', form: 'Majun (Electuary)', strength: '5g', frequency: 'Twice daily', anupan: 'Lukewarm cow milk', duration: '21 Days', track: 'QARABADEEN', axis: 'Musculoskeletal', ingredients: 'Suranjan Talkh Mudabbar, Kateera, Zanjabeel' },
            { name: 'Raughan-e-Balsan', form: 'Raughan (Medicated Oil)', strength: '10ml', frequency: 'Bedtime', anupan: 'Local fomentation', duration: '30 Days', track: 'QARABADEEN', axis: 'Musculoskeletal', ingredients: 'Commiphora gileadensis resin oil' }
          ],
          medications: [
            { name: 'Majun Suranjan', dose: '5g twice daily after meals with warm water', role: 'Primary Anti-inflammatory', note: 'Mudabbar Detoxified (Schedule E1)' },
            { name: 'Raughan-e-Balsan', dose: 'Gentle local application on both knees at bedtime', role: 'Local Analgesic Fomentation', note: 'Ilaj bil-Tadbeer Regimen' }
          ],
          dietaryAdvice: 'Avoid curd, chilled drinks, and flatulent legumes. Drink warm ginger infusion.',
          status: 'Draft - Awaiting Clinician Signature',
          locked: false
        }
      ],
      inventory: [
        { name: 'Majun Suranjan (Mudabbar)', batch: 'BATCH-MS-2026-0441', exp: '2028-01-09', stock: 142, status: 'Clinic Unani (Schedule E1)', category: 'CLINIC_UNANI', e1: true },
        { name: 'Raughan-e-Balsan', batch: 'BATCH-RB-2026-0209', exp: '2029-02-14', stock: 88, status: 'Retail Classical Unani', category: 'RETAIL_UNANI', e1: false },
        { name: 'Hab-e-Suranjan Forte', batch: 'BATCH-HS-2026-0312', exp: '2027-08-31', stock: 210, status: 'Clinic Unani (Schedule E1)', category: 'CLINIC_UNANI', e1: true },
        { name: 'MetaboCore Elite Powder', batch: 'BATCH-MCE-2026-101', exp: '2028-06-20', stock: 320, status: 'AYUSH Proprietary Formulation', category: 'AYUSH_PROPRIETARY', e1: false },
        { name: 'RestoreVital Herbal Infusion', batch: 'BATCH-RVH-2026-055', exp: '2028-11-15', stock: 450, status: 'FSSAI Dietary Supplement', category: 'FSSAI_SUPPLEMENT', e1: false }
      ],
      users: [
        { id: 'USR-01', name: 'Hakim Dr. Irfan Ashraf', role: 'Doctor / Senior Clinician', reg: 'CCIM-DEL-2014-9982', status: 'Active (21 CFR Signer)', suite: 'Chamber Suite #01' },
        { id: 'USR-02', name: 'Zubair Ahmad', role: 'Chief Pharmacist', reg: 'PCI-TEL-2018-4410', status: 'Active (FEFO Dispenser)', suite: 'Central Dispensary' },
        { id: 'USR-03', name: 'Sana Khan', role: 'Clinic OPD Receptionist', reg: 'EMP-ADM-2022-019', status: 'Active (Queue Intake)', suite: 'Front Desk OPD' },
        { id: 'USR-04', name: 'Rashid Mehmood', role: 'Manufacturing QA Chemist', reg: 'GMP-AYUSH-2020-881', status: 'Active (eBMR Officer)', suite: 'Herbal Dawakhana Wing' }
      ],
      consultationStep: 1
    };

    // Navigation Definitions by Role
    const roleNavs = {
      patient: [
        { id: 'home', label: 'Home' },
        { id: 'appointments', label: 'My Appointments' },
        { id: 'health', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> My Health' },
        { id: 'treatment', label: '<svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> Treatment Plan' },
        { id: 'medicines', label: '<svg class="w-4 h-4 inline-block text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg> My Medicines' },
        { id: 'reports', label: 'Reports' },
        { id: 'messages', label: 'Care Team' },
        { id: 'profile', label: 'Profile' }
      ],
      doctor: [
        { id: 'today', label: 'Today' },
        { id: 'patients', label: 'Patients & 360' },
        { id: 'consultation', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Consultation Suite' },
        { id: 'prescriptions', label: '<svg class="w-4 h-4 inline-block text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg> Prescriptions' },
        { id: 'ghiza', label: 'Ilaj bil Ghiza (Dietetics)' },
        { id: 'tadbeer', label: 'Ilaj bil Tadbeer (16 Modalities)' },
        { id: 'nafsiyat', label: 'Ilaj bil Nafsiyat (Mind & Psychosomatics)' },
        { id: 'yad', label: 'Ilaj bil Yad (Operative Surgery)' },
        { id: 'followups', label: 'Follow-ups' },
        { id: 'assistant', label: '<svg class="w-4 h-4 inline-block text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg> Clinical Assistant' },
        { id: 'knowledge', label: 'Clinical Knowledge' },
        { id: 'profile', label: 'Profile' }
      ],
      clinic: [
        { id: 'overview', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> Overview' },
        { id: 'appointments', label: 'Appointments' },
        { id: 'patients', label: 'Patients' },
        { id: 'queue', label: 'Live OPD Queue' },
        { id: 'doctors', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Doctors Roster' },
        { id: 'billing', label: 'Billing & Claims' },
        { id: 'settings', label: '⚙️ Clinic Settings' }
      ],
      nurse: [
        { id: 'ward', label: '🏥 Inpatient Ward & Beds' },
        { id: 'vitals', label: '🩺 Vitals Triage & Intake' },
        { id: 'meds', label: '💊 Medication Schedule (MAR)' },
        { id: 'rounds', label: '📋 Clinical Rounds & Notes' }
      ],
      pharmacy: [
        { id: 'dispensing', label: '<svg class="w-4 h-4 inline-block text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg> Dispensing Queue' },
        { id: 'inventory', label: 'Botanical Inventory (FEFO)' },
        { id: 'detox', label: '<svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg> Mudabbar Detoxification Gate' },
        { id: 'orders', label: 'Dispensed Orders' }
      ],
      research: [
        { id: 'zfie_studio', label: '<svg class="w-3.5 h-3.5 inline-block text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg> 🧬 ZFIE Discovery Studio' },
        { id: 'studies', label: '<svg class="w-4 h-4 inline-block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Active Clinical Trials' },
        { id: 'outcomes', label: 'Patient Outcomes (PROMs)' },
        { id: 'adverse', label: '<svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg> Adverse Event Reporting (ICH E2B)' }
      ],
      admin: [
        { id: 'organizations', label: 'Facilities & Clinics' },
        { id: 'users', label: 'User Permissions & RBAC' },
        { id: 'audit', label: '<svg class="w-3.5 h-3.5 inline-block text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg> Tamper-Evident Audit Ledger' },
        { id: 'safety', label: '<svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg> Safety Firewall Rules' },
        { id: 'engines', label: 'System Health & Engines' }
      ],
      enterprise: [
        { id: 'overview', label: 'Enterprise Overview' },
        { id: 'facilities', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> Multi-Facility Network' },
        { id: 'financials', label: 'Financials & Revenue' },
        { id: 'governance', label: '⚖️ 3-Specialist Governance' },
        { id: 'expansion', label: '<svg class="w-4 h-4 inline-block text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg> Global Matab Franchising' }
      ],
      manufacturing: [
        { id: 'bom', label: '📋 Master BOM & Specifications' },
        { id: 'batches', label: 'Active Batch Records (BMR)' },
        { id: 'testing', label: 'QC Chromatography & HPTLC' },
        { id: 'mudabbar', label: '<svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg> Schedule E(1) Detox Protocols' },
        { id: 'coa', label: 'Release Certificates (COA)' }
      ],
      website: [
        { id: 'home', label: '<svg class="w-4 h-4 inline-block text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg> Home' },
        { id: 'services', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Clinical Services' },
        { id: 'products', label: '<svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> Botanical Products' },
        { id: 'doctors', label: '‍⚕️ Faculty & Doctors' },
        { id: 'careers', label: '💼 Careers' },
        { id: 'ethics', label: '🛡️ Ethics Charter' },
        { id: 'research', label: '<svg class="w-4 h-4 inline-block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Research & RWE' },
        { id: 'knowledge', label: '📖 Medical Library' },
        { id: 'about', label: '🏛️ About' },
        { id: 'contact', label: '📞 Contact & Triage' },
        { id: 'pages25', label: '<svg class="w-4 h-4 inline-block text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg> Site Directory (25 Pages)' }
      ],
      herbals: [
        { id: 'catalog', label: '<svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> 32 Master Formulations Portfolio' },
        { id: 'cart', label: 'Live Cart & Checkout' },
        { id: 'monographs', label: 'Clinical Monographs' },
        { id: 'fefo', label: 'Dispensary Batch FEFO' }
      ],
      mobile: [
        { id: 'simulator', label: '<svg class="w-4 h-4 inline-block text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg> Bedside Mobile Interface' },
        { id: 'audio_posology', label: 'Vernacular Voice Guidance' },
        { id: 'asbab_sittah', label: '<svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> Asbab-e-Sittah 6 Essentials' },
        { id: 'companion', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Doctor Mobile Triage' }
      ],
      hardware: [
        { id: 'nabz', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> 10-Ajnas Nabz (Pulse) Sensor' },
        { id: 'lisan', label: 'Multispectral Lisan Camera' },
        { id: 'wearables', label: '⌚ Wearables BLE Stream' },
        { id: 'nir', label: 'NIR Botanical QC Scanner' },
        { id: 'coldchain', label: '️ Dispensary Cold-Chain IoT' }
      ]
    };
    window.state = state;

    function switchRole(newRole, bypassAuth = false) {
      const protectedRoles = ['doctor', 'pharmacy', 'clinic', 'nurse', 'admin', 'manufacturing', 'research', 'patient', 'enterprise', 'hardware', 'mobile'];
      const isSuperAdmin = state.currentUser && (state.currentUser.role === 'admin' || state.currentUser.role === 'super_admin' || state.currentUser.isSuperAdmin);

      // Security Gate: Protect all clinical & administrative consoles
      if (protectedRoles.includes(newRole) && !isSuperAdmin && !bypassAuth) {
        const hasSession = state.currentUser && (state.currentUser.role === newRole || (newRole === 'patient' && state.currentUser.role === 'patient'));
        if (!hasSession) {
          toggleLoginModal(true);
          prefillLogin(newRole);
          showNotification(`Please enter password and click 'Sign In' to access ${newRole.toUpperCase()} desk.`, 'info');
          return;
        }
      }

      if (newRole !== 'website' && newRole !== 'herbals') {
        const roleProfiles = {
          doctor: { name: 'Hakeem Dr. Irfan Ashraf', title: 'Senior Tabeeb & Lead Clinician (BUMS - AKTC AMU)', email: 'dr.irfan@zayvorahealth.com' },
          clinic: { name: 'Reception & Patient Intake Desk', title: 'OPD Queue & Token In-Charge', email: 'reception@zayvorahealth.com' },
          nurse: { name: 'Inpatient Nursing Station', title: 'Ward 2A Triage In-Charge', email: 'nurse@zayvorahealth.com' },
          patient: { name: 'Hamza Farooqi', title: 'Patient (MRN-2026-0814)', email: 'hamza.farooqi@gmail.com' },
          pharmacy: { name: 'Chief Pharmacist', title: 'Clinical Pharmacy & FEFO In-Charge', email: 'pharmacy@zayvorahealth.com' },
          manufacturing: { name: 'Head of Botanical QA/QC', title: 'eBMR Batch Release Officer', email: 'manufacturing@zayvorahealth.com' },
          admin: { name: 'Enterprise Super Administrator', title: 'Platform Security & Governance', email: 'admin@zayvorahealth.com' },
          research: { name: 'Principal Clinical Investigator', title: 'RWE & Pharmacopoeia Editorial Board', email: 'research@zayvorahealth.com' },
          enterprise: { name: 'Hakeem Dr. Irfan Ashraf', title: 'Founder & Chairman', email: 'dr.irfan@zayvorahealth.com' },
          hardware: { name: 'IoMT Hardware Gateway', title: 'Hardware Admin', email: 'hardware@zayvorahealth.com' },
          herbals: { name: 'Retail Guest', title: 'Herbal Store Customer', email: 'guest@zayvorahealth.com' },
          mobile: { name: 'Mobile Bedside User', title: 'PWA Bedside User', email: 'mobile@zayvorahealth.com' }
        };
        const p = roleProfiles[newRole] || { name: 'Authorized User', title: newRole.toUpperCase(), email: `${newRole}@zayvorahealth.com` };
        
        // If Super Admin is switching between desks, preserve Super Admin status!
        if (isSuperAdmin) {
          state.currentUser.activeDesk = newRole;
          state.currentUser.title = `Super Admin Oversight • ${newRole.toUpperCase()} Desk`;
        } else if (state.currentUser && state.currentUser.token) {
          state.currentUser.role = newRole;
        } else if (bypassAuth) {
          const secureToken = 'zyv.' + btoa(JSON.stringify({ uid: 'USR-' + newRole.toUpperCase(), email: p.email, name: p.name, role: newRole, exp: Math.floor(Date.now() / 1000) + 86400 })) + '.sig';
          state.currentUser = { email: p.email, name: p.name, title: p.title, role: newRole, isSuperAdmin: (newRole === 'admin'), token: secureToken };
        }
      }
      state.role = newRole;
      state.tab = (roleNavs[newRole] && roleNavs[newRole][0]) ? roleNavs[newRole][0].id : 'overview';
      try { sessionStorage.setItem('zayvora_session_desk', newRole); } catch(e) {}
      const sel = document.getElementById('role-selector');
      if (sel) sel.value = newRole;
      updateAuthHeaderUI();
      renderNavigation();
      renderWorkspace();
      try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch(e) {}
    }

    function switchTab(newTab) {
      state.tab = newTab;
      if (state.role === 'website') {
        try {
          if (window.history && window.history.pushState) {
            window.history.pushState(null, null, '#' + newTab);
          } else {
            window.location.hash = newTab;
          }
        } catch (e) {}
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        const ws = document.getElementById('workspace-container');
        if (ws && window.scrollY > 180) {
          ws.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
      renderNavigation();
      renderWorkspace();
    }

    function isTabActive(itemId, currentTab) {
      if (itemId === currentTab) return true;
      if (state.role === 'website') {
        if (itemId === 'doctors' && (currentTab === 'doctors' || currentTab === 'team')) return true;
        if (itemId === 'careers' && currentTab === 'careers') return true;
        if (itemId === 'ethics' && currentTab === 'ethics') return true;
        if (itemId === 'services' && (currentTab.startsWith('services_') || currentTab === 'care_journey' || currentTab === 'clinics')) return true;
        if (itemId === 'products' && (currentTab.startsWith('products_') || currentTab === 'shipping_refunds')) return true;
        if (itemId === 'knowledge' && currentTab === 'knowledge') return true;
        if (itemId === 'research' && currentTab.startsWith('research_')) return true;
        if (itemId === 'about' && (currentTab === 'philosophy' || currentTab === 'privacy' || currentTab === 'terms' || currentTab === 'disclaimer' || currentTab === 'refunds' || currentTab === 'shipping' || currentTab === 'grievance')) return true;
        if (itemId === 'contact' && currentTab === 'faqs') return true;
      }
      return false;
    }

    function renderNavigation() {
      const navContainer = document.getElementById('role-navigation');
      const navItems = roleNavs[state.role] || [];
      let html = navItems.map(item => `
        <button onclick="switchTab('${item.id}')" class="nav-link shrink-0 ${isTabActive(item.id, state.tab) ? 'active' : 'text-[var(--muted)] hover:text-white'} px-3.5 py-1.5 rounded-xl text-xs font-medium border border-transparent transition-colors">
          ${item.label}
        </button>
      `).join('');

      if (state.role === 'website') {
        html += `
          <button onclick="document.getElementById('site-footer-directory')?.scrollIntoView({ behavior: 'smooth' })" class="shrink-0 text-xs text-slate-400 hover:text-emerald-400 px-3 py-1.5 rounded-xl border border-dashed border-slate-700/80 hover:border-emerald-500/50 flex items-center gap-1.5 transition ml-auto" title="Explore all 25 canonical pages & complete sitemap in footer">
            <span>Sitemap &amp; Directory ↓</span>
          </button>
        `;
      }
      navContainer.innerHTML = html;
    }

    function showNotification(text, type = 'success') {
      const banner = document.getElementById('system-notification');
      const textEl = document.getElementById('system-notif-text');
      const iconEl = document.getElementById('system-notif-icon');

      textEl.textContent = text;
      if (type === 'success') {
        banner.className = "p-4 rounded-xl border text-xs flex items-center justify-between bg-emerald-500/10 border-emerald-500/30 text-emerald-300";
        iconEl.textContent = "✓";
      } else if (type === 'error') {
        banner.className = "p-4 rounded-xl border text-xs flex items-center justify-between bg-rose-500/10 border-rose-500/30 text-rose-300";
        iconEl.textContent = "✕";
      } else {
        banner.className = "p-4 rounded-xl border text-xs flex items-center justify-between bg-blue-500/10 border-blue-500/30 text-blue-300";
        iconEl.textContent = "ℹ";
      }
      banner.classList.remove('hidden');
      setTimeout(() => banner.classList.add('hidden'), 5000);
    }

    function dismissNotification() {
      document.getElementById('system-notification').classList.add('hidden');
    }

    function toggleHelpModal() {
      const el = document.getElementById('help-modal');
      el.classList.toggle('hidden');
    }

