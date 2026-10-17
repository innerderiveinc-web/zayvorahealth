import re

narrative_function = """
  // =========================================================================
  // UNIFIED CLINICAL NARRATIVE PARSER & AI SYNTHESIS ENGINE
  // =========================================================================

  function hakeemSynthesizeFromClinicalNarrative(narrativeText) {
    const textEl = document.getElementById('fast-clinical-narrative');
    const narrative = (narrativeText || (textEl ? textEl.value : '')).trim();
    if (!narrative) {
      if (textEl) textEl.focus();
      return;
    }

    const lower = narrative.toLowerCase();

    // 1. Detect Chief Diagnosis from narrative
    let detectedDiag = '';
    if (lower.includes('knee') || lower.includes('joint') || lower.includes('waja') || lower.includes('osteo') || lower.includes('arthritis') || lower.includes('gout') || lower.includes('uric acid') || lower.includes('niqris')) {
      detectedDiag = 'Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)';
    } else if (lower.includes('fatty liver') || lower.includes('jigar') || lower.includes('liver') || lower.includes('sgpt') || lower.includes('steatosis') || lower.includes('jaundice') || lower.includes('yarqan')) {
      detectedDiag = 'Su-e-Qinya & Warm-e-Jigar (Non-Alcoholic Fatty Liver / سوء القنیہ)';
    } else if (lower.includes('stone') || lower.includes('calculi') || lower.includes('kidney') || lower.includes('hisat') || lower.includes('pathri') || lower.includes('renal')) {
      detectedDiag = 'Hisat-e-Kulya (Renal Nephrolithiasis / حصاة الکلیہ)';
    } else if (lower.includes('asthma') || lower.includes('dama') || lower.includes('zeeq') || lower.includes('cough') || lower.includes('bronch') || lower.includes('respir')) {
      detectedDiag = 'Zeequn-Nafs Shuabi (Bronchial Asthma / ضیق النفس شعبی)';
    } else if (lower.includes('piles') || lower.includes('bawaseer') || lower.includes('hemorrhoid') || lower.includes('bleeding')) {
      detectedDiag = 'Bawaseer Damiya & Riyah (Hemorrhoidal Disease / بواسیر)';
    } else if (lower.includes('sciatica') || lower.includes('irq') || lower.includes('disc') || lower.includes('lumbago')) {
      detectedDiag = 'Irq-un-Nasa (Lumbar Sciatica & Spondylosis / عرق النساء)';
    } else if (lower.includes('sugar') || lower.includes('diabet') || lower.includes('hba1c') || lower.includes('glucose') || lower.includes('ziabetus')) {
      detectedDiag = 'Ziabetus Shakari Type 2 (Metabolic Syndrome / ذیابیطس شکری)';
    } else if (lower.includes('bp') || lower.includes('hypertens') || lower.includes('pressure') || lower.includes('zaght')) {
      detectedDiag = 'Zaght-ud-Dam Qawi (Essential Hypertension / ضغط الدم قوی)';
    } else if (lower.includes('pcos') || lower.includes('period') || lower.includes('menses') || lower.includes('haiz') || lower.includes('tams') || lower.includes('uterus')) {
      detectedDiag = 'Usr-e-Tams & PCOS (Polycystic Ovarian Syndrome / عسر الطمث)';
    } else if (lower.includes('sailan') || lower.includes('leucorrh') || lower.includes('safed pani') || lower.includes('white discharge')) {
      detectedDiag = 'Sailan-ur-Rahm (Chronic Leucorrhea / سیلان الرحم)';
    } else if (lower.includes('surat') || lower.includes('inzal') || lower.includes('mani') || lower.includes('jariyan') || lower.includes('vitality') || lower.includes('bah')) {
      detectedDiag = 'Surat-e-Inzal & Zof-e-Bah (Andrological Vitality Debility / ضعف باہ)';
    } else if (lower.includes('insomnia') || lower.includes('sahar') || lower.includes('sleep') || lower.includes('neend')) {
      detectedDiag = 'Sahar & Malikhuliya (Chronic Insomnia / سہر مزمن)';
    } else if (lower.includes('eczema') || lower.includes('skin') || lower.includes('rash') || lower.includes('jild') || lower.includes('khujli') || lower.includes('alopecia') || lower.includes('hair fall')) {
      detectedDiag = 'Amraz-e-Jild & Quba (Chronic Dermatosis / امراض جلد)';
    } else if (lower.includes('gas') || lower.includes('hazm') || lower.includes('dyspep') || lower.includes('pet') || lower.includes('gerd') || lower.includes('colitis')) {
      detectedDiag = 'Su-e-Hazm & Nafkh (Gastric Dyspepsia & Colitis / سوء ہضم)';
    } else {
      detectedDiag = narrative.split('.')[0].slice(0, 70);
    }

    // Update diagnosis field
    const diagInput = document.getElementById('fast-diagnosis-input');
    if (diagInput) diagInput.value = detectedDiag;

    // 2. Synthesize formulations
    generateAiNuskhaFromDiagnosis(detectedDiag || narrative);

    const rx = state.prescriptions[0];
    if (!rx || !rx.medicines) return;

    // 3. Check physical examination findings from text
    let isRapidHot = lower.includes('saree') || lower.includes('rapid') || lower.includes('tachy') || lower.includes('yellow') || lower.includes('safra');
    let isSlowCold = lower.includes('batee') || lower.includes('slow') || lower.includes('brady') || lower.includes('white') || lower.includes('balgham');

    if (isRapidHot) {
      rx.medicines.forEach(m => {
        if (!m.anupan || m.anupan.includes('Lukewarm water')) {
          m.anupan = 'Fresh water / Arq Shahtarra (Cooling Badraqa)';
        }
      });
    } else if (isSlowCold) {
      rx.medicines.forEach(m => {
        if (m.anupan && m.anupan.includes('Fresh water')) {
          m.anupan = 'Neem garam paani / Joshanda Zanjabeel (Warm Badraqa)';
        }
      });
    }

    // 4. Incorporate Lab & Radiology findings into Parhez & Tadbir
    const parhezInput = document.getElementById('fast-parhez-text');
    let parhezAdditions = [];

    if (lower.includes('uric acid') || lower.includes('gout')) {
      parhezAdditions.push('Purine rich ghizayein (gosht, daalein, tamatar, palak) se sakht parhez. Rozana 3L paani.');
    }
    if (lower.includes('hba1c') || lower.includes('sugar') || lower.includes('glucose')) {
      parhezAdditions.push('Meethi aashia, chawal, aalo aur refined sugar band karein.');
    }
    if (lower.includes('crp') || lower.includes('esr') || lower.includes('inflammation')) {
      parhezAdditions.push('Warm fomentation (Takmeed) karein, shadeed dhoop aur tili cheezon se parhez.');
    }
    if (lower.includes('ultrasound') || lower.includes('fatty liver') || lower.includes('sgpt')) {
      parhezAdditions.push('Oily/fried khano se mukammal parhez, anar ka ras aur subah 30 min brisk walk.');
    }
    if (lower.includes('x-ray') || lower.includes('osteoarthritis') || lower.includes('disc')) {
      parhezAdditions.push('Chokri mar kar na bethein, western commode istemal karein, Roghan Suranjan se halka massage karein.');
    }

    if (parhezInput && parhezAdditions.length > 0) {
      parhezInput.value = (parhezInput.value ? parhezInput.value + ' | ' : '') + parhezAdditions.join(' | ');
    }

    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    autoSaveConsultationDraft();

    if (typeof showNotification === 'function') {
      showNotification(`✨ Hakeem Sahab™ analyzed history, physical exam & diagnostics. Generated Nuskha for "${detectedDiag}". Review active.`, 'success');
    }
  }

  function startClinicalNarrativeDictation() {
    const textEl = document.getElementById('fast-clinical-narrative');
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      if (typeof showNotification === 'function') {
        showNotification('Speech dictation requires Google Chrome or Chromium browser.', 'warning');
      }
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    if (typeof showNotification === 'function') {
      showNotification('🎤 Listening... Speak patient history, symptoms, physical exam and lab findings.', 'info');
    }

    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      if (textEl) {
        textEl.value = (textEl.value ? textEl.value + ' ' : '') + transcript;
        hakeemSynthesizeFromClinicalNarrative(textEl.value);
      }
    };
    recognition.onerror = function(err) {
      if (typeof showNotification === 'function') {
        showNotification('Voice dictation error: ' + err.error, 'error');
      }
    };
    recognition.start();
  }
"""

