#!/usr/bin/env python3
"""
Deep Comprehensive Audit & Mismatch Fixer for ZAYVORA Health OS
Synchronizes all product doses, packaging forms, and clinical prescribing posology.
"""
import re
import shutil

CORE_JS = "js/zayvora-core.js"

with open(CORE_JS, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Extract authoritative map from herbalsProducts
p_start = text.find("const herbalsProducts = [")
p_end = text.find("// ZAYVORA COMMERCE ENGINE STATE", p_start)
herbals_chunk = text[p_start:p_end]

h_items = re.findall(
    r'\{\s*"id":\s*"([^"]+)",\s*"sku":\s*"([^"]+)",\s*"name":\s*"([^"]+)",\s*'
    r'"unani_name":\s*"([^"]+)",\s*"category":\s*"([^"]+)",\s*"price":\s*(\d+).*?'
    r'"dosage":\s*"([^"]+)".*?"form":\s*"([^"]+)"',
    herbals_chunk,
    re.DOTALL,
)
sku_map = {item[1]: {"dosage": item[6], "form": item[7]} for item in h_items}
print(f"Authoritative products mapped from herbalsProducts: {len(sku_map)}")

# 2. Update ZAYVORA_PRODUCTS_16 array
p16_start = text.find("const ZAYVORA_PRODUCTS_16 = [")
p16_end = text.find("const ZAYVORA_PRODUCTS_32 = ZAYVORA_PRODUCTS_16;", p16_start)
chunk_16 = text[p16_start:p16_end]

def replace_prod(m):
    prod_block = m.group(0)
    sku_m = re.search(r'"(?:id|code)":\s*"(ZAY-\d+)"', prod_block)
    if not sku_m:
        return prod_block
    sku = sku_m.group(1)
    if sku in sku_map:
        correct_dose = sku_map[sku]["dosage"]
        correct_form = sku_map[sku]["form"]
        prod_block = re.sub(r'"form":\s*"[^"]+"', f'"form": "{correct_form}"', prod_block)
        prod_block = re.sub(r'"dose":\s*"[^"]+"', f'"dose": "{correct_dose}"', prod_block)
    return prod_block

updated_chunk_16 = re.sub(r'\{\s*"id":\s*"ZAY-\d+".*?\n\s*\}', replace_prod, chunk_16, flags=re.DOTALL)
text = text[:p16_start] + updated_chunk_16 + text[p16_end:]

# 3. Update addPrescriptionMedicine to handle rendered dose properly
old_rx_fn = """    function addPrescriptionMedicine(item) {
      const rx = state.prescriptions[0];
      if (!rx.medicines) rx.medicines = [];
      rx.medicines.push(item);
      if (!rx.medications) rx.medications = [];
      rx.medications.push({
        name: item.name,
        dose: `${item.strength || item.dose || '5g'} ${item.frequency || 'Twice daily'} with ${item.anupan || 'warm water'}`,
        role: item.track === 'SELF_NUSKHA' ? 'Clinician Bespoke Compounding' : item.track === 'GMP_PRODUCT' ? 'ZAYVORA GMP Product' : 'Classical Qarabadeen Compound',
        note: item.notes || item.ingredients || 'Prescribed by clinician'
      });
      showNotification(`✓ Added "${item.name}" to Prescription RX-2026-0441.`, 'success');
      jumpToSection(11);
    }"""

new_rx_fn = """    function addPrescriptionMedicine(item) {
      const rx = state.prescriptions[0];
      if (!rx.medicines) rx.medicines = [];
      rx.medicines.push(item);
      if (!rx.medications) rx.medications = [];

      let renderedDose = item.dose || '';
      if (!renderedDose) {
        if (item.strength && item.frequency) {
          renderedDose = `${item.strength} ${item.frequency} with ${item.anupan || 'warm water'}`;
        } else {
          renderedDose = `${item.strength || '1 Unit'} with ${item.anupan || 'warm water'}`;
        }
      }
      rx.medications.push({
        name: item.name,
        dose: renderedDose,
        role: item.track === 'SELF_NUSKHA' ? 'Clinician Bespoke Compounding' : item.track === 'GMP_PRODUCT' ? 'ZAYVORA GMP Product' : 'Classical Qarabadeen Compound',
        note: item.notes || item.ingredients || 'Prescribed by clinician'
      });
      showNotification(`✓ Added "${item.name}" to Prescription RX-2026-0441.`, 'success');
      jumpToSection(11);
    }"""

if old_rx_fn in text:
    text = text.replace(old_rx_fn, new_rx_fn)
    print("addPrescriptionMedicine function modernized successfully!")

# 4. Refine prescribed item parameters in renderZayvoraProductsCatalog
old_rx_btn_pattern = re.compile(
    r'<button onclick=\'addPrescriptionMedicine\(\$\{[^}]*name:\s*p\.name,[^}]*\}\)\);\s*toggleZayvoraProductsModal\(\);\'\s*class="px-3\.5 py-1\.5 bg-amber-600[^"]*">',
    re.DOTALL,
)

new_rx_btn = """<button onclick='addPrescriptionMedicine({
              name: p.name,
              form: p.form,
              dose: p.dose,
              strength: p.form.includes("Capsule") ? "1-2 Capsules" : p.form.includes("Tablet") ? "1-2 Tablets" : p.form.includes("Sachet") ? "1 Sachet" : "1 Unit",
              frequency: p.dose.toLowerCase().includes("twice") ? "Twice daily" : "Daily",
              anupan: p.dose.toLowerCase().includes("milk") ? "Warm milk" : "Lukewarm water",
              duration: "30 Days",
              track: "GMP_PRODUCT",
              axis: p.axis,
              ingredients: p.actives,
              notes: `${p.code} • ${p.category} • BMR: ${p.bmr}`
            }); toggleZayvoraProductsModal();' class="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-[11px] font-bold shadow transition flex items-center gap-1">"""

if old_rx_btn_pattern.search(text):
    text = old_rx_btn_pattern.sub(new_rx_btn, text)
    print("Catalog Prescribe button posology parser modernized successfully!")

# 5. Fix FEFO Allocation batch card
text = text.replace(
    '<div class="text-[11px] text-[var(--muted)] mt-0.5">5g twice daily with lukewarm milk • Qty: 200g Granules</div>',
    '<div class="text-[11px] text-[var(--muted)] mt-0.5">1 stick sachet (10g) twice daily with lukewarm milk • Qty: 1 Box (30 Stick Sachets)</div>',
)

# 6. Fix Audio Posology Card & Voice Strings
text = text.replace(
    '<h3 class="font-bold text-white text-base">ManiVital Pro Granules (5g Twice Daily)</h3>',
    '<h3 class="font-bold text-white text-base">ManiVital Pro Granules (1 Stick Sachet Twice Daily)</h3>',
)

old_audio_urdu = "محترم مریض، السلام علیکم۔ یہ دوا صبح اور شام کھانا کھانے کے بعد، آدھا چمچ نیم گرم دودھ یا تازہ پانی کے ساتھ نوش فرمائیں۔ کھٹی، تلی ہوئی اور ٹھنڈی چیزوں سے پرہیز رکھیں۔ اللہ تعالیٰ آپ کو صحت اور شفائے کاملہ عطا فرمائے۔"
new_audio_urdu = "محترم مریض، السلام علیکم۔ یہ دوا (1 ساشے) صبح اور شام کھانا کھانے کے بعد، نیم گرم دودھ کے ساتھ نوش فرمائیں۔ کھٹی، تلی ہوئی اور ٹھنڈی چیزوں سے پرہیز رکھیں۔ اللہ تعالیٰ آپ کو صحت اور شفائے کاملہ عطا فرمائے۔"
text = text.replace(old_audio_urdu, new_audio_urdu)

old_audio_hindi = "नमस्ते। यह औषधि सुबह और शाम भोजन के बाद, आधा चम्मच गुनगुने दूध या ताज़े पानी के साथ लें। खट्टी, तली हुई और ठंडी चीज़ों से परहेज़ रखें। ईश्वर आपको शीघ्र स्वास्थ्य लाभ दे।"
new_audio_hindi = "नमस्ते। यह औषधि (1 सैशे) सुबह और शाम भोजन के बाद, गुनगुने दूध के साथ लें। खट्टी, तली हुई और ठंडी चीज़ों से परहेज़ रखें। ईश्वर आपको शीघ्र स्वास्थ्य लाभ दे।"
text = text.replace(old_audio_hindi, new_audio_hindi)

old_audio_en = "Hello. Please take half a teaspoon twice daily after meals with lukewarm milk or fresh water. Strictly avoid cold drinks, sour and fried foods. Wishing you a speedy recovery."
new_audio_en = "Hello. Please take 1 stick sachet dissolved in warm milk twice daily after meals. Strictly avoid cold drinks, sour and fried foods. Wishing you a speedy recovery."
text = text.replace(old_audio_en, new_audio_en)

# 7. Fix Mobile Screen ManiVital prescription card
text = text.replace(
    '<p class="text-slate-300 text-[11px]">5g twice daily with lukewarm milk.</p>',
    '<p class="text-slate-300 text-[11px]">1 stick sachet (10g) twice daily with lukewarm milk.</p>',
)

with open(CORE_JS, "w", encoding="utf-8") as f:
    f.write(text)
print("js/zayvora-core.js completely updated and saved!")

# 8. Synchronize HTML files so all routes serve the modern architecture
# index.html is the modular source of truth
for target_html in ["app.html", "docs/app.html", "docs/index.html"]:
    shutil.copyfile("index.html", target_html)
    print(f"Synchronized {target_html} from index.html!")

print("All mismatches audit and synchronization completed successfully!")
