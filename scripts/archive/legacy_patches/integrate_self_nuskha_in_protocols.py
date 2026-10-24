#!/usr/bin/env python3
"""
ZAYVORA Health OS — Self-Nuskha (Bespoke Compounding) Integration
Ensures every auto-synthesized clinical prescription includes:
1. Classical Qarabadeen Murakkab (NFUM Pharmacopoeia)
2. ZAYVORA Sovereign Standardized Product
3. Bespoke Clinician Self-Nuskha (Personalized Mufradat Compound / خود ساختہ نسخہ)
4. Dietary guidelines & Asbab-e-Sittah Zarooriyyah regimen
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_JS = os.path.join(BASE_DIR, "js", "zayvora-core.js")

def update_fast_protocols():
    with open(CORE_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Update arthri in applyFastProtocol to include Bespoke Self-Nuskha
    old_arthri = """    if (protocolId === 'arthri') {
      rx.medicines = [
        { name: 'Majun Suranjan (معجون سرنجان / माजून सुरंजान)', form: 'Majun (Paste)', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g (1 tsp)', anupan: 'Lukewarm water / Arq-e-Gaozaban', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'Roghan-e-Suranjan (روغن سرنجان / रोग़ن सुरंजان)', form: 'Roghan (Oil)', strength: 'Hasb-e-Zaroorat', frequency: 'BD (Morning & Night)', morning: 'Local Application', noon: '—', night: 'Gentle Friction', anupan: 'External Dalk (Massage)', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'Habbe Asgand (حب اسگند / हब्बे असگند)', form: 'Habb (Tablet)', strength: '2 Tabs BD', frequency: 'BD', morning: '2 Tablets', noon: '—', night: '2 Tablets', anupan: 'Lukewarm milk or water', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'SynovoFlex™ Micro-Granules', form: 'Stick Sachet', strength: '5g Once Daily', frequency: 'OD (Morning)', morning: '1 Sachet (5g)', noon: '—', night: '—', anupan: '100ml warm water post-breakfast', axis: 'Musculoskeletal', track: 'ZAYVORA_PRODUCT' }
      ];"""

    new_arthri = """    if (protocolId === 'arthri') {
      rx.medicines = [
        { name: 'Majun Suranjan (معجون سرنجان / माजून सुरंजान)', form: 'Majun (Paste)', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g (1 tsp)', anupan: 'Lukewarm water / Arq-e-Gaozaban', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'Roghan-e-Suranjan (روغن سرنجان / रोग़ن सुरंजان)', form: 'Roghan (Oil)', strength: 'Hasb-e-Zaroorat', frequency: 'BD (Morning & Night)', morning: 'Local Application', noon: '—', night: 'Gentle Friction', anupan: 'External Dalk (Massage)', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'SynovoFlex™ Micro-Granules', form: 'Stick Sachet', strength: '5g Once Daily', frequency: 'OD (Morning)', morning: '1 Sachet (5g)', noon: '—', night: '—', anupan: '100ml warm water post-breakfast', axis: 'Musculoskeletal', track: 'ZAYVORA_PRODUCT' },
        { name: 'Bespoke Safoof-e-Tanqiya-e-Mafasil (سفوف تنقیہ مفاصل و جگر)', form: 'Safoof (Micro-Powder)', strength: '3g Morning Empty Stomach', frequency: 'OD (Morning)', morning: '3g (1/2 tsp)', noon: '—', night: '—', anupan: 'Arq-e-Kasni wa Mako (50ml)', axis: 'Hepato-Musculoskeletal', track: 'SELF_NUSKHA', ingredients: 'Asgandh 2g, Suranjan Talkh Mudabbar 500mg, Zanjabeel 1g, Filfil Siyah 250mg, Kateera 500mg', notes: 'Clinician Bespoke Humoral Balance (خود ساختہ نسخہ)' }
      ];"""

    if old_arthri in js:
        js = js.replace(old_arthri, new_arthri, 1)
        print("✓ Injected Bespoke Self-Nuskha into ArthriCare protocol")

    # 2. Update gastro in applyFastProtocol to include Bespoke Self-Nuskha
    old_gastro = """    } else if (protocolId === 'gastro') {
      rx.medicines = [
        { name: 'Jawarish Kamuni (جوارش کمونی / जवारिश कमूनी)', form: 'Jawarish', strength: '5g Post Meals', frequency: 'BD', morning: '5g after meal', noon: '—', night: '5g after dinner', anupan: 'Fresh water', axis: 'Gastrointestinal', track: 'QARABADEEN' },
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل / शरबत बज़ूरी)', form: 'Sharbat (Syrup)', strength: '20ml with water', frequency: 'BD', morning: '20ml in water', noon: '20ml in water', night: '—', anupan: 'Lukewarm water', axis: 'Renal/Hepatic', track: 'QARABADEEN' },
        { name: 'Itrifal Ustukhuddus (اطریفل اسطخودوس / इतरीफ़ل उसतुख़ुद्दूस)', form: 'Itrifal', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g', anupan: 'Warm water', axis: 'Gastrointestinal', track: 'QARABADEEN' },
        { name: 'GastroVora™ Veg Capsules', form: 'Capsule', strength: '1 Cap BD', frequency: 'BD', morning: '1 Capsule', noon: '—', night: '1 Capsule', anupan: 'Fresh water', axis: 'Gastrointestinal', track: 'ZAYVORA_PRODUCT' }
      ];"""

    new_gastro = """    } else if (protocolId === 'gastro') {
      rx.medicines = [
        { name: 'Jawarish Kamuni (جوارش کمونی / जوارिश कमूनी)', form: 'Jawarish', strength: '5g Post Meals', frequency: 'BD', morning: '5g after meal', noon: '—', night: '5g after dinner', anupan: 'Fresh water', axis: 'Gastrointestinal', track: 'QARABADEEN' },
        { name: 'Sharbat Bazoori Motadil (شربت بزوری معتدل / शरबत बज़ूरी)', form: 'Sharbat (Syrup)', strength: '20ml with water', frequency: 'BD', morning: '20ml in water', noon: '20ml in water', night: '—', anupan: 'Lukewarm water', axis: 'Renal/Hepatic', track: 'QARABADEEN' },
        { name: 'GastroVora™ Veg Capsules', form: 'Capsule', strength: '1 Cap BD', frequency: 'BD', morning: '1 Capsule', noon: '—', night: '1 Capsule', anupan: 'Fresh water', axis: 'Gastrointestinal', track: 'ZAYVORA_PRODUCT' },
        { name: 'Bespoke Safoof-e-Hazim wa Kasir-e-Riyah (سفوف ہاضم و کاسر ریاح)', form: 'Safoof (Herbal Powder)', strength: '3g Post-Lunch & Dinner', frequency: 'BD', morning: '—', noon: '3g (1/2 tsp)', night: '3g (1/2 tsp)', anupan: 'Taza Paani (Fresh water)', axis: 'Gastrointestinal', track: 'SELF_NUSKHA', ingredients: 'Badiyan 2g, Zira Siyah 1g, Namak Siyah 500mg, Pudina Khushk 1g, Filfil Daraz 250mg', notes: 'Clinician Bespoke Digestive Tonic (خود ساختہ نسخہ)' }
      ];"""

    if old_gastro in js:
        js = js.replace(old_gastro, new_gastro, 1)
        print("✓ Injected Bespoke Self-Nuskha into GastroBalance protocol")

    # 3. Update cephalic in applyFastProtocol to include Bespoke Self-Nuskha
    old_ceph = """    } else if (protocolId === 'ceph') {
      rx.medicines = [
        { name: 'Itrifal Kishneezi (اطریفل کشنیزی / इतरीफ़ल किशनीज़ी)', form: 'Itrifal', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g', anupan: 'Warm milk / water', axis: 'Neurologic', track: 'QARABADEEN' },
        { name: 'Sharbat Ustukhuddus (شربت اسطخودوس / शरबत उसतुख़ुद्दूस)', form: 'Sharbat', strength: '20ml BD', frequency: 'BD', morning: '20ml with water', noon: '—', night: '20ml with water', anupan: 'Warm water', axis: 'Neurologic', track: 'QARABADEEN' },
        { name: 'Roghan-e-Banafsha (روغن بنفشہ / रोग़ن बनफ़्शा)', form: 'Roghan', strength: 'Hasb-e-Zaroorat', frequency: 'OD (Bedtime)', morning: '—', noon: '—', night: 'Scalp Massage', anupan: 'Gentle scalp friction', axis: 'Neurologic', track: 'QARABADEEN' },
        { name: 'TensioCalm™ Herbal Elixir', form: 'Liquid Tonic', strength: '10ml at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '10ml', anupan: 'Direct sip with lukewarm water', axis: 'Neurologic', track: 'ZAYVORA_PRODUCT' }
      ];"""

    new_ceph = """    } else if (protocolId === 'ceph') {
      rx.medicines = [
        { name: 'Itrifal Kishneezi (اطریفل کشنیزی / इतरीफ़ल किशनीज़ी)', form: 'Itrifal', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g', anupan: 'Warm milk / water', axis: 'Neurologic', track: 'QARABADEEN' },
        { name: 'Roghan-e-Banafsha (روغن بنفشہ / रोग़ن बनफ़्شا)', form: 'Roghan', strength: 'Hasb-e-Zaroorat', frequency: 'OD (Bedtime)', morning: '—', noon: '—', night: 'Scalp Massage', anupan: 'Gentle scalp friction', axis: 'Neurologic', track: 'QARABADEEN' },
        { name: 'TensioCalm™ Herbal Elixir', form: 'Liquid Tonic', strength: '10ml at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '10ml', anupan: 'Direct sip with lukewarm water', axis: 'Neurologic', track: 'ZAYVORA_PRODUCT' },
        { name: 'Bespoke Safoof-e-Muqawwi-e-Dimagh wa Asab (سفوف مقوی دماغ و اعصاب)', form: 'Safoof (Fine Powder)', strength: '3g with Milk', frequency: 'OD (Morning)', morning: '3g', noon: '—', night: '—', anupan: 'Neem Garam Doodh (Warm Milk)', axis: 'Neurologic', track: 'SELF_NUSKHA', ingredients: 'Ustukhuddus 2g, Kishneez Khushk 2g, Maghz Badam Shireen 3g, Brahmi 1g', notes: 'Clinician Bespoke Neuro-Tonic (خود ساختہ نسخہ)' }
      ];"""

    if old_ceph in js:
        js = js.replace(old_ceph, new_ceph, 1)
        print("✓ Injected Bespoke Self-Nuskha into Cephalic protocol")

    # 4. Enhance Prescription Slip track badge for SELF_NUSKHA
    old_track_display = "${m.form || ''} • ${m.track || 'Unani Formulary'}"
    new_track_display = "${m.form || ''} • ${m.track === 'SELF_NUSKHA' ? 'Bespoke Matab Nuskha (خود ساختہ نسخہ)' : m.track === 'ZAYVORA_PRODUCT' ? 'ZAYVORA Sovereign Product' : 'Classical Qarabadeen'}"
    if old_track_display in js:
        js = js.replace(old_track_display, new_track_display, 1)
        print("✓ Enhanced slip track display to show Bespoke Matab Nuskha (خود ساختہ نسخہ)")

    with open(CORE_JS, "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == "__main__":
    update_fast_protocols()
