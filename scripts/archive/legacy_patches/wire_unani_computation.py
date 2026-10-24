import re

unani_functions = """
  // =========================================================================
  // UNANI CLINICAL COMPUTATIONAL INTELLIGENCE & DOSE STEPPERS
  // =========================================================================

  function calculateAutonomousUnaniPrinciples(narrative, detectedDiag) {
    const text = ((narrative || '') + ' ' + (detectedDiag || '')).toLowerCase();
    
    // 1. MIZAJ & SU-E-MIZAJ CALCULATION (4 Humors & Dyscrasia)
    let mizajDeviation = 'Su-e-Mizaj Barid Balghami (Cold-Phlegmatic / سوء مزاج بارد بلغمی)';
    let baselineMizaj = 'Balghami (Phlegmatic)';
    let percentages = { damawi: 20, balghami: 55, safrawi: 15, sawdawi: 10 };

    if (text.includes('saree') || text.includes('yellow') || text.includes('safra') || text.includes('burning') || text.includes('fever') || text.includes('acid') || text.includes('bile') || text.includes('piles') || text.includes('sozak')) {
      mizajDeviation = 'Su-e-Mizaj Haar Safrawi (Hot-Bilious / سوء مزاج حار صفراوی)';
      baselineMizaj = 'Safrawi (Bilious / Choleric)';
      percentages = { damawi: 20, balghami: 10, safrawi: 60, sawdawi: 10 };
    } else if (text.includes('bp') || text.includes('hypertens') || text.includes('pressure') || text.includes('zaght') || text.includes('headache') || text.includes('shaqeeqa') || text.includes('damawi')) {
      mizajDeviation = 'Su-e-Mizaj Haar Damawi (Hot-Sanguine / سوء مزاج حار دموی)';
      baselineMizaj = 'Damawi (Sanguine)';
      percentages = { damawi: 58, balghami: 18, safrawi: 14, sawdawi: 10 };
    } else if (text.includes('insomnia') || text.includes('sahar') || text.includes('gas') || text.includes('dry') || text.includes('melanch') || text.includes('sawda') || text.includes('depression') || text.includes('anxiety')) {
      mizajDeviation = 'Su-e-Mizaj Barid Sawdawi (Cold-Dry Melancholic / سوء مزاج بارد سوداوی)';
      baselineMizaj = 'Sawdawi (Melancholic)';
      percentages = { damawi: 15, balghami: 15, safrawi: 15, sawdawi: 55 };
    }

    // 2. 10-AJNAS PULSE (اجناسِ عشرہ نبض) MAPPING
    let ajnasPulse = 'Nabz-e-Batee wa Layyin (Slow, Soft & Deep Phlegmatic / نبض بطی و لین)';
    let miqdar = 'Motadil';
    let harakat = 'Batee (Slow)';
    let qawwa = 'Motadil';

    if (percentages.safrawi > 40) {
      ajnasPulse = 'Nabz-e-Saree wa Daqeeq wa Mushtadd (Rapid, Sharp & Active Bilious / نبض سریع و دقیق)';
      harakat = 'Saree (Rapid)';
      miqdar = 'Daqeeq (Small/Sharp)';
      qawwa = 'Mushtadd (Tense)';
    } else if (percentages.damawi > 40) {
      ajnasPulse = 'Nabz-e-Azeem wa Qawi wa Mumtali (Full, Strong & Bounding Sanguine / نبض عظیم و قوی و ممتلی)';
      harakat = 'Saree / Motadil';
      miqdar = 'Azeem (Large)';
      qawwa = 'Qawi (Strong)';
    } else if (percentages.sawdawi > 40) {
      ajnasPulse = 'Nabz-e-Batee wa Salb wa Munqata (Slow, Hard & Spasmodic Melancholic / نبض بطی و صلب)';
      harakat = 'Batee (Slow)';
      miqdar = 'Sagheer (Small)';
      qawwa = 'Salb (Hard)';
    }

    // 3. 12-ORGAN AXIS (اعضاء کے بارہ راستے) IDENTIFICATION
    let organAxis = 'Axis 6: Mafasil-Azlat (Musculoskeletal / مفاصل و عضلات)';
    let axisCode = 'MAFASIL';

    if (text.includes('liver') || text.includes('jigar') || text.includes('steatosis') || text.includes('sgpt') || text.includes('jaundice')) {
      organAxis = 'Axis 2: Jigar-Tihal (Hepatosplenic / جگر و طحال)';
      axisCode = 'JIGAR';
    } else if (text.includes('stone') || text.includes('kidney') || text.includes('renal') || text.includes('hisat') || text.includes('creatinine')) {
      organAxis = 'Axis 5: Kulliya-Masana (Renal-Urological / کلیہ و مثانہ)';
      axisCode = 'KULLIYA';
    } else if (text.includes('stomach') || text.includes('dyspep') || text.includes('hazm') || text.includes('gerd') || text.includes('gas') || text.includes('colitis')) {
      organAxis = 'Axis 1: Meda-Amaa (Gastrointestinal / معدہ و امعاء)';
      axisCode = 'MEDA';
    } else if (text.includes('bp') || text.includes('pressure') || text.includes('heart') || text.includes('qalb') || text.includes('cardio')) {
      organAxis = 'Axis 4: Qalb-Urooq (Cardiovascular / قلب و عروق)';
      axisCode = 'QALB';
    } else if (text.includes('headache') || text.includes('migraine') || text.includes('insomnia') || text.includes('dimagh') || text.includes('neuro')) {
      organAxis = 'Axis 3: Dimagh-Aasab (Neuropsychiatric / دماغ و اعصاب)';
      axisCode = 'DIMAGH';
    } else if (text.includes('asthma') || text.includes('dama') || text.includes('zeeq') || text.includes('cough') || text.includes('bronch') || text.includes('sadr')) {
      organAxis = 'Axis 9: Sadr-Riya (Respiratory / صدر و ریہ)';
      axisCode = 'SADR';
    } else if (text.includes('pcos') || text.includes('period') || text.includes('menses') || text.includes('sailan') || text.includes('reham')) {
      organAxis = 'Axis 7: Tams-Reham (Gynecological / رحم و طمث)';
      axisCode = 'REHAM';
    } else if (text.includes('bah') || text.includes('surat') || text.includes('inzal') || text.includes('mani') || text.includes('jariyan') || text.includes('sperm')) {
      organAxis = 'Axis 8: Bah-Mani (Andrological & Vitality / باہ و منی)';
      axisCode = 'BAH';
    } else if (text.includes('skin') || text.includes('jild') || text.includes('eczema') || text.includes('rash') || text.includes('khujli') || text.includes('alopecia')) {
      organAxis = 'Axis 10: Jild-Sha\'r (Dermatological / جلد و شعر)';
      axisCode = 'JILD';
    }

    // 4. DUAL DIAGNOSIS & ICD-11 CODE MAPPING
    let dualDiag = {
      unani: detectedDiag || 'Waja-ul-Mafasil Balghami (وجع المفاصل بلغمی)',
      biomedical: 'Bilateral Knee Osteoarthritis',
      icd11: 'FA00.0'
    };

    if (axisCode === 'JIGAR') {
      dualDiag.biomedical = 'Non-Alcoholic Fatty Liver Disease (NAFLD)';
      dualDiag.icd11 = 'DB92';
    } else if (axisCode === 'KULLIYA') {
      dualDiag.biomedical = 'Calculus of Kidney / Nephrolithiasis';
      dualDiag.icd11 = 'GB40.0';
    } else if (axisCode === 'MEDA') {
      dualDiag.biomedical = 'Functional Dyspepsia & Acid Peptic Disorder';
      dualDiag.icd11 = 'DB30';
    } else if (axisCode === 'QALB') {
      dualDiag.biomedical = 'Essential Primary Hypertension';
      dualDiag.icd11 = 'BA00';
    } else if (axisCode === 'DIMAGH') {
      dualDiag.biomedical = 'Chronic Migraine & Tension Cephalalgia';
      dualDiag.icd11 = '8A80.0';
    } else if (axisCode === 'SADR') {
      dualDiag.biomedical = 'Bronchial Asthma & Chronic Bronchospasm';
      dualDiag.icd11 = 'CA23';
    } else if (axisCode === 'REHAM') {
      dualDiag.biomedical = 'Polycystic Ovarian Syndrome (PCOS) / Pelvic Congestion';
      dualDiag.icd11 = '5A80.1';
    } else if (axisCode === 'BAH') {
      dualDiag.biomedical = 'Male Sexual Dysfunction & Seminal Debility';
      dualDiag.icd11 = 'GA10';
    } else if (axisCode === 'JILD') {
      dualDiag.biomedical = 'Chronic Atopic Dermatitis / Eczematous Prurigo';
      dualDiag.icd11 = 'EA80';
    }

    // 5. AF'AAL CASCADE & THERAPEUTIC STAGING
    let afaalStage = 'Stage 1: Nuzj-e-Khilt (Munzij-e-Balgham / منضج بلغم — 14 Days)';
    let primaryFaculty = 'Quwa-e-Tabiyyah (Nutritive / Metabolic Faculty)';

    if (percentages.safrawi > 40) {
      afaalStage = 'Stage 1: Nuzj-e-Safra (Munzij-e-Safra / منضج صفراء — 7 Days)';
      primaryFaculty = 'Quwa-e-Tabiyyah (Hepatic/Metabolic)';
    } else if (percentages.damawi > 40) {
      afaalStage = 'Stage 1: Fasd / Tadeel-e-Dam (Venesection / Vascular Cooling — 7 Days)';
      primaryFaculty = 'Quwa-e-Haywaniyyah (Cardiovascular / Vital)';
    } else if (percentages.sawdawi > 40) {
      afaalStage = 'Stage 1: Nuzj-e-Sawda (Munzij-e-Sawda / منضج سوداء — 21 Days)';
      primaryFaculty = 'Quwa-e-Nafsaniyyah (Psychic / Nervous)';
    }

    // Update global patient state
    if (typeof state !== 'undefined' && state && state.patient) {
      state.patient.currentDyscrasia = mizajDeviation;
      state.patient.baselineMizaj = baselineMizaj;
      state.patient.mizaj = mizajDeviation;
      state.patient.nabzType = ajnasPulse;
      state.afaalStage = afaalStage;
    }

    return {
      mizajDeviation,
      baselineMizaj,
      percentages,
      ajnasPulse,
      miqdar,
      harakat,
      qawwa,
      organAxis,
      axisCode,
      dualDiag,
      afaalStage,
      primaryFaculty
    };
  }

  function renderUnaniPrinciplesSynthesis(data) {
    const card = document.getElementById('fast-unani-principles-card');
    if (!card) return;

    card.innerHTML = `
      <div class="p-3 bg-gradient-to-r from-emerald-950/90 via-slate-900 to-teal-950/90 border border-emerald-500/40 rounded-2xl shadow-sm text-xs space-y-2">
        <div class="flex items-center justify-between border-b border-emerald-500/20 pb-1.5">
          <div class="flex items-center gap-1.5">
            <span class="w-5 h-5 rounded-md bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-bold text-xs">⚖️</span>
            <strong class="text-white text-xs">Unani Clinical Principles (اصولِ طب — خودکار خلاصہ)</strong>
          </div>
          <span class="text-[9px] font-mono text-emerald-300 font-bold bg-emerald-500/20 px-2 py-0.5 rounded border border-emerald-500/30">Backend Computed</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
          <!-- Mizaj Deviation -->
          <div class="bg-slate-900/80 p-2 rounded-xl border border-slate-800 space-y-0.5">
            <span class="text-[10px] text-slate-400 block font-medium">سوء مزاج (Mizaj Deviation):</span>
            <strong class="text-emerald-300 font-bold block">${data.mizajDeviation}</strong>
            <span class="text-[9px] text-slate-400 font-mono">Dam: ${data.percentages.damawi}% | Balgham: ${data.percentages.balghami}% | Safra: ${data.percentages.safrawi}% | Sawda: ${data.percentages.sawdawi}%</span>
          </div>

          <!-- 10-Ajnas Pulse -->
          <div class="bg-slate-900/80 p-2 rounded-xl border border-slate-800 space-y-0.5">
            <span class="text-[10px] text-slate-400 block font-medium">اجناسِ عشرہ نبض (10-Ajnas Pulse):</span>
            <strong class="text-cyan-300 font-bold block">${data.ajnasPulse}</strong>
            <span class="text-[9px] text-slate-400 font-mono">Harakat: ${data.harakat} • Miqdar: ${data.miqdar} • Qawwa: ${data.qawwa}</span>
          </div>

          <!-- Organ Axis -->
          <div class="bg-slate-900/80 p-2 rounded-xl border border-slate-800 space-y-0.5">
            <span class="text-[10px] text-slate-400 block font-medium">اعضاء کا راستہ (Organ Axis):</span>
            <strong class="text-amber-300 font-bold block">${data.organAxis}</strong>
            <span class="text-[9px] text-slate-400 font-mono">Faculty: ${data.primaryFaculty}</span>
          </div>

          <!-- Dual Diagnosis & Af'aal Cascade -->
          <div class="bg-slate-900/80 p-2 rounded-xl border border-slate-800 space-y-0.5">
            <span class="text-[10px] text-slate-400 block font-medium">تشخیص و مراحلِ علاج (ICD-11 &amp; Af'aal Cascade):</span>
            <strong class="text-purple-300 font-bold block">${data.dualDiag.biomedical} (${data.dualDiag.icd11})</strong>
            <span class="text-[9px] text-teal-300 font-mono">${data.afaalStage}</span>
          </div>
        </div>
      </div>
    `;
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
    else m.strength = m.strength + ' [+]';

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
    else if (m.strength.includes(' [+]')) m.strength = m.strength.replace(' [+]', '');
    else m.strength = m.strength + ' [−]';

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

    # Inject functions right above renderFastMatabPrescriptionList
    anchor = 'function renderFastMatabPrescriptionList() {'
    if anchor in c and 'function calculateAutonomousUnaniPrinciples' not in c:
        c = c.replace(anchor, unani_functions + "\n  " + anchor)
        print(f"[✓] Injected Unani computational functions and dose steppers into {fp}")

    # Update renderFastMatabPrescriptionList to include dose stepper buttons [ - ] 5g [ + ]
    old_rx_map = """      return `
      <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 hover:border-slate-700 transition flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-xs">
        <div class="space-y-0.5">
          <div class="flex items-center gap-2 flex-wrap">
            <strong class="text-white text-sm">${idx + 1}. ${m.name}</strong>
            <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${m.track || 'FORMULATION'}</span>
            <span class="text-[10px] text-slate-400 font-mono">${m.form || ''}</span>
            ${stockBadge}
          </div>
          <p class="text-[11px] text-slate-300">
            Dose: <strong class="text-amber-300 font-mono">${m.strength}</strong> • 
            Timing: <span>☀️ ${m.morning || '—'} | ⛅ ${m.noon || '—'} | 🌙 ${m.night || '—'}</span>
          </p>
          <p class="text-[10px] text-teal-400">Vehicle (Badraqa): ${m.anupan || 'Lukewarm water'}</p>
        </div>
        <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
          ${badalBtn}
          <button onclick="removePrescriptionMedicine(${idx}); renderFastMatabPrescriptionList(); calculateIlajBilZidd();" class="text-rose-400 hover:text-rose-300 text-xs px-2.5 py-1 rounded bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30">
            ✕ Remove
          </button>
        </div>
      </div>
      `;"""

    new_rx_map = """      return `
      <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 hover:border-slate-700 transition flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-xs">
        <div class="space-y-1">
          <div class="flex items-center gap-2 flex-wrap">
            <strong class="text-white text-sm">${idx + 1}. ${m.name}</strong>
            <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${m.track || 'FORMULATION'}</span>
            <span class="text-[10px] text-slate-400 font-mono">${m.form || ''}</span>
            ${stockBadge}
          </div>
          <div class="flex items-center gap-2 flex-wrap text-[11px] text-slate-300">
            <div class="inline-flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded-lg border border-slate-700">
              <span class="text-[10px] text-slate-400">Dose:</span>
              <button type="button" onclick="decreaseMedicineDose(${idx})" class="w-4 h-4 rounded bg-slate-900 hover:bg-slate-700 text-slate-300 hover:text-white font-black text-xs flex items-center justify-center transition cursor-pointer" title="Dose Ghatayein (-)">−</button>
              <strong class="text-amber-300 font-mono text-[11px] px-1">${m.strength}</strong>
              <button type="button" onclick="increaseMedicineDose(${idx})" class="w-4 h-4 rounded bg-slate-900 hover:bg-emerald-600 text-slate-300 hover:text-white font-black text-xs flex items-center justify-center transition cursor-pointer" title="Dose Badhayein (+)">+</button>
            </div>
            <span>• Timing: ☀️ ${m.morning || '—'} | ⛅ ${m.noon || '—'} | 🌙 ${m.night || '—'}</span>
          </div>
          <p class="text-[10px] text-teal-400">Vehicle (Badraqa): ${m.anupan || 'Lukewarm water'}</p>
        </div>
        <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
          ${badalBtn}
          <button onclick="removePrescriptionMedicine(${idx}); renderFastMatabPrescriptionList(); calculateIlajBilZidd();" class="text-rose-400 hover:text-rose-300 text-xs px-2.5 py-1 rounded bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 flex items-center gap-1" title="Nuskhe se hatayein">
            <span>✕</span> <span>ہٹائیں</span>
          </button>
        </div>
      </div>
      `;"""

    if old_rx_map in c:
        c = c.replace(old_rx_map, new_rx_map)
        print(f"[✓] Updated prescription items list with dose steppers [ - ] 5g [ + ] in {fp}")

    with open(fp, 'w') as f:
        f.write(c)

print("Wiring complete.")
