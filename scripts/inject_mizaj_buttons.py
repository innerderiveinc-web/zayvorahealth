import os

path = "js/zayvora-core.js"
with open(path, "r", encoding="utf-8") as f:
    js = f.read()

target = "              <!-- Nabz Harakat -->\n              <div class=\"space-y-1\">"

mizaj_block = """              <!-- 4-BUTTON TACTILE MIZAJ PICKER -->
              <div class="space-y-1.5 pb-2 border-b border-slate-800">
                <span class="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Mizaj-e-Mareez (طبیعی / غیر طبیعی مزاج):</span>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                  <button onclick="selectFastMizaj('Damawi (Sanguine / خونی)')" data-mizaj="Damawi (Sanguine / خونی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Damawi')) ? 'bg-rose-600 border-rose-400 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>🔴</span> Damawi (خون)
                  </button>
                  <button onclick="selectFastMizaj('Balghami (Phlegmatic / بلغمی)')" data-mizaj="Balghami (Phlegmatic / بلغمی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Balghami')) ? 'bg-cyan-600 border-cyan-400 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>⚪</span> Balghami (بلغم)
                  </button>
                  <button onclick="selectFastMizaj('Safrawi (Choleric / صفراوی)')" data-mizaj="Safrawi (Choleric / صفراوی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Safrawi')) ? 'bg-amber-600 border-amber-400 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>🟡</span> Safrawi (صفراء)
                  </button>
                  <button onclick="selectFastMizaj('Sawdawi (Melancholic / سوداوی)')" data-mizaj="Sawdawi (Melancholic / سوداوی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Sawdawi')) ? 'bg-slate-700 border-slate-500 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>⚫</span> Sawdawi (سوداء)
                  </button>
                </div>
              </div>\n\n"""

if "fast-mizaj-btn" not in js:
    if target in js:
        js = js.replace(target, mizaj_block + target, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(js)
        print("SUCCESS: Added 4-button tactile Mizaj picker!")
    else:
        print("Target string not found in js")
else:
    print("fast-mizaj-btn already present in js")
