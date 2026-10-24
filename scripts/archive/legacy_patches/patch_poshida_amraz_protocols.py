import sys

protocols_code = """    } else if (protocolId === 'poshida_male') {
      rx.medicines = [
        { name: 'Majoon Arad Khurma (معجون آرد خرما / माजून आरद ख़ुरما)', form: 'Majun', strength: '5g with Warm Milk', frequency: 'BD', morning: '5g', noon: '—', night: '5g', anupan: 'Lukewarm cow milk', axis: 'Neuro-Andrological', track: 'QARABADEEN' },
        { name: 'Majun Salab (معجون ثعلب)', form: 'Majun', strength: '5g Once Daily (Morning)', frequency: 'OD (Morning)', morning: '5g', noon: '—', night: '—', anupan: 'Warm milk + 2 dates', axis: 'Neuro-Andrological', track: 'QARABADEEN' },
        { name: 'Habbe Jadwar (حب جدوار / हब्बे जदवार)', form: 'Habb (Tablet)', strength: '1 Tab at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '1 Tablet', anupan: 'Warm milk', axis: 'Neuro-Andrological', track: 'QARABADEEN' },
        { name: 'ManiVital Pro™ Herbal Extract', form: 'Stick Sachet', strength: '1 Sachet Daily', frequency: 'OD (Morning)', morning: '1 Sachet', noon: '—', night: '—', anupan: 'Warm milk', axis: 'Neuro-Andrological', track: 'ZAYVORA_PRODUCT' }
      ];
      if (parhezInput) parhezInput.value = "Tez mirch masale, garm taseer aashia (beef, egg yolk, alcohol), late night jagna aur qabz se bachein. Subah nahaar-munh doodh aur badam istemal karein.";
      showNotification('Applied Male Reproductive & Vitality Protocol (Arad Khurma + Salab + Jadwar)', 'success');
    } else if (protocolId === 'poshida_sailan') {
      rx.medicines = [
        { name: 'Majun Supari Pak (معجون سپاری پاک)', form: 'Majun', strength: '7g Twice Daily', frequency: 'BD', morning: '7g', noon: '—', night: '7g', anupan: 'Lukewarm milk', axis: 'Gynecological', track: 'QARABADEEN' },
        { name: 'Safoof Sailan (سفوف سیلان)', form: 'Safoof (Powder)', strength: '5g Twice Daily', frequency: 'BD', morning: '5g', noon: '—', night: '5g', anupan: 'Fresh water / cow milk', axis: 'Gynecological', track: 'QARABADEEN' },
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل)', form: 'Sharbat (Syrup)', strength: '20ml in water', frequency: 'BD', morning: '20ml', noon: '—', night: '20ml', anupan: 'Fresh water', axis: 'Renal-Gynecological', track: 'QARABADEEN' },
        { name: 'FeminaVora™ Uterine Balance', form: 'Capsule', strength: '1 Cap BD', frequency: 'BD', morning: '1 Capsule', noon: '—', night: '1 Capsule', anupan: 'Fresh water', axis: 'Gynecological', track: 'ZAYVORA_PRODUCT' }
      ];
      if (parhezInput) parhezInput.value = "Khatti aashia (imli, achaar, tamatar), baasi aur tili hui cheezon se parhez karein. Zati safai (intimate hygiene) ka khas khayal rakhein.";
      showNotification('Applied Gynecological & Leucorrhea Protocol (Supari Pak + Safoof Sailan)', 'success');
    } else if (protocolId === 'poshida_bleeding') {
      rx.medicines = [
        { name: 'Safoof Habis (سفوف حابس)', form: 'Safoof (Powder)', strength: '3g Twice Daily', frequency: 'BD', morning: '3g', noon: '—', night: '3g', anupan: 'Cold water or Sharbat Anjabar', axis: 'Gynecological', track: 'QARABADEEN' },
        { name: 'Majun Muqawwi-e-Reham (معجون مقوی رحم)', form: 'Majun', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g', anupan: 'Lukewarm milk', axis: 'Gynecological', track: 'QARABADEEN' },
        { name: 'Sharbat Anjabar (شربت انجبار)', form: 'Sharbat (Syrup)', strength: '20ml Twice Daily', frequency: 'BD', morning: '20ml', noon: '—', night: '20ml', anupan: 'Arq Gaozaban or water', axis: 'Hemostatic', track: 'QARABADEEN' }
      ];
      if (parhezInput) parhezInput.value = "Mukammal aaraam karein, shadeed mehnath aur garam masaledar khano se parhez karein. Thande mashroobat istemal karein.";
      showNotification('Applied Uterine Hemostatic Protocol (Safoof Habis + Muqawwi-e-Reham)', 'success');
    } else if (protocolId === 'poshida_infertility') {
      rx.medicines = [
        { name: 'Majun Muqawwi-e-Reham (معجون مقوی رحم)', form: 'Majun', strength: '5g Twice Daily', frequency: 'BD', morning: '5g', noon: '—', night: '5g', anupan: 'Lukewarm cow milk', axis: 'Gynecological', track: 'QARABADEEN' },
        { name: 'Khamira Gaozaban Ambari (خمیرہ گاوزبان عنبری)', form: 'Khamira', strength: '5g Morning', frequency: 'OD (Morning)', morning: '5g', noon: '—', night: '—', anupan: 'Arq Gaozaban', axis: 'Neuro-Endocrine', track: 'QARABADEEN' },
        { name: 'FeminaVora™ OvulaGranules', form: 'Stick Sachet', strength: '1 Sachet Daily', frequency: 'OD (Morning)', morning: '1 Sachet', noon: '—', night: '—', anupan: 'Warm milk with honey', axis: 'Reproductive', track: 'ZAYVORA_PRODUCT' }
      ];
      if (parhezInput) parhezInput.value = "Maqwi gizaayein (badam, maghziyat, khajoor, dhoodh) istemal karein. Zehni tanav (stress) aur raton ko der tak jagna band karein.";
      showNotification('Applied Subfertility & Uterine Tonic Protocol (Muqawwi-e-Reham + Gaozaban)', 'success');
    } else if (protocolId === 'poshida_sozak') {
      rx.medicines = [
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل)', form: 'Sharbat (Syrup)', strength: '25ml Thrice Daily', frequency: 'TDS', morning: '25ml', noon: '25ml', night: '25ml', anupan: 'Fresh water / Ma-ul-Shaeer', axis: 'Genito-Urinary', track: 'QARABADEEN' },
        { name: 'Qurs Kushta Qalai (قرص کشتہ قلعی)', form: 'Qurs (Tablet)', strength: '1 Tab BD', frequency: 'BD', morning: '1 Tablet', noon: '—', night: '1 Tablet', anupan: 'Milk or Sharbat Bazoori', axis: 'Genito-Urinary', track: 'QARABADEEN' },
        { name: 'AlkaVora™ Alkalizing Granules', form: 'Granules', strength: '1 Sachet BD', frequency: 'BD', morning: '1 Sachet', noon: '—', night: '1 Sachet', anupan: '200ml cold water', axis: 'Renal-Genitourinary', track: 'ZAYVORA_PRODUCT' }
      ];
      if (parhezInput) parhezInput.value = "Rozana 3.5 se 4 litre paani, jau ka paani (Ma-ul-Shaeer), aur nariyal paani piyein. Mirch masale aur smoking se sakht parhez karein.";
      showNotification('Applied Urethral Soothing Protocol (Bazoori + Kushta Qalai)', 'success');
"""

