import re
import sys

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add Nuskha Preflight Modal & Evidence Drawer HTML right before </body>
    modals_html = """
  <!-- ===================================================================== -->
  <!-- 21 CFR PART 11 NUSKHA PREFLIGHT & DIGITAL SIGNATURE MODAL -->
  <!-- ===================================================================== -->
  <div id="nuskha-preflight-modal" class="hidden fixed inset-0 bg-black/75 backdrop-blur-md z-50 flex items-center justify-center p-4">
    <div class="bg-[var(--card)] border-2 border-emerald-500/40 rounded-3xl max-w-2xl w-full p-6 md:p-8 space-y-5 shadow-2xl animate-fade-in text-xs">
      
      <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold text-sm">
            🔒
          </span>
          <div>
            <h3 class="font-extrabold text-base text-white">Nuskha Preflight & 21 CFR Part 11 Digital Signoff</h3>
            <span class="text-[11px] text-[var(--muted)]">Mandatory Statutory Review Barrier before Locking Prescription</span>
          </div>
        </div>
        <button onclick="closeNuskhaPreflightModal()" class="text-[var(--muted)] hover:text-white font-bold text-base">✕</button>
      </div>

      <!-- Preflight Checklist Cards -->
      <div class="space-y-2.5 max-h-[60vh] overflow-y-auto pr-1">
        
        <!-- Checklist 1: Patient & Encounter Identity -->
        <div class="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">1. Patient & Encounter Identity</span>
            <strong class="text-white text-xs">Hamza Farooqi (MRN-2026-0008) • ABHA: 91-1234-5678-9012</strong>
            <p class="text-[11px] text-[var(--muted)] mt-0.5">Encounter ID: ENC-2026-0914 • Age 42y Male • Facility: Central Hospital Delhi</p>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold safety-badge-pass">PASS</span>
        </div>

        <!-- Checklist 2: Canonical Substance Identity -->
        <div class="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">2. Substance Identity Reconciliation</span>
            <strong class="text-white text-xs">Hab-e-Suranjan (ZMF-096) + Roghan-e-Suranjan (ZMF-112)</strong>
            <p class="text-[11px] text-[var(--muted)] mt-0.5">0 confusable botanical pairs • Canonical ZKB botanical monographs verified.</p>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold safety-badge-pass">PASS</span>
        </div>

        <!-- Checklist 3: Evidence Grounding -->
        <div class="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">3. Evidence & Monograph Grounding</span>
            <strong class="text-white text-xs">UPI Vol I, p. 112 & Kitab al-Aghziya (Tier E3 / Grade B+)</strong>
            <p class="text-[11px] text-[var(--muted)] mt-0.5">Indications and dosage match statutory pharmacopoeia standards.</p>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold safety-badge-pass">PASS</span>
        </div>

        <!-- Checklist 4: Safety Firewall & Detoxification -->
        <div class="p-3.5 rounded-2xl bg-[var(--background)] border border-amber-500/40 flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">4. Safety Firewall & Schedule E(1) Mudabbar</span>
            <strong class="text-white text-xs">Mudabbar Certificate #DETOX-2026-04 Attached</strong>
            <p class="text-[11px] text-[var(--muted)] mt-0.5">Colchicum alkaloids purified in cow's milk per classical formulary standard.</p>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold safety-badge-caution">VERIFIED</span>
        </div>

        <!-- Checklist 5: Clinician Credential Verification -->
        <div class="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">5. Clinician Statutory Scope</span>
            <strong class="text-white text-xs">Hakim Dr. Tariq Mansoor • NCISM Reg: #ND-9842-A</strong>
            <p class="text-[11px] text-[var(--muted)] mt-0.5">Credential Active • Scope: Outpatient Integrative Internal Medicine</p>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold safety-badge-pass">ACTIVE</span>
        </div>

      </div>

      <!-- Digital Signature Input Section -->
      <div class="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/40 space-y-3">
        <div class="flex items-center justify-between">
          <span class="font-bold text-emerald-300">Clinician Electronic Signature (21 CFR Part 11)</span>
          <span class="text-[10px] text-emerald-400 font-mono">SHA-256 Merkle Ledger</span>
        </div>
        <div class="flex items-center gap-3">
          <input id="clinician-pin-input" type="password" placeholder="Enter Clinician Signing PIN (e.g. 1234)" class="px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white text-xs flex-1 focus:outline-none focus:border-emerald-400 font-mono" />
          <button onclick="executeNuskhaDigitalSeal()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">
            Sign & Seal Prescription →
          </button>
        </div>
        <p class="text-[10px] text-[var(--muted)]">
          By entering your PIN, you confirm under penalty of medical license revocation that this prescription complies with the Unani Pharmacopoeia of India and NCISM clinical guidelines.
        </p>
      </div>

    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- FIRST-CLASS EVIDENCE DRAWER (PROMPT SECTION 23) -->
  <!-- ===================================================================== -->
  <div id="evidence-drawer-overlay" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex justify-end">
    <div class="w-full max-w-xl bg-[#0F172A] border-l border-[#334155] h-full shadow-2xl flex flex-col animate-slide-left text-xs">
      
      <!-- Drawer Header -->
      <div class="p-5 border-b border-[#334155] flex items-center justify-between bg-[#1E293B]">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold text-sm">
            📚
          </div>
          <div>
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              Evidence Provenance Drawer
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Tier E3 / Grade B+</span>
            </h3>
            <span class="text-[11px] text-[#94A3B8]">6-Point Statutory Grounding & Provenance Ledger</span>
          </div>
        </div>
        <button onclick="toggleEvidenceDrawer(false)" class="text-[#94A3B8] hover:text-white text-base font-bold px-2 py-1">✕</button>
      </div>

      <!-- Drawer Body: The 6 Mandatory Provenance Questions -->
      <div class="p-6 flex-1 overflow-y-auto space-y-4">
        
        <!-- 1. WHAT IS THE CLAIM? -->
        <div class="p-4 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1.5">
          <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">1. What is the Clinical Claim?</span>
          <p class="text-white font-medium">Resolvent (Muhallil) and analgesic efficacy for chronic phlegmatic arthralgia (Waja-ul-Mafasil / Osteoarthritis).</p>
        </div>

        <!-- 2. WHAT IS THE SOURCE? -->
        <div class="p-4 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1.5">
          <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">2. What is the Authoritative Source?</span>
          <p class="text-white font-medium">Unani Pharmacopoeia of India (UPI) Vol I, Page 112, Monograph #048 • Ministry of AYUSH, Govt of India.</p>
          <p class="text-[11px] text-[var(--muted)]">Classical cross-reference: <em>Al-Qanun fi al-Tibb</em> (Ibn Sina), Kitab al-Adwiya al-Mufradah, Maqala 2.</p>
        </div>

        <!-- 3. HOW STRONG IS THE EVIDENCE? -->
        <div class="p-4 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1.5">
          <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">3. How Strong is the Evidence?</span>
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 rounded font-bold bg-emerald-500/20 text-emerald-400 font-mono">Tier E3</span>
            <span class="text-white font-semibold">Grade B+ (Consensus Pharmacopoeia + Real-World Evidence Registry)</span>
          </div>
          <p class="text-[11px] text-[var(--muted)]">1,240+ multi-center observational subjects in ZAYVORA registry confirm 76.4% pain attenuation at Day 28.</p>
        </div>

        <!-- 4. WHO REVIEWED IT? -->
        <div class="p-4 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1.5">
          <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">4. Who Reviewed and Approved It?</span>
          <p class="text-white font-medium">Dr. K. Saxena (Chief Pharmacognosist) & Dr. Tariq Mansoor (Chief Clinician) • Clinical Board Quorum 3/3 signed.</p>
        </div>

        <!-- 5. WHEN WAS IT REVIEWED? -->
        <div class="p-4 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1.5">
          <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">5. When Was the Review Certified?</span>
          <p class="text-white font-mono">14 June 2026 • Knowledge Release v5.2 • Audit Hash: a9b4c810fe7...</p>
        </div>

        <!-- 6. WHAT ARE THE LIMITATIONS? -->
        <div class="p-4 rounded-2xl bg-[var(--card)] border border-amber-500/30 space-y-1.5">
          <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">6. What are the Clinical Limitations?</span>
          <p class="text-[var(--muted)] leading-relaxed">
            Must not be prescribed without Mudabbar detoxification. Co-administration of <em>Kateera</em> or <em>Maa-ul-Sha'eer</em> mandatory for Safrawi or gastric-sensitive temperaments.
          </p>
        </div>

      </div>

      <!-- Drawer Footer -->
      <div class="p-4 border-t border-[#334155] bg-[#1E293B] flex items-center justify-between">
        <span class="text-[11px] text-[var(--muted)]">ZKB Graph Node: #ZKB-MONO-048</span>
        <button onclick="toggleEvidenceDrawer(false); showNotification('Evidence citation acknowledged and added to clinical encounter note.', 'info');" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-xs">
          Acknowledge & Close
        </button>
      </div>

    </div>
  </div>
    """

    if 'id="nuskha-preflight-modal"' not in html:
        html = html.replace('</body>', modals_html + '\n</body>', 1)
        print("✓ Injected Nuskha Preflight Modal and Evidence Drawer into HTML")

    # 2. Add JavaScript functions for Preflight, Evidence Drawer, and 12-Stage Governance
    js_functions = """
    // =========================================================================
    // NUSKHA PREFLIGHT & 21 CFR PART 11 DIGITAL SIGNATURE LOGIC
    // =========================================================================
    function approvePrescriptionAndLock() {
      openNuskhaPreflightModal();
    }

    function openNuskhaPreflightModal() {
      const modal = document.getElementById('nuskha-preflight-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeNuskhaPreflightModal() {
      const modal = document.getElementById('nuskha-preflight-modal');
      if (modal) modal.classList.add('hidden');
    }

    function executeNuskhaDigitalSeal() {
      const pin = document.getElementById('clinician-pin-input')?.value;
      if (!pin || pin.length < 4) {
        showNotification('Please enter your 4-digit Clinician Signing PIN.', 'error');
        return;
      }
      closeNuskhaPreflightModal();
      showNotification('✓ 21 CFR Part 11 Digital Signature Sealed: SHA256-8F72A1B94C! Prescription locked and transmitted to Central Pharmacy.', 'success');
      // Update Clinical Thread Stage to Treatment
      const ctBadge = document.querySelector('#clinical-thread-container span');
      if (ctBadge) ctBadge.textContent = 'Active: Stage 11 (Treatment)';
    }

    // =========================================================================
    // FIRST-CLASS EVIDENCE DRAWER TOGGLE
    // =========================================================================
    function toggleEvidenceDrawer(show) {
      const drawer = document.getElementById('evidence-drawer-overlay');
      if (!drawer) return;
      if (show) {
        drawer.classList.remove('hidden');
      } else {
        drawer.classList.add('hidden');
      }
    }
    """

    if '// NUSKHA PREFLIGHT & 21 CFR PART 11 DIGITAL SIGNATURE LOGIC' not in html:
        html = html.replace('function renderClinicalThread(', js_functions + '\n    function renderClinicalThread(', 1)
        print("✓ Injected Preflight, Evidence Drawer, and Signature JS functions")

    # 3. Update Evidence Provenance Card button in Zone 3 to call toggleEvidenceDrawer(true)
    old_ev_btn = '<button onclick="switchRole(\'website\'); switchTab(\'knowledge\');" class="w-full py-1.5 border border-[var(--border)] rounded-lg text-[10px] text-slate-300 hover:text-white hover:bg-[var(--background)] transition">\n                  Browse ZKB Pharmacopoeia →\n                </button>'
    new_ev_btn = '<button onclick="toggleEvidenceDrawer(true)" class="w-full py-1.5 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 font-bold border border-emerald-500/30 rounded-lg text-[10px] transition">\n                  Inspect 6-Point Evidence Drawer →\n                </button>'
    if old_ev_btn in html:
        html = html.replace(old_ev_btn, new_ev_btn, 1)
        print("✓ Connected Evidence Provenance button to toggleEvidenceDrawer(true)")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Saved updated index.html and docs/index.html")

if __name__ == '__main__':
    run()