new_col1_html = """          <!-- COLUMN 1 (5 cols): Streamlined Clinical Narrative & Intake Pad -->
          <div class="lg:col-span-5 space-y-4 text-xs">
            
            <!-- Unified Clinical Narrative Intake Card -->
            <div class="bg-[var(--card)] border border-emerald-500/30 rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-bold text-xs">📋</span>
                  <span class="font-bold text-white text-xs">Patient Clinical Encounter &amp; History (تفصیلی تاریخِ مریض)</span>
                </div>
                <div class="flex items-center gap-1.5">
                  <button type="button" onclick="startClinicalNarrativeDictation()" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-teal-300 border border-slate-700 text-[10px] font-bold transition flex items-center gap-1 cursor-pointer" title="Speak patient history & findings">
                    <span>🎤</span> <span>Dictate</span>
                  </button>
                  <button type="button" onclick="document.getElementById('fast-clinical-narrative').value=''; document.getElementById('fast-clinical-narrative').focus();" class="px-1.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 text-[10px] font-bold" title="Clear text">
                    ✕
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-[10px] font-bold text-slate-400 mb-1">
                  History, Symptoms, Physical Exam (Nabz/Tongue), Labs &amp; Radiology:
                </label>
                <textarea id="fast-clinical-narrative" rows="5" onkeydown="if(event.ctrlKey && event.key==='Enter'){ hakeemSynthesizeFromClinicalNarrative(this.value); }" class="w-full p-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-sans leading-relaxed transition" placeholder="Write or dictate everything the patient reports, physical exam (Nabz, Tongue), lab findings (Blood sugar, CRP, Uric Acid), and radiology reports (Ultrasound, X-ray)... Press Enter or click button below to compile Nuskha.">52M presenting with chronic bilateral knee pain with morning stiffness for 6 months. High uric acid 8.4 mg/dL and hs-CRP 4.8 mg/L. Knee X-ray shows Grade 2 Osteoarthritis. Pulse slow (Batee / بارد), tongue white-coated (Balghami).</textarea>
              </div>

              <!-- Main Synthesis Button -->
              <button type="button" onclick="hakeemSynthesizeFromClinicalNarrative(document.getElementById('fast-clinical-narrative').value)" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-xs shadow-md flex items-center justify-center gap-2 transition cursor-pointer transform hover:scale-[1.01]">
                <span>✨</span>
                <span>حکیم صاحب تجزیہ کریں اور نسخہ بنائیں (Analyze &amp; Generate Nuskha)</span>
              </button>

              <!-- Extracted Diagnosis Preview -->
              <div class="pt-1 flex items-center gap-2">
                <span class="text-[10px] text-slate-400 font-bold whitespace-nowrap">Diagnosis:</span>
                <input id="fast-diagnosis-input" type="text" onchange="generateAiNuskhaFromDiagnosis(this.value)" onkeydown="if(event.key==='Enter'){event.preventDefault();generateAiNuskhaFromDiagnosis(this.value);}" class="flex-1 px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-emerald-300 text-xs font-semibold outline-none focus:border-emerald-500" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">
              </div>
            </div>

            <!-- Tucked-Away Diagnostic Tools & Physical Exam (Accordion / Dropdown) -->
            <details class="bg-[var(--card)] border border-slate-800 rounded-2xl p-3 text-xs group transition shadow-sm">
              <summary class="cursor-pointer font-bold text-slate-300 hover:text-emerald-400 flex items-center justify-between select-none py-1">
                <span class="flex items-center gap-1.5">
                  <span>🛠️</span>
                  <span>Optional Diagnostic Tools, Physical Exam &amp; Quick Chips (اختیاری اوزار)</span>
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

          </div>\n\n"""

for fp in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
    with open(fp, 'r') as f:
        c = f.read()

    # 1. Inject narrative function
    if 'function hakeemSynthesizeFromClinicalNarrative' not in c:
        anchor_fn = 'function renderFastMatabPrescriptionList() {'
        if anchor_fn in c:
            c = c.replace(anchor_fn, narrative_function + "\n  " + anchor_fn)
            print(f"[✓] Injected narrative engine into {fp}")

    # 2. Replace Column 1 with new simplified Column 1
    col1_anchor_start = '<!-- COLUMN 1 (5 cols): Diagnostic & Classical Tashkhees Pad -->'
    col2_anchor = '<!-- COLUMN 2 (7 cols): 1-Click Fast Protocols, Nuskha Pad & Action -->'

    start_idx = c.find(col1_anchor_start)
    end_idx = c.find(col2_anchor)

    if start_idx != -1 and end_idx != -1:
        c = c[:start_idx] + new_col1_html + c[end_idx:]
        print(f"[✓] Replaced Column 1 with simplified Clinical Encounter box and folded tools accordion in {fp}")
    else:
        print(f"[!] Column boundaries not found in {fp}: start={start_idx}, end={end_idx}")

    with open(fp, 'w') as f:
        f.write(c)

print("Patching complete.")
