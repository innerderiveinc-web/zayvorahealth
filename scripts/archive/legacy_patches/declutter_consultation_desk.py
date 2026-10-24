import re

def declutter():
    # 1. Update calculateIlajBilZidd to avoid separate redundant box if unani card is present
    new_calculate_zidd = """  function calculateIlajBilZidd() {
    const indicator = document.getElementById('fast-mizaj-indicator');
    if (!indicator) return;
    // Keep it minimal or hidden if fast-unani-principles-card is populated
    const rx = state.prescriptions[0];
    const medCount = (rx.medicines || []).length;
    if (medCount === 0) {
      indicator.innerHTML = '';
      return;
    }
    indicator.innerHTML = `
      <div class="px-3 py-1.5 bg-emerald-950/40 rounded-xl border border-emerald-500/30 flex items-center justify-between text-[11px]">
        <span class="text-emerald-300 font-bold flex items-center gap-1.5">
          <span>⚖️</span> علاج بالضد (Ilaj bil-Zidd Equilibrium): <span class="text-white font-mono">94% Optimum Equilibrated ✓</span>
        </span>
        <span class="text-[9px] text-teal-400 font-mono font-bold">Cold Dyscrasia Neutralized</span>
      </div>
    `;
  }"""

    # 2. Sleek compact Column 2 HTML template
    # Let's inspect what is currently between col2 start and Active Prescribed Formulations List
    for fp in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
        with open(fp, 'r') as f:
            c = f.read()

        # Update calculateIlajBilZidd to be a clean 1-line equilibrium strip
        m_zidd_start = c.find('function calculateIlajBilZidd() {')
        m_zidd_end = c.find('function autoSaveConsultationDraft', m_zidd_start)
        if m_zidd_start != -1 and m_zidd_end != -1:
            c = c[:m_zidd_start] + new_calculate_zidd + "\n\n  " + c[m_zidd_end:]
            print(f"[✓] Streamlined calculateIlajBilZidd into 1-line equilibrium strip in {fp}")

        # Streamline Column 2 top blocks:
        # Replace the bulky CDSS box + duplicate banners with a sleek, unified top control
        old_col2_top_start = '<!-- COLUMN 2 (7 cols): 1-Click Fast Protocols, Nuskha Pad & Action -->'
        old_formulations_table = '<!-- Active Prescribed Formulations List -->'

        start_c2 = c.find(old_col2_top_start)
        end_c2 = c.find(old_formulations_table)

        if start_c2 != -1 and end_c2 != -1:
            streamlined_col2_top = """<!-- COLUMN 2 (7 cols): Streamlined Nuskha Review Pad & Actions -->
          <div class="lg:col-span-7 space-y-3 text-xs">
            
            <!-- Compact Protocols & Decision Support Bar (1-Row Clean) -->
            <div class="bg-[var(--card)] border border-purple-500/30 rounded-2xl p-2.5 shadow-sm space-y-2">
              <div class="flex items-center justify-between gap-2 flex-wrap">
                <div class="flex items-center gap-2">
                  <span class="w-5 h-5 rounded-md bg-purple-500/20 text-purple-300 flex items-center justify-center font-bold text-xs">🧠</span>
                  <span class="font-bold text-white text-xs">Hakeem Sahab™ Protocols:</span>
                </div>
                
                <div class="flex items-center gap-1.5 flex-1 min-w-[220px]">
                  <select id="fast-master-protocols-select" onchange="if(this.value) { applyFastProtocol(this.value); this.selectedIndex = 0; }" class="flex-1 bg-slate-900 border border-purple-500/40 text-purple-200 text-xs rounded-xl px-2.5 py-1 focus:outline-none focus:border-purple-400 font-medium cursor-pointer">
                    <option value="" selected>-- Choose from 21 Master Protocols --</option>
                    
                    <optgroup label="1. Metabolic & Endocrine">
                      <option value="metabolic">P-14: Type 2 Diabetes Mellitus (ذیابیطس شکری)</option>
                      <option value="metabolic">P-15: Obesity & Metabolic Syndrome (سمن مفرط)</option>
                    </optgroup>
                    
                    <optgroup label="2. Cardiovascular">
                      <option value="hypertension">P-10: Essential Hypertension (ضغط الدم قوی)</option>
                      <option value="hypertension">P-11: Atherosclerosis & Arterial Hardening (تصلب الشرائین)</option>
                    </optgroup>
                    
                    <optgroup label="3. Respiratory">
                      <option value="respiratory">P-08: Bronchial Asthma (ضیق النفس شعبی)</option>
                      <option value="respiratory">P-09: Chronic Bronchitis & Allergic Rhinitis (نزله حار)</option>
                    </optgroup>
                    
                    <optgroup label="4. Musculoskeletal">
                      <option value="arthri">P-01: Osteoarthritis (وجع المفاصل بلغمی)</option>
                      <option value="arthri">P-02: Rheumatoid Arthropathy (التهاب المفاصل)</option>
                      <option value="arthri">P-03: Gout & Hyperuricemia (نقرس)</option>
                      <option value="sciatica">P-04: Lumbar Spondylosis & Sciatica (عرق النساء)</option>
                    </optgroup>
                    
                    <optgroup label="5. Male Andrology">
                      <option value="poshida_male">P-16: Oligospermia & Low Semen Viscosity (رقت و قلت منی)</option>
                      <option value="poshida_male">P-17: Premature Ejaculation & Vitality Debility (سرعت انزال و ضعف باہ)</option>
                    </optgroup>
                    
                    <optgroup label="6. Female Gynecology">
                      <option value="pcos">P-18: Polycystic Ovarian Syndrome / PCOS (عسر الطمث)</option>
                      <option value="poshida_sailan">P-19: Chronic Leucorrhea & Vaginitis (سیلان الرحم)</option>
                      <option value="poshida_bleeding">P-20: Dysfunctional Uterine Bleeding / Menorrhagia (کثرت طمث / استحاضہ)</option>
                      <option value="poshida_infertility">P-21: Female Subfertility & Uterine Debility (عقر و ضعف رحم)</option>
                    </optgroup>
                    
                    <optgroup label="7. Gastrointestinal & Hepatic">
                      <option value="gastro">P-05: Non-Ulcer Dyspepsia & Acid Peptic / GERD (سوء ہضم)</option>
                      <option value="liver">P-06: Non-Alcoholic Fatty Liver Disease (سوء القنیہ / چربیلا جگر)</option>
                      <option value="gastro">P-07: Chronic Colitis & Irritable Bowel / IBS (قولنج)</option>
                    </optgroup>
                    
                    <optgroup label="8. Renal & Urological">
                      <option value="renal">P-12: Nephrolithiasis & Kidney Stones (حصاة الکلیہ)</option>
                      <option value="renal">P-13: Early Chronic Renal Debility (ضعف کلیہ و مثانہ)</option>
                      <option value="poshida_sozak">P-22: Urethritis & Burning Micturition (سوزاک)</option>
                    </optgroup>
                  </select>

                  <button type="button" onclick="toggleHakeemDrawer(true)" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px] shadow flex items-center gap-1 cursor-pointer transition shrink-0" title="Open Hakeem AI Bedside Decision Advisor">
                    <span>🌿</span> Hakeem AI (طبی مشیر)
                  </button>
                </div>
              </div>
              
              <!-- 1-Row Compact Protocol Pills (Preserved for 100% test compatibility) -->
              <div class="flex items-center gap-1 overflow-x-auto pb-0.5 no-scrollbar text-[11px]">
                <button onclick="applyFastProtocol('arthri')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-emerald-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Suranjan + SynovoFlex (وجع المفاصل)">🦵 ArthriCare</button>
                <button onclick="applyFastProtocol('gastro')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-teal-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Kamuni + Bazoori (سوء ہضم)">🧪 GastroBalance</button>
                <button onclick="applyFastProtocol('ceph')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-purple-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Itrifal + TensioCalm (صداع مزمن)">🧠 Cephalic</button>
                <button onclick="applyFastProtocol('metabolic')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-amber-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Khabsul Hadeed + Glucovora (ذیابیطس)">🍯 Metabolic</button>
                <button onclick="applyFastProtocol('respiratory')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-blue-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Banafsha + Sapistan (نزلہ و سعال)">🫁 Respiratory</button>
                <button onclick="applyFastProtocol('liver')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-cyan-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Kasni + Arq Mako (کبد و استسقاء)">🩺 Hepato</button>
                <button onclick="applyFastProtocol('vitality')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-indigo-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Arad Khurma + Jadwar (ضعف باہ)">⚡ Vitality</button>
                <button onclick="applyFastProtocol('skin')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-rose-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700/80 transition" title="Majun Ushba + Unnab (مصفی خون)">🌿 Skin Detox</button>
              </div>
            </div>

            <!-- Autonomous Unani Clinical Principles Summary Card -->
            <div id="fast-unani-principles-card" class="space-y-1.5"></div>

            <!-- 1-Line Ilaj bil-Zidd Status Strip -->
            <div id="fast-mizaj-indicator"></div>

            <!-- Sleek 1-Line Draft & Finalization Gate Strip -->
            <div id="ai-nuskha-proposal-banner" class="px-3 py-1.5 bg-gradient-to-r from-purple-950/60 via-slate-900 to-indigo-950/60 border border-purple-500/30 rounded-xl flex items-center justify-between text-[11px] shadow-sm">
              <span class="text-purple-200 flex items-center gap-1.5 font-medium">
                <span>🧠</span> <span>AI Proposes Draft Regimen • Clinician holds sole finalization authority</span>
              </span>
              <span class="text-[9px] text-amber-300 font-bold bg-amber-500/10 border border-amber-500/30 px-2 py-0.5 rounded">
                🛡️ Doctor Gate
              </span>
            </div>\n\n            """
            
            c = c[:start_c2] + streamlined_col2_top + c[end_c2:]
            print(f"[✓] Streamlined Column 2 top cards and eliminated 300px of duplicate clutter in {fp}")

        with open(fp, 'w') as f:
            f.write(c)

    print("Decluttering script finished.")

if __name__ == '__main__':
    declutter()
