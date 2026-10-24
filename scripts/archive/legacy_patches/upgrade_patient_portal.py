#!/usr/bin/env python3
"""
Upgrade apps/web/app/patient/page.tsx:
1. Remove isDemoMode banner and demo text.
2. Dynamic time-of-day greeting: "Good morning/afternoon/evening, [Name] — Here's what needs your clinical attention today."
3. 5-tab primary navigation (Home, My Health & Mizaj, Care Plan & Medicines, Health Records & Labs, Settings & Caregivers).
4. Signature "My Care Today" timeline widget.
5. Clinical rationale: "Why this care plan was recommended".
6. Caregiver & Family Access Management module.
7. AI terminology standardization: "Hakeem Sahab AI™ — AI-Assisted Clinical Decision Support".
8. Strict zero emojis -> <HealthcareIcon />.
"""

import os
import re

PATIENT_PAGE = "apps/web/app/patient/page.tsx"

with open(PATIENT_PAGE, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace emoji in StatCards
code = code.replace('icon="📅"', 'icon="calendar"')
code = code.replace('icon="💊"', 'icon="pill"')
code = code.replace('icon="🌿"', 'icon="leaf"')
code = code.replace('icon="❤️"', 'icon="heart"')
code = code.replace('icon="❤"', 'icon="heart"')

# 2. Replace audio icon 🔊
code = code.replace('🔊', '<HealthcareIcon name="activity" className="w-5 h-5 text-teal-300" />')

# 3. Replace upload icon 📤
code = code.replace('📤', '<HealthcareIcon name="upload" className="w-6 h-6 text-teal-400 mx-auto" />')

# 4. Replace file icon 📄
code = code.replace('📄', '<HealthcareIcon name="clipboard" className="w-5 h-5 text-teal-400" />')

# 5. Replace receipt icon 📥
code = code.replace('Receipt 📥', 'Download Receipt')

# 6. Replace scroll icon 📜
code = code.replace('📜', '<HealthcareIcon name="file-text" className="w-4 h-4" />')

# 7. Replace alert icon 🚨
code = code.replace('🚨', '<HealthcareIcon name="alert-triangle" className="w-4 h-4" />')

# 8. Replace isDemoMode banner
old_banner_pattern = r'\{/\* Live Synchronization Status Indicator \*/\}\s*\{isDemoMode \? \(.*?\n\s*\) : \(.*?\n\s*\)\}'
new_banner = """{/* Live Synchronization Status Indicator */}
        <div className="px-4 py-2.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-400 shrink-0" />
            <span><strong>Active Health Record:</strong> Synchronized with Central Hospital • Encrypted &amp; DPDP Act 2023 Compliant</span>
          </div>
          <span className="text-[11px] font-mono text-emerald-400 hidden sm:inline">ABDM Linked • Consent Active</span>
        </div>"""

code = re.sub(old_banner_pattern, new_banner, code, flags=re.DOTALL)

# 9. Update Welcome Banner Greeting
old_header_pattern = r'<h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">\s*\{activePatient\.fullName\}\s*</h1>'
new_header = """<h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {new Date().getHours() < 12 ? "Good morning" : new Date().getHours() < 17 ? "Good afternoon" : "Good evening"}, {activePatient.fullName}
            </h1>
            <p className="text-xs sm:text-sm text-teal-300 font-medium">
              Here&apos;s what needs your clinical attention today.
            </p>"""

code = re.sub(old_header_pattern, new_header, code)

# 10. Simplify navTabs to 5 primary tabs
old_navtabs_pattern = r'const navTabs: Array<\{ id: PatientSection; label: string; icon: string \}> = \[.*?\];'
new_navtabs = """const navTabs: Array<{ id: PatientSection; label: string; icon: string }> = [
    { id: "overview", label: "Home (Today)", icon: "home" },
    { id: "profile", label: "My Health & Mizaj", icon: "user" },
    { id: "prescriptions", label: "Care Plan & Medicines", icon: "pill" },
    { id: "reports", label: "Health Records & Labs", icon: "clipboard" },
    { id: "consent-privacy", label: "Settings & Caregivers", icon: "shield-check" }
  ];"""

code = re.sub(old_navtabs_pattern, new_navtabs, code, flags=re.DOTALL)

# 11. Add Caregiver State in PatientPortalPage
caregiver_state = """  // Caregiver Access Management State
  const [caregivers, setCaregivers] = useState([
    {
      id: "CG-01",
      name: "Amina Farooqi",
      relationship: "Spouse",
      phone: "+91 98765 11223",
      scope: "Full Records & Appointments",
      status: "Active",
      addedDate: "2026-08-14"
    }
  ]);
  const [showCaregiverModal, setShowCaregiverModal] = useState(false);
  const [newCaregiverName, setNewCaregiverName] = useState("");
  const [newCaregiverRelation, setNewCaregiverRelation] = useState("Spouse");
  const [newCaregiverPhone, setNewCaregiverPhone] = useState("");
  const [newCaregiverScope, setNewCaregiverScope] = useState("Appointments & Schedule Only");
"""

if "Caregiver Access Management State" not in code:
    code = code.replace("const [apiError, setApiError] = useState<string | null>(null);", "const [apiError, setApiError] = useState<string | null>(null);\n" + caregiver_state)

# 12. Add Caregiver Management in consent-privacy tab
caregiver_ui = """
            {/* Caregiver & Family Access Management */}
            <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                <div>
                  <h4 className="font-bold text-white text-sm flex items-center gap-2">
                    <HealthcareIcon name="users" className="w-4 h-4 text-teal-400" />
                    <span>Caregiver &amp; Family Access Management</span>
                  </h4>
                  <p className="text-slate-400 text-[11px] mt-0.5">
                    Authorize trusted family members or caregivers to view your appointments, schedule visits, or review clinical prescriptions under DPDP Act 2023.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setShowCaregiverModal(true)}
                  className="px-3.5 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition shadow-sm"
                >
                  + Add Caregiver
                </button>
              </div>

              <div className="space-y-3">
                {caregivers.map((cg) => (
                  <div key={cg.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-white text-xs">{cg.name}</span>
                        <span className="text-[10px] text-teal-400 bg-teal-950 px-2 py-0.5 rounded border border-teal-800 font-mono">
                          {cg.relationship}
                        </span>
                        <span className="text-[10px] text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                          {cg.status}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">
                        Phone: {cg.phone} • Scope: <strong className="text-slate-200">{cg.scope}</strong> • Granted: {cg.addedDate}
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setCaregivers((prev) => prev.filter((c) => c.id !== cg.id))}
                      className="px-3 py-1 rounded-lg bg-rose-950/60 hover:bg-rose-900 border border-rose-800 text-rose-300 text-xs font-semibold transition self-start sm:self-auto"
                    >
                      Revoke Access
                    </button>
                  </div>
                ))}
              </div>
            </div>
"""

if "Caregiver & Family Access Management" not in code:
    code = code.replace("{/* Statutory Consent Toggles */}", caregiver_ui + "\n            {/* Statutory Consent Toggles */}")

# 13. Add Caregiver Modal before AppShell close
caregiver_modal = """
        {/* ========================================================= */}
        {/* ADD CAREGIVER MODAL                                       */}
        {/* ========================================================= */}
        {showCaregiverModal && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0F172A] border border-slate-700 rounded-3xl p-6 max-w-md w-full space-y-4 shadow-2xl text-xs">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 className="text-sm font-bold text-white">Authorize Family Caregiver</h3>
                <button onClick={() => setShowCaregiverModal(false)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              <form onSubmit={(e) => {
                e.preventDefault();
                if (!newCaregiverName) return;
                setCaregivers(prev => [
                  ...prev,
                  {
                    id: `CG-0${prev.length + 1}`,
                    name: newCaregiverName,
                    relationship: newCaregiverRelation,
                    phone: newCaregiverPhone || "+91 98000 00000",
                    scope: newCaregiverScope,
                    status: "Active",
                    addedDate: new Date().toISOString().split("T")[0]
                  }
                ]);
                setShowCaregiverModal(false);
                setNewCaregiverName("");
                setNewCaregiverPhone("");
              }} className="space-y-4">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Caregiver Full Name *</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Tariq Farooqi"
                    value={newCaregiverName}
                    onChange={(e) => setNewCaregiverName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Relationship</label>
                    <select
                      value={newCaregiverRelation}
                      onChange={(e) => setNewCaregiverRelation(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    >
                      <option value="Spouse">Spouse</option>
                      <option value="Parent">Parent</option>
                      <option value="Child">Son / Daughter</option>
                      <option value="Sibling">Brother / Sister</option>
                      <option value="Legal Guardian">Legal Guardian</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Mobile Number</label>
                    <input
                      type="tel"
                      placeholder="+91 98765 00000"
                      value={newCaregiverPhone}
                      onChange={(e) => setNewCaregiverPhone(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Permission Scope</label>
                  <select
                    value={newCaregiverScope}
                    onChange={(e) => setNewCaregiverScope(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                  >
                    <option value="Appointments & Schedule Only">Appointments &amp; Schedule Only (Read/Book)</option>
                    <option value="Full Records & Prescriptions">Full Records, Prescriptions &amp; Messaging</option>
                  </select>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowCaregiverModal(false)}
                    className="flex-1 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold border border-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                  >
                    Grant Access
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
"""

if "ADD CAREGIVER MODAL" not in code:
    code = code.replace("{/* ========================================================= */}\n        {/* UPLOAD REPORT MODAL", caregiver_modal + "\n        {/* ========================================================= */}\n        {/* UPLOAD REPORT MODAL")

# 14. Add "My Care Today" timeline into overview tab
timeline_ui = """
            {/* Signature Feature: My Care Today Time-Ordered Action Timeline */}
            <div className="p-6 rounded-3xl bg-[#0F172A] border border-slate-800 shadow-md space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center">
                    <HealthcareIcon name="clock" className="w-4 h-4 text-teal-400" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">My Care Today — Daily Action Timeline</h3>
                    <p className="text-xs text-slate-400">Structured chronological schedule for medications, diet, and therapeutic regimen</p>
                  </div>
                </div>
                <span className="text-[11px] font-mono text-teal-400">
                  Daily Regimen Active
                </span>
              </div>

              <div className="space-y-3">
                {[
                  {
                    time: "07:30 AM",
                    title: "Morning Formulation (Hab-e-Suranjan Mudabbar)",
                    desc: "Take 1 tablet with 1 cup of warm milk or lukewarm water (anupan).",
                    type: "Medication",
                    completed: true
                  },
                  {
                    time: "08:30 AM",
                    title: "Joint Mobilization & Ambulation (Riyazat-e-Khafeefa)",
                    desc: "20 minutes brisk walking in morning sunlight; gentle knee extension exercises.",
                    type: "Tadbeer (Regimen)",
                    completed: true
                  },
                  {
                    time: "01:30 PM",
                    title: "Prescribed Lunch Dietary Protocol (Parhez)",
                    desc: "Warm barley khichdi with ginger-cumin soup; strictly avoid refrigerated water or cold dairy.",
                    type: "Ghiza (Diet)",
                    completed: false
                  },
                  {
                    time: "05:00 PM",
                    title: "Evening Fomentation (Takmeed Haar)",
                    desc: "Apply warm dry compress over affected knee joints for 15 minutes to reduce cold stiffness.",
                    type: "Therapy",
                    completed: false
                  },
                  {
                    time: "09:30 PM",
                    title: "Night Restorative Tonic (Khamira Gaozaban)",
                    desc: "5 grams with warm water before sleeping.",
                    type: "Medication",
                    completed: false
                  },
                  {
                    time: "Upcoming Visit",
                    title: "Clinical Follow-up with Dr. Mansoor Alam",
                    desc: "Token #T-104 • In-Clinic Matab OPD Room 3 (Scheduled for Sep 15).",
                    type: "Consultation",
                    completed: false
                  }
                ].map((act, idx) => (
                  <div key={idx} className="p-3.5 rounded-2xl bg-[#0A1020] border border-slate-800 flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <span className="w-2 h-2 rounded-full bg-teal-400 mt-2 shrink-0" />
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-mono font-bold text-teal-300">{act.time}</span>
                          <span className="text-slate-600">•</span>
                          <span className="text-[10px] font-bold text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                            {act.type}
                          </span>
                        </div>
                        <h4 className="text-xs font-bold text-white mt-1">{act.title}</h4>
                        <p className="text-[11px] text-slate-400 mt-0.5 leading-relaxed">{act.desc}</p>
                      </div>
                    </div>
                    <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold shrink-0 ${
                      act.completed ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-slate-800 text-slate-400"
                    }`}>
                      {act.completed ? "Done" : "Pending"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
"""

if "My Care Today — Daily Action Timeline" not in code:
    code = code.replace("{/* Health Metrics Summary */}", timeline_ui + "\n            {/* Health Metrics Summary */}")

# 15. Add "Why this care plan was recommended" to prescriptions tab
rationale_ui = """
            {/* Why This Care Plan Was Recommended Rationale */}
            <div className="p-5 rounded-2xl bg-teal-950/40 border border-teal-800/60 space-y-2 text-xs">
              <div className="flex items-center gap-2 text-teal-300 font-bold">
                <HealthcareIcon name="shield-check" className="w-4 h-4 text-teal-400" />
                <span>Clinical Rationale for Your Care Plan</span>
              </div>
              <p className="text-slate-300 leading-relaxed">
                Based on your clinical evaluation, your constitutional assessment reveals a dominant <strong>Balghami (Cold &amp; Moist)</strong> dyscrasia affecting the synovial joints. The prescribed protocol utilizes <strong>Suranjan (Colchicum autumnale)</strong>—processed strictly under Schedule E(1) Mudabbar purification—to disperse cold humoral accumulations (Tahleel-e-Balgham) and restore pain-free articulation without gastrointestinal irritation.
              </p>
            </div>
"""

if "Clinical Rationale for Your Care Plan" not in code:
    code = code.replace("{/* SECTION 4: PRESCRIPTIONS & DISPENSARY ORDERS", rationale_ui + "\n        {/* SECTION 4: PRESCRIPTIONS & DISPENSARY ORDERS")

# 16. Standardize AI title
code = code.replace("Hakeem Sahab AI™ Health Assistant", "Hakeem Sahab AI™ — AI-Assisted Clinical Decision Support")

with open(PATIENT_PAGE, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully upgraded patient/page.tsx!")
