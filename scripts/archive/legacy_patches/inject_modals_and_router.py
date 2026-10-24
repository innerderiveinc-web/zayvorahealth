import re

with open("docs/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Modals to inject right after help-modal
modals_html = """
  <!-- ===================================================================== -->
  <!-- GLOBAL SEARCH MODAL (⌘K) -->
  <!-- ===================================================================== -->
  <div id="search-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-start justify-center pt-20 p-4">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-4 space-y-4 shadow-2xl">
      <div class="flex items-center gap-3 border-b border-[var(--border)] pb-3 px-2">
        <span class="text-lg">🔍</span>
        <input id="global-search-input" type="text" oninput="handleGlobalSearch(this.value)" placeholder="Search patients, medicines, clinical protocols, pages..." class="flex-1 bg-transparent text-white text-sm focus:outline-none placeholder-[var(--muted)]" />
        <kbd class="px-2 py-0.5 rounded bg-[var(--background)] text-xs text-[var(--muted)] border border-[var(--border)]">ESC</kbd>
        <button onclick="toggleSearchModal()" class="text-[var(--muted)] hover:text-white">✕</button>
      </div>
      <div id="global-search-results" class="max-h-80 overflow-y-auto space-y-2 text-xs">
        <p class="text-slate-500 text-center py-4">Type to search across patients, medicines, protocols, and 25 website pages...</p>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- CLINICAL NOTIFICATIONS DRAWER / MODAL -->
  <!-- ===================================================================== -->
  <div id="notifications-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-start justify-end p-4">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-md w-full p-5 space-y-4 shadow-2xl mt-12 mr-2">
      <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
        <div class="flex items-center gap-2">
          <span class="text-base">🔔</span>
          <h3 class="font-bold text-white text-sm">Clinical & System Alerts</h3>
          <span id="drawer-notif-count" class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-mono text-[10px] font-bold">3 Active</span>
        </div>
        <button onclick="toggleNotificationsModal()" class="text-[var(--muted)] hover:text-white">✕</button>
      </div>
      <div id="drawer-alerts-list" class="space-y-2.5 max-h-96 overflow-y-auto">
        <!-- Rendered by JS -->
      </div>
      <div class="pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs">
        <button onclick="markAllAlertsRead()" class="text-emerald-400 hover:underline font-semibold">Mark All Acknowledged</button>
        <button onclick="toggleNotificationsModal()" class="px-3 py-1.5 rounded-lg bg-[var(--background)] text-white hover:bg-slate-700">Close</button>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- REGISTER NEW PATIENT MODAL -->
  <!-- ===================================================================== -->
  <div id="add-patient-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
      <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
        <h3 class="font-bold text-base text-white flex items-center gap-2">
          <span>👤 Register New Patient (OPD Intake)</span>
        </h3>
        <button onclick="toggleAddPatientModal()" class="text-[var(--muted)] hover:text-white">✕</button>
      </div>
      <form onsubmit="handleRegisterNewPatient(event)" class="space-y-3 text-xs">
        <div>
          <label class="block text-[var(--muted)] mb-1">Full Legal Name</label>
          <input id="new-pat-name" required placeholder="e.g. Zaid Khan" class="w-full px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[var(--muted)] mb-1">Age</label>
            <input id="new-pat-age" type="number" required placeholder="42" class="w-full px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
          </div>
          <div>
            <label class="block text-[var(--muted)] mb-1">Gender</label>
            <select id="new-pat-gender" class="w-full px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-[var(--muted)] mb-1">Phone Number</label>
          <input id="new-pat-phone" required placeholder="+91 97738 82657" class="w-full px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
        </div>
        <div>
          <label class="block text-[var(--muted)] mb-1">Primary Clinical Complaint</label>
          <input id="new-pat-complaint" required placeholder="e.g. Chronic knee pain with morning cold intolerance" class="w-full px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
        </div>
        <div>
          <label class="block text-[var(--muted)] mb-1">Baseline Mizaj Assessment</label>
          <select id="new-pat-mizaj" class="w-full px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400">
            <option value="Barid Balghami (Cold-Phlegmatic)">Barid Balghami (Cold-Phlegmatic)</option>
            <option value="Har Safrawi (Hot-Choleric)">Har Safrawi (Hot-Choleric)</option>
            <option value="Har Damawi (Hot-Sanguine)">Har Damawi (Hot-Sanguine)</option>
            <option value="Barid Sawdawi (Cold-Melancholic)">Barid Sawdawi (Cold-Melancholic)</option>
          </select>
        </div>
        <div class="pt-3 border-t border-[var(--border)] flex justify-end gap-2">
          <button type="button" onclick="toggleAddPatientModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-[var(--muted)] hover:text-white">Cancel</button>
          <button type="submit" class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold">Register & Admit to Queue</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- PRINTABLE CLINICAL SUMMARY & COA MODAL -->
  <!-- ===================================================================== -->
  <div id="report-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
        <div>
          <span class="text-[10px] font-mono font-bold text-emerald-400">21 CFR PART 11 VERIFIED RECORD</span>
          <h3 class="font-bold text-base text-white">Clinical Summary & Certificate of Formulation</h3>
        </div>
        <button onclick="toggleReportModal()" class="text-[var(--muted)] hover:text-white">✕</button>
      </div>
      <div id="report-modal-content" class="bg-[var(--background)] p-5 rounded-xl border border-[var(--border)] space-y-4 text-xs">
        <!-- Rendered by JS -->
      </div>
      <div class="pt-2 flex justify-end gap-2">
        <button onclick="toggleReportModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white">Close</button>
        <button onclick="window.print()" class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow">🖨️ Print / Save PDF</button>
      </div>
    </div>
  </div>
"""

# Insert modals right before </main> or after help-modal
if '<div id="help-modal"' in html:
    parts = html.split('<!-- ===================================================================== -->\n  <!-- CLIENT-SIDE APPLICATION DATA & LOGIC -->')
    if len(parts) == 2:
        html = parts[0] + modals_html + '\n  <!-- ===================================================================== -->\n  <!-- CLIENT-SIDE APPLICATION DATA & LOGIC -->' + parts[1]
        print("✓ Modals injected successfully")

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
