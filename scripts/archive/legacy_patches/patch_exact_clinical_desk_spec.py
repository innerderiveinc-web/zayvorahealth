import re

def patch():
    snippet_code = """
  function insertClinicalSnippet(type) {
    const el = document.getElementById('input-comprehensive-clinical-note') || document.getElementById('fast-clinical-narrative');
    if (!el) return;
    let snippet = '';
    if (type === 'exam') {
      snippet = '\\n[معائنۂ نبض و زبان]: Nabz: Batee (Slow/Cold / بارد) | Lisan: White-coated (بلغم) | Qaroora: Pale Clear.';
    } else if (type === 'labs') {
      snippet = '\\n[لیب ٹیسٹ]: Fasting Glucose: 110 mg/dL | HbA1c: 6.2% | Uric Acid: 8.4 mg/dL | hs-CRP: 4.8 mg/L.';
    } else if (type === 'imaging') {
      snippet = '\\n[الٹراساؤنڈ و ایکسرے]: Ultrasound Abdomen: Mild hepatic steatosis (Fatty Liver Grade 1). Bilateral renal calculi nil.';
    }
    el.value = (el.value ? el.value.trim() + ' ' : '') + snippet;
    el.focus();
    if (typeof showNotification === 'function') {
      showNotification('Inserted clinical findings snippet template.', 'info');
    }
  }
"""

    for fp in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
        with open(fp, 'r') as f:
            c = f.read()

        # 1. Update hakeemSynthesizeFromClinicalNarrative to check input-comprehensive-clinical-note
        c = c.replace(
            "const textEl = document.getElementById('fast-clinical-narrative');",
            "const textEl = document.getElementById('input-comprehensive-clinical-note') || document.getElementById('fast-clinical-narrative');"
        )
        c = c.replace(
            "const textEl = document.getElementById('fast-clinical-narrative');\n    if (!('webkitSpeechRecognition'",
            "const textEl = document.getElementById('input-comprehensive-clinical-note') || document.getElementById('fast-clinical-narrative');\n    if (!('webkitSpeechRecognition'"
        )

        # 2. Inject snippet function if not present
        if 'function insertClinicalSnippet' not in c:
            anchor = 'function hakeemSynthesizeFromClinicalNarrative'
            c = c.replace(anchor, snippet_code + "\n  " + anchor)
            print(f"[✓] Added insertClinicalSnippet to {fp}")

        # 3. Update textarea and snippet buttons in Column 1
        old_card_hdr = '<div class="flex items-center gap-1.5">\n                  <button type="button" onclick="startClinicalNarrativeDictation()"'
        new_card_hdr = """<div class="flex items-center gap-1.5 flex-wrap">
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
                </div>"""
        
        # Replace header buttons
        old_full_hdr = """<div class="flex items-center gap-1.5">
                  <button type="button" onclick="startClinicalNarrativeDictation()" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-teal-300 border border-slate-700 text-[10px] font-bold transition flex items-center gap-1 cursor-pointer" title="Speak patient history & findings">
                    <span>🎤</span> <span>Dictate</span>
                  </button>
                  <button type="button" onclick="document.getElementById('fast-clinical-narrative').value=''; document.getElementById('fast-clinical-narrative').focus();" class="px-1.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 text-[10px] font-bold" title="Clear text">
                    ✕
                  </button>
                </div>"""

        if old_full_hdr in c:
            c = c.replace(old_full_hdr, new_card_hdr)
            print(f"[✓] Replaced header buttons with snippet chips in {fp}")

        # Ensure textarea has id="input-comprehensive-clinical-note" and data-alias
        old_textarea = '<textarea id="fast-clinical-narrative" rows="5" onkeydown="if(event.ctrlKey && event.key===\'Enter\'){ hakeemSynthesizeFromClinicalNarrative(this.value); }"'
        new_textarea = '<textarea id="input-comprehensive-clinical-note" name="fast-clinical-narrative" rows="5" onkeydown="if((event.ctrlKey||event.metaKey) && event.key===\'Enter\'){ hakeemSynthesizeFromClinicalNarrative(this.value); }"'
        if old_textarea in c:
            c = c.replace(old_textarea, new_textarea)
            print(f"[✓] Renamed textarea to input-comprehensive-clinical-note in {fp}")

        # Update primary button label to ⚡ Hakeem Sahab™ AI: Generate Comprehensive Nuskha
        old_btn = '<span>حکیم صاحب تجزیہ کریں اور نسخہ بنائیں (Analyze &amp; Generate Nuskha)</span>'
        new_btn = '<span>⚡ Hakeem Sahab™ AI: Generate Comprehensive Nuskha (Ctrl+Enter)</span>'
        if old_btn in c:
            c = c.replace(old_btn, new_btn)
            print(f"[✓] Updated AI synthesis button label in {fp}")

        # Update accordion summary title
        old_acc = '<span>Optional Diagnostic Tools, Physical Exam &amp; Quick Chips (اختیاری اوزار)</span>'
        new_acc = '<span>🛠️ تفصیلی تشخیصی ٹولز (اختیاری) — Pulse Presets, Dominant Mizaj, ICD-11 &amp; Detailed Tashkhees</span>'
        if old_acc in c:
            c = c.replace(old_acc, new_acc)
            print(f"[✓] Updated accordion title to Urdu/English exact title in {fp}")

        # 4. Update dose steppers in renderFastMatabPrescriptionList: [ - ] strength [ + ]
        old_dose_display = """<p class="text-[11px] text-slate-300">
            Dose: <strong class="text-amber-300 font-mono">${m.strength}</strong> • 
            Timing: <span>☀️ ${m.morning || '—'} | ⛅ ${m.noon || '—'} | 🌙 ${m.night || '—'}</span>
          </p>"""
        
        new_dose_display = """<div class="flex items-center gap-2 flex-wrap pt-0.5">
            <div class="inline-flex items-center gap-1 bg-slate-800/90 px-2 py-0.5 rounded-lg border border-slate-700/80">
              <span class="text-[10px] text-slate-400 font-medium">Dose:</span>
              <button type="button" onclick="decreaseMedicineDose(${idx})" class="w-4 h-4 rounded bg-slate-900 hover:bg-slate-700 text-slate-300 hover:text-white font-black text-xs flex items-center justify-center transition cursor-pointer" title="Dose Ghatayein (-)">−</button>
              <strong class="text-amber-300 font-mono text-[11px] px-1">${m.strength}</strong>
              <button type="button" onclick="increaseMedicineDose(${idx})" class="w-4 h-4 rounded bg-slate-900 hover:bg-emerald-600 text-slate-300 hover:text-white font-black text-xs flex items-center justify-center transition cursor-pointer" title="Dose Badhayein (+)">+</button>
            </div>
            <span class="text-[10px] text-slate-400">☀️ ${m.morning || '—'} | ⛅ ${m.noon || '—'} | 🌙 ${m.night || '—'}</span>
          </div>"""
        
        if old_dose_display in c:
            c = c.replace(old_dose_display, new_dose_display)
            print(f"[✓] Enhanced inline dose steppers in {fp}")

        with open(fp, 'w') as f:
            f.write(c)

    print("Complete.")

if __name__ == '__main__':
    patch()