branch_detect = """    } else if (txt.includes('sailan') || txt.includes('leucorrh') || txt.includes('likoria') || txt.includes('safed pani') || txt.includes('white discharge') || txt.includes('vaginitis')) {
      protocolId = 'poshida_sailan';
    } else if (txt.includes('istihaza') || txt.includes('kasrat-e-tams') || txt.includes('heavy bleeding') || txt.includes('menorrhagia') || txt.includes('zyada haiz')) {
      protocolId = 'poshida_bleeding';
    } else if (txt.includes('uqr') || txt.includes('infertility') || txt.includes('be auladi') || txt.includes('hamal') || txt.includes('ovulat') || txt.includes('conception')) {
      protocolId = 'poshida_infertility';
    } else if (txt.includes('sozak') || txt.includes('suzak') || txt.includes('urethritis') || txt.includes('gonorr') || txt.includes('peep')) {
      protocolId = 'poshida_sozak';
    } else if (txt.includes('surat') || txt.includes('inzal') || txt.includes('shighra') || txt.includes('jariyan') || txt.includes('jiryan') || txt.includes('mani') || txt.includes('riqqat') || txt.includes('sperm') || txt.includes('erectile') || txt.includes('namardi') || txt.includes('poshida') || txt.includes('mardana') || txt.includes('impoten')) {
      protocolId = 'poshida_male';
"""

for filepath in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update detection logic in generateAiNuskhaFromDiagnosis
    pcos_block = "} else if (txt.includes('pcos') || txt.includes('period') || txt.includes('menses') || txt.includes('haiz') || txt.includes('tams') || txt.includes('rehem') || txt.includes('uterus')) {\n      protocolId = 'pcos';\n"
    if pcos_block in content and 'poshida_male' not in content:
        content = content.replace(pcos_block, pcos_block + branch_detect)
        print(f"[✓] Added poshida amraz detection branches to {filepath}")
    else:
        print(f"[!] Detection branches check: already present or anchor missing in {filepath}")

    # 2. Add protocol bodies to applyFastProtocol
    pcos_end_anchor = "showNotification('Applied Women\\'s Health Protocol (Supari Pak + Bazoori + FeminaVora™)', 'success');\n    }"
    if pcos_end_anchor in content and "protocolId === 'poshida_male'" not in content:
        replacement = pcos_end_anchor + "\n" + protocols_code
        content = content.replace(pcos_end_anchor, replacement)
        print(f"[✓] Added poshida amraz protocol definitions to {filepath}")
    else:
        print(f"[!] Protocol definitions check: already present or anchor missing in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

print("Patch complete.")
