import re

def build_perfect_desk():
    # 1. Read base clean files
    with open('js/zayvora-core.js', 'r') as f:
        core = f.read()

    # Define the complete, clean, elegant 2-column desk HTML
    clean_desk_html = """        <!-- 2-COLUMN CLUTTER-FREE MATAB WORKDESK -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          
          <!-- COLUMN 1 (5 cols): Master Clinical Intake & Findings -->
          <div class="lg:col-span-5 space-y-4 text-xs">
            
            <!-- Unified Clinical Narrative Intake Card -->
            <div class="bg-[var(--card)] border border-emerald-500/30 rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-bold text-xs">📋</span>
                  <span class="font-bold text-white text-xs">Doctor's Clinical Notes (مریض کی ہسٹری و معائنہ)</span>
                </div>
                <div class="flex items-center gap-1.5 flex-wrap">
                  <button type="button" onclick="startClinicalNarrativeDictation()" class="px-2 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px] shadow flex items-center gap-1 cursor-pointer transition" title="Speak patient history & findings">
                    <span>🎤</span> <span>Voice Dictate</span>
                  </button>
                  <button type="button" onclick="insertClinicalSnippet('exam')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-teal-300 border border-slate-700 text-[10px] font-medium transition cursor-pointer" title="Insert Pulse & Tongue template">
                    + نبض و بول
                  </button>
                  <button type="button" onclick="insertClinicalSnippet('labs')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700 text-[10px] font-medium transition cursor-pointer" title="Insert Labs template">
                    + لیب ٹیسٹ
                  </button>
                  <button type="button" onclick="insertClinicalSnippet('imaging')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 text-[10px] font-medium transition cursor-pointer" title="Insert Ultrasound/X-ray template">
                    + الٹراساؤنڈ
                  </button>
                  <button type="button" onclick="(document.getElementById('input-comprehensive-clinical-note')||document.getElementById('fast-clinical-narrative')).value=''; (document.getElementById('input-comprehensive-clinical-note')||document.getElementById('fast-clinical-narrative')).focus();" class="px-1.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 text-[10px] font-bold" title="Clear text">
                    ✕
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-[10px] font-bold text-slate-400 mb-1">
                  History, Symptoms, Physical Exam (Nabz/Tongue), Labs &amp; Radiology:
                </label>
                <textarea id="input-comprehensive-clinical-note" name="fast-clinical-narrative" rows="6" onkeydown="if((event.ctrlKey||event.metaKey) && event.key==='Enter'){ hakeemSynthesizeFromClinicalNarrative(this.value); }" class="w-full p-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-sans leading-relaxed transition" placeholder="Write or dictate everything the patient reports, physical exam (Nabz, Tongue), lab findings (Blood sugar, CRP, Uric Acid), and radiology reports (Ultrasound, X-ray)... Press Enter or click button below to compile Nuskha.">52M presenting with chronic bilateral knee pain with morning stiffness for 6 months. High uric acid 8.4 mg/dL and hs-CRP 4.8 mg/L. Knee X-ray shows Grade 2 Osteoarthritis. Pulse slow (Batee / بارد), tongue white-coated (Balghami).</textarea>
              </div>

              <!-- Main Synthesis Button -->
              <button type="button" onclick="hakeemSynthesizeFromClinicalNarrative()" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-xs shadow-md flex items-center justify-center gap-2 transition cursor-pointer transform hover:scale-[1.01]">
                <span>⚡</span>
                <span>Hakeem Sahab™ AI: Generate Comprehensive Nuskha (Ctrl+Enter)</span>
              </button>

              <!-- Extracted Diagnosis Preview -->
              <div class="pt-1 flex items-center gap-2">
                <span class="text-[10px] text-slate-400 font-bold whitespace-nowrap">Diagnosis:</span>
                <input id="fast-diagnosis-input" type="text" onchange="generateAiNuskhaFromDiagnosis(this.value)" onkeydown="if(event.key==='Enter'){event.preventDefault();generateAiNuskhaFromDiagnosis(this.value);}" placeholder="Type any disease in English, Urdu or Roman Urdu..." class="flex-1 px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-emerald-300 text-xs font-semibold outline-none focus:border-emerald-500" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">
              </div>
            </div>

            <!-- Tucked-Away Diagnostic Tools & Physical Exam (Accordion / Dropdown) -->
            <details class="bg-[var(--card)] border border-slate-800 rounded-2xl p-3 text-xs group transition shadow-sm">
              <summary class="cursor-pointer font-bold text-slate-300 hover:text-emerald-400 flex items-center justify-between select-none py-1">
                <span class="flex items-center gap-1.5">
                  <span>🛠️</span>
                  <span>تفصیلی تشخیصی ٹولز (اختیاری) — Pulse Presets, Dominant Mizaj, ICD-11 &amp; Detailed Tashkhees</span>
                </span>
                <span class="text-[10px] text-slate-500 font-mono group-open:rotate-180 transition">▼</span>
              </summary>

              <div class="mt-3 space-y-3 pt-2 border-t border-slate-800/80">
                
                <!-- Quick Complaint Chips -->
                <div class="space-y-1.5">
                  <span class="text-[10px] text-slate-400 font-bold block">1-Click Quick Complaints:</span>
                  <div class="flex flex-wrap gap-1.5">
                    <button onclick="selectFastComplaint('Waja-ul-Mafasil', 'Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)')" data-complaint="Waja-ul-Mafasil" class="fast-complaint-chip px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-bold text-[11px] shadow">🦵 Waja-ul-Mafasil</button>
                    <button onclick="selectFastComplaint('Su-e-Hazm', 'Su-e-Hazm & Nafkh (Gastric Dyspepsia / سوء ہضم)')" data-complaint="Su-e-Hazm" class="fast-complaint-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-medium text-[11px]">🧪 Su-e-Hazm</button>
                    <button onclick="selectFastComplaint('Suda', 'Suda-e-Muzmin & Shaqeeqa (Chronic Cephalalgia / صداع مزمن)')" data-complaint="Suda" class="fast-complaint-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-medium text-[11px]">🧠 Suda / Migraine</button>
                    <button onclick="selectFastComplaint('Ziabetus', 'Ziabetus Shakari Type 2 (Metabolic Support / ذیابیطس)')" data-complaint="Ziabetus" class="fast-complaint-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-medium text-[11px]">🍯 Ziabetus</button>
                    <button onclick="selectFastComplaint('Zof-e-Bah', 'Zof-e-Bah & Taqwiyat-e-Asab (Neuro-Andrological / ضعف باہ)')" data-complaint="Zof-e-Bah" class="fast-complaint-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-medium text-[11px]">⚡ Zof-e-Bah</button>
                  </div>
                </div>

                <!-- Classical Tashkhees (Nabz, Lisan, Qaroora) -->
                <div class="space-y-2 pt-2 border-t border-slate-800 text-[10px]">
                  <span class="text-slate-400 font-bold block">Physical Exam Chips (Pulse, Tongue, Urine):</span>
                  
                  <!-- Nabz -->
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span class="text-slate-400">Nabz:</span>
                    <button onclick="selectFastTashkhees('pulse', 'Batee')" data-val="Batee" class="fast-pulse-chip px-2 py-0.5 rounded bg-teal-600 text-white font-bold text-[10px]">Batee (Slow)</button>
                    <button onclick="selectFastTashkhees('pulse', 'Saree')" data-val="Saree" class="fast-pulse-chip px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Saree (Rapid)</button>
                    <button onclick="selectFastTashkhees('pulse', 'Motadil')" data-val="Motadil" class="fast-pulse-chip px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Motadil (Normal)</button>
                  </div>

                  <!-- Lisan -->
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span class="text-slate-400">Lisan:</span>
                    <button onclick="selectFastTashkhees('tongue', 'White-Coated')" data-val="White-Coated" class="fast-tongue-chip px-2 py-0.5 rounded bg-teal-600 text-white font-bold text-[10px]">White Slimy</button>
                    <button onclick="selectFastTashkhees('tongue', 'Yellowish')" data-val="Yellowish" class="fast-tongue-chip px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Yellowish</button>
                    <button onclick="selectFastTashkhees('tongue', 'Normal')" data-val="Normal" class="fast-tongue-chip px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Normal Pink</button>
                  </div>

                  <!-- Qaroora -->
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span class="text-slate-400">Qaroora:</span>
                    <button onclick="selectFastTashkhees('urine', 'Pale Clear')" data-val="Pale Clear" class="fast-urine-chip px-2 py-0.5 rounded bg-teal-600 text-white font-bold text-[10px]">Pale Clear</button>
                    <button onclick="selectFastTashkhees('urine', 'Yellowish')" data-val="Yellowish" class="fast-urine-chip px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Yellow Sub-bilious</button>
                    <button onclick="selectFastTashkhees('urine', 'Mukaddar')" data-val="Mukaddar" class="fast-urine-chip px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Turbid</button>
                  </div>
                </div>

                <!-- Modern Vitals -->
                <div class="grid grid-cols-3 gap-1.5 pt-2 border-t border-slate-800 text-[9px]">
                  <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                    <span class="text-slate-400 block">BP:</span>
                    <strong class="text-white">128/82 mmHg</strong>
                  </div>
                  <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                    <span class="text-slate-400 block">HR:</span>
                    <strong class="text-white">72 bpm</strong>
                  </div>
                  <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                    <span class="text-slate-400 block">hs-CRP:</span>
                    <strong class="text-cyan-400">4.8 mg/L</strong>
                  </div>
                </div>

                <!-- Safety Checklist -->
                <div class="grid grid-cols-2 gap-1.5 pt-1 text-[9px]">
                  <div class="p-1.5 rounded bg-[var(--background)] border border-emerald-500/20 flex justify-between">
                    <span class="text-slate-400">Renal/GI:</span>
                    <span class="text-emerald-400 font-bold">NORMAL ✓</span>
                  </div>
                  <div class="p-1.5 rounded bg-[var(--background)] border border-emerald-500/20 flex justify-between">
                    <span class="text-slate-400">Herb-Drug:</span>
                    <span class="text-emerald-400 font-bold">0 KHATRA ✓</span>
                  </div>
                </div>

              </div>
            </details>

          </div>

          <!-- COLUMN 2 (7 cols): Prescription Review Pad & Actions -->
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
            </div>

            <!-- Active Prescribed Formulations List -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex justify-between items-center border-b border-[var(--border)] pb-2.5">
                <span class="font-bold text-white text-xs flex items-center gap-1.5">
                  <span>℞</span> Active Nuskha &amp; Formulations Table
                </span>
                <div class="flex items-center gap-2 flex-wrap">
                  <button onclick="openQarabadeenCatalogModal()" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] rounded-lg transition" title="Search all 59 Classical Formulations">
                    + Qarabadeen
                  </button>
                  <button onclick="openZayvoraProductsModal()" class="px-2.5 py-1 bg-amber-600 hover:bg-amber-500 text-white font-bold text-[11px] rounded-lg transition" title="Search all 32 ZAYVORA Sovereign Formulations">
                    + ZAYVORA
                  </button>
                  <button onclick="openSelfNuskhaModal()" class="px-2.5 py-1 bg-purple-600 hover:bg-purple-500 text-white font-bold text-[11px] rounded-lg transition">
                    + Self-Nuskha
                  </button>
                </div>
              </div>

              <!-- Fast Inline Medicine Search Input -->
              <div class="relative">
                <div class="relative">
                  <input id="fast-med-quick-input" type="text" placeholder="🔍 Dawa dhoondein (e.g. Khamira, Majun, Itrifal, Sharbat, Safuf)..." oninput="handleFastMedSearch(this.value)" onfocus="handleFastMedSearch(this.value)" class="w-full pl-8 pr-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-medium">
                  <span class="absolute left-2.5 top-2.5 text-xs text-slate-400">🔍</span>
                </div>
                <div id="fast-med-search-results" class="hidden absolute left-0 right-0 top-full mt-1 bg-slate-900 border border-emerald-500/40 rounded-xl shadow-2xl max-h-56 overflow-y-auto z-40 p-1 space-y-1">
                </div>
              </div>

              <!-- Prescription Items List -->
              <div id="fast-prescriptions-list" class="space-y-2">
                <!-- Rendered dynamically -->
              </div>
            </div>

            <!-- Parhez & Tadbeer Note Pad -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-2">
              <span class="text-xs font-bold text-white block">پرہیز و غذائی ہدایات (Dietary Restrictions &amp; Parhez)</span>
              <textarea id="fast-parhez-text" rows="2" class="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 text-xs outline-none focus:border-emerald-500" placeholder="Dietary restrictions and lifestyle instructions..."></textarea>
            </div>

            <!-- Bottom Finalization Actions -->
            <div class="flex items-center justify-between pt-2">
              <div class="flex items-center gap-2">
                <button onclick="openBilingualPrescriptionSlipModal()" class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-bold text-xs shadow-sm transition flex items-center gap-1.5 cursor-pointer">
                  <span>🖨️</span> <span>Patient Slip</span>
                </button>
                <button onclick="sendRxViaWhatsApp()" class="px-3 py-2 rounded-xl bg-teal-800/80 hover:bg-teal-700 border border-teal-700 text-white font-bold text-xs shadow-sm transition flex items-center gap-1.5 cursor-pointer">
                  <span>📲</span> <span>WhatsApp</span>
                </button>
              </div>

              <button onclick="completeConsultation()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-xs shadow-lg transition flex items-center gap-2 cursor-pointer transform hover:scale-[1.01]">
                <span>🔒</span> <span>Sign &amp; Lock (21 CFR 11)</span>
              </button>
            </div>

          </div>
        </div>"""

    # Replace the entire desk section cleanly between the Consultation Desk Header and end of desk HTML
    desk_start_anchor = '<div class="grid grid-cols-1 lg:grid-cols-12 gap-5">'
    desk_end_anchor = '</div>\n      </div>\n    `;\n  }'

    # Check in core
    s_idx = core.find(desk_start_anchor)
    e_idx = core.find(desk_end_anchor, s_idx)

    if s_idx != -1 and e_idx != -1:
        core_new = core[:s_idx] + clean_desk_html + core[e_idx + len('</div>\n      </div>'):]
        with open('js/zayvora-core.js', 'w') as f:
            f.write(core_new)
        print('[✓] Successfully installed clean, clutter-free desk into js/zayvora-core.js')
    else:
        print(f'[!] Could not find desk boundaries in js/zayvora-core.js: s={s_idx}, e={e_idx}')

    # Repeat for 02-clinical-workspace.js
    with open('js/modules/02-clinical-workspace.js', 'r') as f:
        mod = f.read()

    ms_idx = mod.find(desk_start_anchor)
    me_idx = mod.find(desk_end_anchor, ms_idx)

    if ms_idx != -1 and me_idx != -1:
        mod_new = mod[:ms_idx] + clean_desk_html + mod[me_idx + len('</div>\n      </div>'):]
        with open('js/modules/02-clinical-workspace.js', 'w') as f:
            f.write(mod_new)
        print('[✓] Successfully installed clean, clutter-free desk into js/modules/02-clinical-workspace.js')
    else:
        print(f'[!] Could not find desk boundaries in js/modules/02-clinical-workspace.js: s={ms_idx}, e={me_idx}')

if __name__ == '__main__':
    build_perfect_desk()
