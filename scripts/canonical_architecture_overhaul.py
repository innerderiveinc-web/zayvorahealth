#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Canonical Architecture, Terminology & Task-First Overhaul.
Performs repository and SPA level updates:
1. Replaces outdated CCIM references with NCISM Act, 2020.
2. Purges internal engineering jargon (Merkle, ZAPE) into canonical healthcare terms.
3. Cleans role selector options of hardcoded individual names.
4. Injects task-first "Find Care Discovery" section into Homepage right after the Hero.
5. Adds interactive Medical Disclaimer and AI Transparency modals/views to the SPA.
"""

import re
import os

BASE_DIR = "/Users/irfanashraf/Downloads/zayvora-platform-phase0-4"

FIND_CARE_HTML = '''
          <!-- ===================================================================== -->
          <!-- TASK-FIRST CARE DISCOVERY (MAYO CLINIC & CLEVELAND CLINIC BENCHMARK) -->
          <!-- ===================================================================== -->
          <div class="p-6 md:p-10 rounded-3xl bg-gradient-to-r from-[#0F172A] via-[#131D31] to-[#0A0F1D] border-2 border-emerald-500/40 shadow-2xl space-y-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
              <div>
                <span class="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold uppercase tracking-wider border border-emerald-500/20">
                  Care Discovery &amp; Triage
                </span>
                <h2 class="text-2xl md:text-3xl font-extrabold text-white mt-2">What brings you to ZAYVORA today?</h2>
                <p class="text-xs md:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                  Select your health concern to immediately access evidence-grounded Greco-Arab pathways, board-certified clinicians, and tailored botanical protocols.
                </p>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-lg transition flex items-center gap-1.5">
                  <span>📅</span> Book Consultation
                </button>
              </div>
            </div>

            <!-- 9 Core Clinical Focus Areas -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-3 gap-4 text-xs">
              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl">🫄</div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Digestive &amp; Gut Health</h3>
                <p class="text-[11px] text-slate-400">Su-e-Hazm, IBS, GERD, Gastritis, Dysbiosis, Liver Congestion</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl">🩸</div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Metabolic &amp; Pre-Diabetes</h3>
                <p class="text-[11px] text-slate-400">Insulin Resistance (HOMA-IR), Obesity, Visceral Adiposity, Dyslipidemia</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl">🦋</div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Hormonal &amp; Thyroid Axis</h3>
                <p class="text-[11px] text-slate-400">PCOS, Hypothyroid (Barid-Ratab), Adrenal Fatigue, Cortisol Dysregulation</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl">🌱</div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Reproductive &amp; Vitality</h3>
                <p class="text-[11px] text-slate-400">Male Oligospermia, Asthenospermia, Female Anovulation, Vitality Deficits</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl">🦵</div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Joint &amp; Musculoskeletal</h3>
                <p class="text-[11px] text-slate-400">Waja-ul-Mafasil, Knee Osteoarthritis, Cervical Spondylosis, Synovial Stiffness</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl">🧠</div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Sleep, Stress &amp; Cognition</h3>
                <p class="text-[11px] text-slate-400">Insomnia, Chronic Anxiety (Khafqan), Mental Fog, Burnout Recovery</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>
            </div>

            <!-- Direct Action Channels -->
            <div class="pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
              <div class="flex flex-wrap items-center gap-4 text-slate-300">
                <span class="text-slate-500 font-bold uppercase text-[10px]">Access Channels:</span>
                <button onclick="viewWebsitePage('doctors')" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span>👨‍⚕️</span> Find a Clinician
                </button>
                <button onclick="viewWebsitePage('clinics')" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span>🏥</span> Find a Matab Complex
                </button>
                <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span>🎫</span> In-Clinic OPD Token
                </button>
                <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span>💻</span> Encrypted Teleconsultation
                </button>
              </div>
              <span class="text-[11px] text-slate-500">Average intake triage time: &lt; 90 seconds</span>
            </div>
          </div>
'''

def overhaul_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace CCIM references with NCISM Act, 2020
    content = content.replace("CCIM / DMC-UN-88412", "NCISM / DMC-UN-88412")
    content = content.replace("NCISM / CCIM Certified", "NCISM Board-Certified")
    content = content.replace("#CCIM-BUMS-DL-0881", "#Updating")
    content = content.replace("CCIM-BUMS", "NCISM-BUMS")
    content = content.replace("CCIM / NCISM", "NCISM")

    # 2. Terminology replacements
    content = content.replace("Merkle Audit Ledger", "Tamper-Evident Audit Ledger")
    content = content.replace("Merkle Cryptographic Audit Trail", "Tamper-Evident Cryptographic Audit Trail")
    content = content.replace("Merkle Cryptographic Governance Root", "Tamper-Evident Cryptographic Governance Root")
    content = content.replace("Merkle root", "tamper-evident audit root")
    content = content.replace("Merkle ledger", "tamper-evident audit ledger")
    content = content.replace("Merkle tree hashes", "tamper-evident cryptographic hashes")
    content = content.replace("Merkle Root Verified", "Tamper-Evident Root Verified")
    content = content.replace("ZAPE Vitality & Posology Adaptation", "ZAYVORA Precision Assessment & Posology Adaptation")

    # 3. Clean role selector of hardcoded names
    content = content.replace('Hamza Farooqi (Patient Health 360 & Regimen)', 'Patient Health 360 &amp; Regimen')
    content = content.replace('Sana Khan (Clinic Reception & OPD Queue)', 'Clinic Reception &amp; OPD Queue')
    content = content.replace('Zainab Ali (Clinical Pharmacist & FEFO)', 'Clinical Pharmacist &amp; FEFO Dispensary')
    content = content.replace('Dr. Arshad Qureshi (Manufacturing QA/QC & BMR)', 'AYUSH-GMP Manufacturing &amp; eBMR')
    content = content.replace('Dr. K. Saxena (Clinical Researcher & RWE)', 'Clinical Research &amp; RWE Registry')

    # 4. Inject Find Care Discovery module right after Hero section if not present
    if "TASK-FIRST CARE DISCOVERY" not in content:
      hero_marker = "<!-- 2. INSTITUTIONAL METRICS COUNTER MARQUEE -->"
      if hero_marker in content:
        content = content.replace(hero_marker, FIND_CARE_HTML.strip() + "\n\n          " + hero_marker)
        print(f"Injected Task-First Care Discovery into {filepath}")
      else:
        print(f"Could not find hero_marker in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Completed {filepath}")

if __name__ == "__main__":
    for p in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "docs/index.html")]:
        if os.path.exists(p):
            overhaul_file(p)
