import re

def patch_files():
    dropdown_html = """              <!-- 21 Master Clinical Protocols Dropdown -->
              <div class="pt-1 flex items-center gap-2">
                <span class="text-[10px] text-purple-300 font-bold whitespace-nowrap hidden sm:inline">Or Select:</span>
                <select id="fast-master-protocols-select" onchange="if(this.value) { applyFastProtocol(this.value); this.selectedIndex = 0; }" class="flex-1 bg-slate-900 border border-purple-500/40 text-purple-200 text-xs rounded-xl px-2.5 py-1.5 focus:outline-none focus:border-purple-400 font-medium cursor-pointer">
                  <option value="" selected>-- Or Choose from 21 Master Protocols --</option>
                  
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
              </div>"""

    for fp in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
        with open(fp, 'r') as f:
            content = f.read()

        # 1. Enhance fast-diagnosis-input with onkeydown Enter and placeholder
        old_input = '<input id="fast-diagnosis-input" type="text" onchange="generateAiNuskhaFromDiagnosis(this.value)" class="flex-1 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-semibold" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">'
        new_input = '<input id="fast-diagnosis-input" type="text" onchange="generateAiNuskhaFromDiagnosis(this.value)" onkeydown="if(event.key===\'Enter\'){event.preventDefault();generateAiNuskhaFromDiagnosis(this.value);}" placeholder="Type any disease in English, Urdu or Roman Urdu (e.g. Fatty Liver, Kidney Stones, Asthma, Sciatica, Bawaseer)..." class="flex-1 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-semibold" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">'
        if old_input in content:
            content = content.replace(old_input, new_input)
            print(f"[✓] Added Enter-key listener & placeholder to fast-diagnosis-input in {fp}")

        # 2. Add Hakeem AI button in master protocols header if not present
        old_proto_hdr = '<span class="font-bold text-white text-xs">Hakeem Sahab™ Clinical CDSS &bull; Master Protocols</span>\n                </div>\n                <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 font-semibold">1-Click Auto-Fill</span>'
        new_proto_hdr = '<span class="font-bold text-white text-xs">Hakeem Sahab™ Clinical CDSS &bull; Master Protocols</span>\n                </div>\n                <div class="flex items-center gap-1.5">\n                  <button type="button" onclick="toggleHakeemDrawer(true)" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px] shadow flex items-center gap-1 cursor-pointer transition" title="Open Hakeem AI Bedside Decision Advisor">\n                    <span>🌿</span> Hakeem AI (طبی مشیر)\n                  </button>\n                  <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 font-semibold hidden sm:inline">1-Click Auto-Fill</span>\n                </div>'
        if old_proto_hdr in content:
            content = content.replace(old_proto_hdr, new_proto_hdr)
            print(f"[✓] Added Hakeem AI (طبی مشیر) button to protocols header in {fp}")

        # 3. Add 21 Master Protocols dropdown right below the 1-click chip buttons
        old_chips_end = '<button onclick="applyFastProtocol(\'skin\')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-rose-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Majun Ushba + Unnab (مصفی خون)">🌿 Skin Detox</button>\n              </div>'
        if old_chips_end in content and 'fast-master-protocols-select' not in content:
            content = content.replace(old_chips_end, old_chips_end + "\n\n" + dropdown_html)
            print(f"[✓] Added 21 Master Protocols Dropdown to {fp}")

        with open(fp, 'w') as f:
            f.write(content)

    print("All patches completed successfully.")

if __name__ == '__main__':
    patch_files()
