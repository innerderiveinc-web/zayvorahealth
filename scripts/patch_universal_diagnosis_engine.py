#!/usr/bin/env python3
"""
ZAYVORA Health OS — Universal Diagnosis & Adaptive AI Nuskha Engine
Enables automatic AI prescription drafting for ANY disease, diagnosis, or symptom:
1. Expands built-in protocols to cover Renal/Kidney Stones, Hypertension, Piles/Bawaseer,
   Insomnia, Sciatica/Irq-un-Nasa, and Gynecological/PCOS disorders.
2. Implements a dynamic semantic formulary search fallback that searches all 59 Qarabadeen
   and 32 ZAYVORA preparations for matching clinical indications, notes, and organ-axes.
3. Allows free-text diagnosis entry in English, Urdu, or Roman Urdu.
4. Preserves 100% human-in-the-loop clinician gate: AI proposes, doctor finalizes.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_JS = os.path.join(BASE_DIR, "js", "zayvora-core.js")
MODULE_JS = os.path.join(BASE_DIR, "js", "modules", "02-clinical-workspace.js")

EXPANDED_GENERATE_AI_NUSKHA = """  function generateAiNuskhaFromDiagnosis(diagText) {
    if (!diagText) {
      const diagInput = document.getElementById('fast-diagnosis-input');
      diagText = diagInput ? diagInput.value : '';
    }
    const txt = (diagText || '').toLowerCase().trim();
    if (!txt) return;

    let protocolId = null;

    // 1. Check matching canonical protocols
    if (txt.includes('waja') || txt.includes('joint') || txt.includes('knee') || txt.includes('osteo') || txt.includes('mafasil') || txt.includes('gout') || txt.includes('niqras') || txt.includes('arthritis')) {
      protocolId = 'arthri';
    } else if (txt.includes('hazm') || txt.includes('gas') || txt.includes('dyspep') || txt.includes('pet') || txt.includes('kamuni') || txt.includes('stomach') || txt.includes('acid') || txt.includes('gerd') || txt.includes('qulanj')) {
      protocolId = 'gastro';
    } else if (txt.includes('suda') || txt.includes('migraine') || txt.includes('head') || txt.includes('sir') || txt.includes('shaqeeqa') || txt.includes('tensio')) {
      protocolId = 'ceph';
    } else if (txt.includes('sugar') || txt.includes('diabet') || txt.includes('ziabetus') || txt.includes('gluco') || txt.includes('metabol')) {
      protocolId = 'metabolic';
    } else if (txt.includes('bah') || txt.includes('vitality') || txt.includes('asab') || txt.includes('neuro') || txt.includes('weak') || txt.includes('mardana') || txt.includes('jiryan')) {
      protocolId = 'vitality';
    } else if (txt.includes('nazla') || txt.includes('cold') || txt.includes('cough') || txt.includes('khansi') || txt.includes('sadr') || txt.includes('respir') || txt.includes('banafsha') || txt.includes('dama') || txt.includes('asthma') || txt.includes('ziq')) {
      protocolId = 'respiratory';
    } else if (txt.includes('jigar') || txt.includes('liver') || txt.includes('kabid') || txt.includes('kasni') || txt.includes('mako') || txt.includes('jaundice') || txt.includes('yarqan')) {
      protocolId = 'liver';
    } else if (txt.includes('skin') || txt.includes('jild') || txt.includes('khujli') || txt.includes('rash') || txt.includes('ushba') || txt.includes('detox') || txt.includes('psoriasis') || txt.includes('eczema') || txt.includes('quba')) {
      protocolId = 'skin';
    } else if (txt.includes('stone') || txt.includes('pathri') || txt.includes('hisat') || txt.includes('kidney') || txt.includes('gurda') || txt.includes('renal') || txt.includes('peshab') || txt.includes('mutr') || txt.includes('kulliya')) {
      protocolId = 'renal';
    } else if (txt.includes('bp') || txt.includes('hypertens') || txt.includes('pressure') || txt.includes('zaght') || txt.includes('qalb') || txt.includes('heart')) {
      protocolId = 'hypertension';
    } else if (txt.includes('piles') || txt.includes('bawaseer') || txt.includes('hemorrhoid') || txt.includes('masse') || txt.includes('maqad')) {
      protocolId = 'piles';
    } else if (txt.includes('insomnia') || txt.includes('sahar') || txt.includes('neend') || txt.includes('sleep') || txt.includes('banafsheh')) {
      protocolId = 'insomnia';
    } else if (txt.includes('sciatica') || txt.includes('irq') || txt.includes('disc') || txt.includes('lumbago')) {
      protocolId = 'sciatica';
    } else if (txt.includes('pcos') || txt.includes('period') || txt.includes('menses') || txt.includes('haiz') || txt.includes('tams') || txt.includes('rehem') || txt.includes('uterus')) {
      protocolId = 'pcos';
    }

    if (protocolId) {
      applyFastProtocol(protocolId);
    } else {
      // 2. Intelligent Dynamic Semantic Formulation Search across Catalogs
      synthesizeDynamicNuskha(txt);
    }

    // Update banner visibility and status
    const banner = document.getElementById('ai-nuskha-proposal-banner');
    if (banner) {
      banner.classList.remove('hidden');
    }
    
    if (typeof showNotification === 'function') {
      showNotification(`✨ Hakeem Sahab™ AI proposed formulation for "${diagText}". Clinician review required before finalizing.`, 'info');
    }
  }

  function synthesizeDynamicNuskha(keyword) {
    const rx = state.prescriptions[0];
    if (!rx.medicines) rx.medicines = [];
    const parhezInput = document.getElementById('fast-parhez-text');

    const matchedMeds = [];
    const k = keyword.toLowerCase();

    // Search Qarabadeen
    if (typeof QARABADEEN_CATALOG !== 'undefined') {
      QARABADEEN_CATALOG.forEach(item => {
        const text = `${item.name} ${item.urdu_name || ''} ${item.notes || ''} ${item.axis || ''} ${item.category || ''}`.toLowerCase();
        if (text.includes(k)) {
          matchedMeds.push({
            name: `${item.name} (${item.urdu_name || ''})`,
            form: item.form || item.category || 'Compound',
            strength: item.strength || '5g Twice Daily',
            frequency: item.frequency || 'BD',
            morning: '5g / 1 dose',
            noon: '—',
            night: '5g / 1 dose',
            anupan: item.anupan || 'Neem garam paani (Lukewarm water)',
            axis: item.axis || 'Integrative',
            track: 'QARABADEEN'
          });
        }
      });
    }

    // Search ZAYVORA Sovereign
    if (typeof ZAYVORA_PRODUCTS_32 !== 'undefined') {
      ZAYVORA_PRODUCTS_32.forEach(item => {
        const text = `${item.name} ${item.indication || ''} ${item.category || ''}`.toLowerCase();
        if (text.includes(k)) {
          matchedMeds.push({
            name: item.name,
            form: item.form || 'Phytopharmaceutical',
            strength: '1 Unit Daily',
            frequency: 'OD',
            morning: '1 Unit',
            noon: '—',
            night: '—',
            anupan: 'Fresh water',
            axis: item.category || 'Integrative',
            track: 'ZAYVORA_PRODUCT'
          });
        }
      });
    }

    if (matchedMeds.length > 0) {
      rx.medicines = matchedMeds.slice(0, 4);
      if (parhezInput) {
        parhezInput.value = "Tez mirch masale, tali hui cheezein, baasi khana aur thandi ashiya se parhez karein. Taza aur subuk ghiza istemal karein.";
      }
    } else {
      // General Classical Adaptogenic & Detox Formula
      rx.medicines = [
        { name: 'Khamira Gaozaban Ambari (خمیرہ گاؤزبان عنبری)', form: 'Khamira', strength: '5g Morning', frequency: 'OD', morning: '5g', noon: '—', night: '—', anupan: 'Neem garam doodh ya paani', axis: 'Cardio-Neuro', track: 'QARABADEEN' },
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل)', form: 'Sharbat', strength: '20ml BD', frequency: 'BD', morning: '20ml in water', noon: '—', night: '20ml in water', anupan: 'Lukewarm water', axis: 'Renal/Hepatic', track: 'QARABADEEN' },
        { name: 'Itrifal Ustukhuddus (اطریفل اسطخودوس)', form: 'Itrifal', strength: '5g at Bedtime', frequency: 'OD', morning: '—', noon: '—', night: '5g', anupan: 'Lukewarm water', axis: 'Neuro-Digestive', track: 'QARABADEEN' }
      ];
      if (parhezInput) {
        parhezInput.value = "Sakht aur der-hazm khane, tez khatti cheezein aur thande paani se parhez karein. Motadil ghiza lein.";
      }
    }

    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    autoSaveConsultationDraft();
  }

  window.synthesizeDynamicNuskha = synthesizeDynamicNuskha;"""

EXPANDED_APPLY_PROTOCOL = """    } else if (protocolId === 'skin') {
      rx.medicines = [
        { name: 'Majun Ushba (معجون عشبہ / माजून उशबा)', form: 'Majun', strength: '5g BD', frequency: 'BD', morning: '5g', noon: '—', night: '5g', anupan: 'Fresh water / Sharbat Unnab', axis: 'Dermatologic', track: 'QARABADEEN' },
        { name: 'Sharbat Unnab (شربت عناب / शरबत उन्नाब)', form: 'Sharbat', strength: '20ml BD', frequency: 'BD', morning: '20ml', noon: '—', night: '20ml', anupan: 'Fresh water', axis: 'Dermatologic', track: 'QARABADEEN' },
        { name: 'Roghan-e-Neem (روغن نیم / रोग़न नीम)', form: 'Roghan (Oil)', strength: 'Hasb-e-Zaroorat (External)', frequency: 'OD', morning: '—', noon: '—', night: 'Apply gently', anupan: 'External use only', axis: 'Dermatologic', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Anda, Machli, Khatti aur garam cheezein, Gud aur baasi khane se mukammal parhez karein.";
      showNotification('Applied Musaffi-e-Dam Skin Detox Protocol (Majun Ushba + Unnab)', 'success');
    } else if (protocolId === 'renal') {
      rx.medicines = [
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل)', form: 'Sharbat (Syrup)', strength: '25ml with water', frequency: 'BD', morning: '25ml in water', noon: '—', night: '25ml in water', anupan: 'Lukewarm water', axis: 'Renal/Urinary', track: 'QARABADEEN' },
        { name: 'Majoon-e-Kundur (معجون کندر)', form: 'Majoon', strength: '5g Twice Daily', frequency: 'BD', morning: '5g', noon: '—', night: '5g', anupan: 'Fresh water', axis: 'Renal/Urinary', track: 'QARABADEEN' },
        { name: 'Bespoke Safoof-e-Hisat wa Mufattit (سفوف سنگ شکن)', form: 'Safoof', strength: '3g with Arq Badiyan', frequency: 'BD', morning: '3g', noon: '—', night: '3g', anupan: 'Arq-e-Badiyan (50ml)', axis: 'Renal/Urinary', track: 'SELF_NUSKHA', ingredients: 'Hajr-ul-Yahood Bhasma 1g, Kulthi 2g, Jawakhar 500mg, Shora Qalmi 500mg', notes: 'Clinician Bespoke Lithotriptic Formulation (سنگ شکن)' }
      ];
      if (parhezInput) parhezInput.value = "Tamatar, Palak, Chaulai, Gosht, Chawal aur Beej wali ashya se sakht parhez karein. Rozana 3 se 4 litre paani piyein.";
      showNotification('Applied Renal Lithotriptic Protocol (Sharbat Bazoori + Majoon Kundur)', 'success');
    } else if (protocolId === 'hypertension') {
      rx.medicines = [
        { name: 'Habbe Asrol / Asrafee (حب اسرول)', form: 'Habb (Tablet)', strength: '1 Tab BD', frequency: 'BD', morning: '1 Tablet', noon: '—', night: '1 Tablet', anupan: 'Fresh water', axis: 'Cardiovascular', track: 'QARABADEEN' },
        { name: 'Khamira Gaozaban Ambari (خمیرہ گاؤزبان عنبری)', form: 'Khamira', strength: '5g Morning', frequency: 'OD (Morning)', morning: '5g', noon: '—', night: '—', anupan: 'Warm milk / water', axis: 'Cardiovascular', track: 'QARABADEEN' },
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل)', form: 'Sharbat', strength: '20ml BD', frequency: 'BD', morning: '20ml in water', noon: '—', night: '20ml in water', anupan: 'Lukewarm water', axis: 'Renal/Hepatic', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Namak (salt) kam se kam karein, Tali hui cheezein, Tez mirch masale aur zehni tanaav se bachein. Subah walk karein.";
      showNotification('Applied Cardio-Vascular & Tension Protocol (Asrol + Khamira Gaozaban)', 'success');
    } else if (protocolId === 'piles') {
      rx.medicines = [
        { name: 'Habbe Muqil (حب مقل)', form: 'Habb (Tablet)', strength: '2 Tabs Twice Daily', frequency: 'BD', morning: '2 Tablets', noon: '—', night: '2 Tablets', anupan: 'Fresh water post-meals', axis: 'Gastrointestinal', track: 'QARABADEEN' },
        { name: 'Itrifal Muqil (اطریفل مقل)', form: 'Itrifal', strength: '7g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '7g (1.5 tsp)', anupan: 'Lukewarm water', axis: 'Gastrointestinal', track: 'QARABADEEN' },
        { name: 'Marham-e-Kafoori (مرہم کافوری)', form: 'Marham (Ointment)', strength: 'Local Application', frequency: 'BD', morning: 'Apply gently', noon: '—', night: 'Apply after wash', anupan: 'External use', axis: 'Proctologic', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Qabz (constipation) se bachein. Tez lal mirch, gosht, garam masale aur maida band karein. Papiya aur daliya lein.";
      showNotification('Applied Anti-Hemorrhoidal Protocol (Habbe Muqil + Itrifal Muqil)', 'success');
    } else if (protocolId === 'insomnia') {
      rx.medicines = [
        { name: 'Khamira Gaozaban Ambari (خمیرہ گاؤزبان عنبری)', form: 'Khamira', strength: '5g Morning', frequency: 'OD (Morning)', morning: '5g empty stomach', noon: '—', night: '—', anupan: 'Warm milk', axis: 'Neuropsychiatric', track: 'QARABADEEN' },
        { name: 'Roghan-e-Kahu / Roghan-e-Labub (روغن کاہو)', form: 'Roghan (Oil)', strength: 'Hasb-e-Zaroorat', frequency: 'OD (Night)', morning: '—', noon: '—', night: 'Gentle scalp massage', anupan: 'External friction', axis: 'Neurologic', track: 'QARABADEEN' },
        { name: 'Sharbat Banafsha (شربت بنفشہ)', form: 'Sharbat', strength: '20ml at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '20ml in warm water', anupan: 'Warm water', axis: 'Neurologic', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Chai, Coffee aur Cold drinks sham 5 baje ke baad bilkul band karein. Raat ko mobile/screen se door rahein.";
      showNotification('Applied Cephalic Calming & Sleep Protocol (Roghan Kahu + Khamira)', 'success');
    } else if (protocolId === 'sciatica') {
      rx.medicines = [
        { name: 'Majun Suranjan (معجون سرنجان)', form: 'Majun', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g', anupan: 'Lukewarm water', axis: 'Neuromuscular', track: 'QARABADEEN' },
        { name: 'Majun Chobchini (معجون چوب چینی)', form: 'Majun', strength: '5g Morning', frequency: 'OD (Morning)', morning: '5g', noon: '—', night: '—', anupan: 'Warm water', axis: 'Neuromuscular', track: 'QARABADEEN' },
        { name: 'Roghan-e-Suranjan (روغن سرنجان)', form: 'Roghan (Oil)', strength: 'Local Application', frequency: 'BD', morning: 'Warm massage', noon: '—', night: 'Warm massage', anupan: 'External use', axis: 'Neuromuscular', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Thandi hawa aur seedhe AC ke samne baithne se bachein. Bhari wazan na uthayein. Badi ashiya band karein.";
      showNotification('Applied Sciatica & Neuralgia Protocol (Suranjan + Chobchini)', 'success');
    } else if (protocolId === 'pcos') {
      rx.medicines = [
        { name: 'Majun Supari Pak (معجون سپاری پاک)', form: 'Majun', strength: '5g Twice Daily', frequency: 'BD', morning: '5g with warm milk', noon: '—', night: '5g', anupan: 'Lukewarm milk', axis: 'Endocrine/Reproductive', track: 'QARABADEEN' },
        { name: 'Sharbat Mudir (شربت مدر)', form: 'Sharbat', strength: '20ml BD', frequency: 'BD', morning: '20ml in water', noon: '—', night: '20ml in water', anupan: 'Warm water', axis: 'Endocrine/Reproductive', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Meetha, Chawal, Fast food aur Dairy ki zyadati se bachein. Rozana 30 minute brisk walk ya kasrat karein.";
      showNotification('Applied Endocrine & Hormonal Protocol (Supari Pak + Sharbat Mudir)', 'success');
    }"""

def apply_universal_patch(filepath):
    if not os.path.exists(filepath):
        print(f"[-] File not found: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace generateAiNuskhaFromDiagnosis
    gen_pattern = re.compile(
        r'function generateAiNuskhaFromDiagnosis\(diagText\)\s*\{[\s\S]*?window\.generateAiNuskhaFromDiagnosis\s*=\s*generateAiNuskhaFromDiagnosis;',
        re.MULTILINE
    )

    if gen_pattern.search(content):
        content = gen_pattern.sub(EXPANDED_GENERATE_AI_NUSKHA.strip(), content)
        print(f"[✓] {os.path.basename(filepath)}: Upgraded generateAiNuskhaFromDiagnosis with universal semantic engine")
    else:
        print(f"[!] {os.path.basename(filepath)}: Could not match exact generateAiNuskhaFromDiagnosis pattern")

    # 2. Expand applyFastProtocol
    old_skin_branch = """    } else if (protocolId === 'skin') {
      rx.medicines = [
        { name: 'Majun Ushba (معجون عشبہ / माजून उशबा)', form: 'Majun', strength: '5g BD', frequency: 'BD', morning: '5g', noon: '—', night: '5g', anupan: 'Fresh water / Sharbat Unnab', axis: 'Dermatologic', track: 'QARABADEEN' },
        { name: 'Sharbat Unnab (شربت عناب / शरबत उन्नाब)', form: 'Sharbat', strength: '20ml BD', frequency: 'BD', morning: '20ml', noon: '—', night: '20ml', anupan: 'Fresh water', axis: 'Dermatologic', track: 'QARABADEEN' },
        { name: 'Roghan-e-Neem (روغن نیم / रोग़न नीम)', form: 'Roghan (Oil)', strength: 'Hasb-e-Zaroorat (External)', frequency: 'OD', morning: '—', noon: '—', night: 'Apply gently', anupan: 'External use only', axis: 'Dermatologic', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Anda, Machli, Khatti aur garam cheezein, Gud aur baasi khane se mukammal parhez karein.";
      showNotification('Applied Musaffi-e-Dam Skin Detox Protocol (Majun Ushba + Unnab)', 'success');
    }"""

    if old_skin_branch in content:
        content = content.replace(old_skin_branch, EXPANDED_APPLY_PROTOCOL)
        print(f"[✓] {os.path.basename(filepath)}: Added Renal, Hypertension, Piles, Insomnia, Sciatica, and PCOS protocols")
    else:
        print(f"[!] {os.path.basename(filepath)}: Old skin branch pattern not matched exact")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True

if __name__ == "__main__":
    print("=" * 70)
    print(" ZAYVORA Health OS — Universal Diagnosis & Adaptive AI Nuskha Engine")
    print("=" * 70)
    apply_universal_patch(CORE_JS)
    apply_universal_patch(MODULE_JS)
    print("=" * 70)
