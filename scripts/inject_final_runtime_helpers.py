with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

helpers_code = '''
    // =========================================================================
    // COMPLETE CLINICAL RUNTIME HELPERS & EVENT CONTROLLERS
    // =========================================================================
    let simulatedPulseRate = 72;
    let coldChainTemp = 19.2;
    let audioPosologyLang = 'ur';
    let isPlayingAudio = false;

    function dispensePharmacyOrder() {
      const btn = document.getElementById('btn-dispense-order');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Dispensed & Pick-up Alert Sent ✓';
        btn.className = 'px-5 py-2.5 rounded-xl bg-gray-500/20 text-gray-400 font-bold cursor-not-allowed';
      }
      if (state.inventory && state.inventory[0]) {
        state.inventory[0].stock = Math.max(0, state.inventory[0].stock - 1);
      }
      showNotification('Prescription dispensed. Stock decremented. Automated pickup SMS dispatched to patient via QSURA.', 'success');
    }

    function setPreviewMizaj(question, value) {
      if (typeof previewMizajAnswers === 'undefined') {
        window.previewMizajAnswers = { temp: 'cold', moisture: 'moist', physique: 'broad', sleep: 'deep' };
      }
      previewMizajAnswers[question] = value;
      renderWebsiteApp(document.getElementById('workspace-container'));
    }

    function setWebsiteStage(idx) {
      activeWebsiteStage = idx;
      renderWebsiteApp(document.getElementById('workspace-container'));
    }

    function setAudioLanguage(lang) {
      audioPosologyLang = lang;
      const audioTexts = {
        ur: "ایک چمچ صبح اور شام کھانے کے بعد نیم گرم دودھ کے ساتھ لیں۔ ٹھنڈے مشروبات اور کھٹی چیزوں سے پرہیز کریں۔",
        hi: "एक चम्मच सुबह और शाम खाना खाने کے बाद गुनगुने दूध के साथ लें। ठंडी चीजों और खट्टी चीजों से परहेज करें।",
        en: "Take one teaspoon twice daily after breakfast and dinner with lukewarm milk. Avoid cold drinks."
      };
      const el = document.getElementById('audio-spoken-text');
      if (el) el.textContent = audioTexts[lang] || audioTexts.en;
      showNotification(`Posology audio language set to ${lang.toUpperCase()}`, 'info');
    }

    function toggleAudioPlayback() {
      isPlayingAudio = !isPlayingAudio;
      showNotification(isPlayingAudio ? 'Playing Vernacular Audio Posology...' : 'Audio paused.');
    }

    function triggerNabzPulseTest() {
      simulatedPulseRate = Math.floor(68 + Math.random() * 16);
      showNotification(`Nabz PPG Sensor calibrated. Heart Rate: ${simulatedPulseRate} BPM (Sampling: 100Hz)`);
      if (state.role === 'hardware') {
        renderHardwareApp(document.getElementById('workspace-container'));
      }
    }

    function triggerColdChainTest() {
      coldChainTemp = Math.round((18.5 + Math.random() * 2.5) * 10) / 10;
      showNotification(`Dispensary Environmental Node refreshed: ${coldChainTemp}°C / 48.4% RH (OPTIMAL)`);
      if (state.role === 'hardware') {
        renderHardwareApp(document.getElementById('workspace-container'));
      }
    }
'''

# Find insertion point right before toggleSearchModal
idx = text.find('function toggleSearchModal(')
if idx != -1:
    ls = text.rfind('\n', 0, idx)
    text = text[:ls+1] + helpers_code + text[ls+1:]
    print("Injected helpers before toggleSearchModal!")
else:
    print("Error finding toggleSearchModal!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved index.html and docs/index.html!")
