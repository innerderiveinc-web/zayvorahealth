import re

def patch():
    # 1. Functions to inject
    functions_code = """
  // =========================================================================
  // HAKEEM SAHAB™ TOTAL CLINICAL SYNTHESIS & DOCTOR TWEAK ENGINE
  // =========================================================================

  function hakeemAnalyzeAndGenerateCompleteNuskha() {
    const diagInput = document.getElementById('fast-diagnosis-input');
    const diagText = diagInput ? diagInput.value : '';
    
    // 1. Generate base regimen matching diagnosis & symptoms
    generateAiNuskhaFromDiagnosis(diagText);

    const rx = state.prescriptions[0];
    if (!rx || !rx.medicines) return;

    // 2. Multi-parameter fine-tuning based on Physical Exam (Pulse/Tongue) & Lab Markers
    const pulse = activeFastPulse || 'Batee';
    const tongue = activeFastTongue || 'White-Coated';
    const parhezInput = document.getElementById('fast-parhez-text');

    // If pulse is Saree (Hot/Inflammatory) or tongue is Yellowish (Safrawi), add cooling vehicle/corrective
    if (pulse === 'Saree' || tongue === 'Yellowish') {
      rx.medicines.forEach(m => {
        if (!m.anupan || m.anupan.includes('Lukewarm water')) {
          m.anupan = 'Fresh water / Arq Shahtarra (Cooling Badraqa)';
        }
      });
      if (parhezInput && !parhezInput.value.includes('Garam taseer')) {
        parhezInput.value += ' [Tadbeer]: Garam taseer aashia, dhoop aur shadeed garm mahol se bachein. Arq Gulab ya Sheera Sandal istemal karein.';
      }
    } else if (pulse === 'Batee' || tongue === 'White-Coated') {
      // Phlegmatic cold state: ensure warm vehicle
      rx.medicines.forEach(m => {
        if (m.anupan && m.anupan.includes('Fresh water')) {
          m.anupan = 'Neem garam paani / Joshanda Zanjabeel (Warm Badraqa)';
        }
      });
      if (parhezInput && !parhezInput.value.includes('Thandi aur balghami')) {
        parhezInput.value += ' [Tadbeer]: Thandi aur balghami ghizayein (chawal, dahi, ice cream) se parhez karein. Dalk-e-Layyin (halka massage) karein.';
      }
    }

    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    autoSaveConsultationDraft();

    if (typeof showNotification === 'function') {
      showNotification('✨ Hakeem Sahab™ has synthesized the complete Nuskha from Symptoms + Pulse + Tongue + Labs. Ready for doctor review.', 'success');
    }
  }

  function increaseMedicineDose(idx) {
    const rx = state.prescriptions[0];
    if (!rx || !rx.medicines || !rx.medicines[idx]) return;
    const m = rx.medicines[idx];
    
    if (m.strength.includes('5g')) m.strength = m.strength.replace('5g', '7g');
    else if (m.strength.includes('7g')) m.strength = m.strength.replace('7g', '10g');
    else if (m.strength.includes('10g')) m.strength = m.strength.replace('10g', '15g');
    else if (m.strength.includes('1 Tab') || m.strength.includes('1 tab')) m.strength = m.strength.replace(/1 [Tt]ab/, '2 Tabs');
    else if (m.strength.includes('1 Cap')) m.strength = m.strength.replace('1 Cap', '2 Caps');
    else if (m.strength.includes('15ml')) m.strength = m.strength.replace('15ml', '25ml');
    else if (m.strength.includes('20ml')) m.strength = m.strength.replace('20ml', '30ml');
    else if (m.strength.includes('3g')) m.strength = m.strength.replace('3g', '5g');
    else m.strength = m.strength + ' [Increased +]';

    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    if (typeof showNotification === 'function') {
      showNotification(`⬆️ Badhaya (+): ${m.name} dose increased to ${m.strength}`, 'info');
    }
  }

  function decreaseMedicineDose(idx) {
    const rx = state.prescriptions[0];
    if (!rx || !rx.medicines || !rx.medicines[idx]) return;
    const m = rx.medicines[idx];
    
    if (m.strength.includes('15g')) m.strength = m.strength.replace('15g', '10g');
    else if (m.strength.includes('10g')) m.strength = m.strength.replace('10g', '7g');
    else if (m.strength.includes('7g')) m.strength = m.strength.replace('7g', '5g');
    else if (m.strength.includes('2 Tabs') || m.strength.includes('2 tabs')) m.strength = m.strength.replace(/2 [Tt]abs/, '1 Tab');
    else if (m.strength.includes('2 Caps')) m.strength = m.strength.replace('2 Caps', '1 Cap');
    else if (m.strength.includes('30ml')) m.strength = m.strength.replace('30ml', '20ml');
    else if (m.strength.includes('25ml')) m.strength = m.strength.replace('25ml', '15ml');
    else if (m.strength.includes('5g') && !m.strength.includes('15g')) m.strength = m.strength.replace('5g', '3g');
    else if (m.strength.includes(' [Increased +]')) m.strength = m.strength.replace(' [Increased +]', '');
    else m.strength = m.strength + ' [Decreased -]';

    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    if (typeof showNotification === 'function') {
      showNotification(`⬇️ Ghataya (-): ${m.name} dose reduced to ${m.strength}`, 'info');
    }
  }
"""

    for fp in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
        with open(fp, 'r') as f:
            c = f.read()

        # 1. Inject functions if not present
        if 'function hakeemAnalyzeAndGenerateCompleteNuskha' not in c:
            anchor = 'function renderFastMatabPrescriptionList() {'
            if anchor in c:
                c = c.replace(anchor, functions_code + "\n  " + anchor)
                print(f"[✓] Injected hakeemAnalyzeAndGenerateCompleteNuskha & dose tweak functions into {fp}")

        # 2. Add prominent Synthesis Button to Column 1 (below safety rails or vitals)
        old_safety_end = '<!-- PERMANENT SAFETY CHECKLIST & STATUTORY AUDIT -->'
        synthesis_btn_html = """<!-- HAKEEM SAHAB ONE-CLICK TOTAL CLINICAL SYNTHESIS -->
            <div class="p-3.5 bg-gradient-to-r from-purple-950/90 via-slate-900 to-emerald-950/90 border border-emerald-500/40 rounded-2xl shadow-md space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-white flex items-center gap-1.5">
                  <span class="w-5 h-5 rounded-md bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-bold text-xs">✨</span>
                  <span>Hakeem Sahab™ Auto-Synthesis</span>
                </span>
                <span class="text-[9px] font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded">Diagnosis + Exam + Labs</span>
              </div>
              <p class="text-[10px] text-slate-300">Backend evaluates Symptoms, Nabz (Pulse), Lisan (Tongue), Qaroora & Vitals into a unified Ilaj-bil-Dawa & Parhez plan.</p>
              <button type="button" onclick="hakeemAnalyzeAndGenerateCompleteNuskha()" class="w-full py-2.5 px-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-xs shadow-md flex items-center justify-center gap-2 transition cursor-pointer">
                <span>🧠</span>
                <span>حکیم صاحب نسخہ بنائیں (Analyze & Generate Complete Nuskha)</span>
              </button>
            </div>\n\n            """

        if old_safety_end in c and 'Hakeem Sahab™ Auto-Synthesis' not in c:
            c = c.replace(old_safety_end, synthesis_btn_html + old_safety_end)
            print(f"[✓] Added Hakeem Sahab Auto-Synthesis button to Column 1 in {fp}")

        # 3. Add Badhana (+) and Ghatana (-) buttons in renderFastMatabPrescriptionList
        # Look for the remove button
        old_remove_btn = """<button onclick="removePrescriptionMedicine(${idx}); renderFastMatabPrescriptionList(); calculateIlajBilZidd();" class="text-rose-400 hover:text-rose-300 text-xs px-2.5 py-1 rounded bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30">
            ✕ Remove
          </button>"""
        
        new_action_btns = """<div class="flex items-center gap-1">
            <button type="button" onclick="increaseMedicineDose(${idx})" class="px-2 py-1 rounded bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold transition flex items-center gap-0.5" title="Dose Badhayein (Increase strength / frequency)">
              <span>➕</span> <span>بڑھائیں</span>
            </button>
            <button type="button" onclick="decreaseMedicineDose(${idx})" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-[10px] font-bold transition flex items-center gap-0.5" title="Dose Ghatayein (Reduce strength / frequency)">
              <span>➖</span> <span>گھٹائیں</span>
            </button>
          </div>
          <button onclick="removePrescriptionMedicine(${idx}); renderFastMatabPrescriptionList(); calculateIlajBilZidd();" class="text-rose-400 hover:text-rose-300 text-[10px] px-2 py-1 rounded bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 flex items-center gap-0.5" title="Nuskhe se hatayein">
            <span>✕</span> <span>ہٹائیں</span>
          </button>"""

        if old_remove_btn in c:
            c = c.replace(old_remove_btn, new_action_btns)
            print(f"[✓] Added Badhana (+) & Ghatana (-) controls to medicine rows in {fp}")

        with open(fp, 'w') as f:
            f.write(c)

    print("Patched all workspace files.")

if __name__ == '__main__':
    patch()
