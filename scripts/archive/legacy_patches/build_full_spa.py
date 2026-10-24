import re
import os

with open("docs/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the showNotification calls on prototype buttons with real working functions:
content = content.replace("showNotification('Opening Add Patient Modal...')", "openAddPatientModal()")
content = content.replace("showNotification('Hakeem Sahab AI Doctor Copilot ready in panel below.')", "focusAiCopilot()")
content = content.replace("showNotification('Generating Clinical Outcomes Audit PDF...')", "openReportModal()")
content = content.replace("showNotification('Reviewing Drug/Herb interaction for Azaraqi...')", "toggleNotificationsModal()")
content = content.replace("showNotification('Alert 1 Acknowledged by Dr. Irfan.')", "acknowledgeAlert('ALT-1')")
content = content.replace("showNotification('Alert 2 Acknowledged by Dr. Irfan.')", "acknowledgeAlert('ALT-2')")
content = content.replace("showNotification('COA Downloaded for BMR-2026-MVP-09')", "openCoaModal('BMR-2026-MVP-09')")
content = content.replace("showNotification('Mudabbar Protocol Signed & Verified')", "approveDetoxStage(this)")
content = content.replace("showNotification('Batch In-Process Sample Queued for Lab')", "queueSpectrometry(this)")

# Update footer links to call viewWebsitePage
content = content.replace(
    """<a href="javascript:void(0)" onclick="showNotification('Support Desk: support@zayvora.health • +91 97738 82657')" class="hover:text-white transition-colors">Contact Support</a>""",
    """<a href="javascript:void(0)" onclick="viewWebsitePage('contact')" class="hover:text-white transition-colors">Contact Support</a>"""
)
content = content.replace(
    """<a href="javascript:void(0)" onclick="showNotification('Privacy Policy: 100% HIPAA, DISHA, DPDP, ABDM compliant.')" class="hover:text-white transition-colors">Privacy Policy</a>""",
    """<a href="javascript:void(0)" onclick="viewWebsitePage('privacy')" class="hover:text-white transition-colors">Privacy Policy</a>"""
)
content = content.replace(
    """<a href="javascript:void(0)" onclick="showNotification('Terms of Clinical Telemedicine Service & Non-Delegable Clinician Gate.')" class="hover:text-white transition-colors">Terms of Service</a>""",
    """<a href="javascript:void(0)" onclick="viewWebsitePage('terms')" class="hover:text-white transition-colors">Terms of Service</a>"""
)
content = content.replace(
    """<a href="javascript:void(0)" onclick="showNotification('Data Protection: AES-256-GCM PHI encryption at rest & TLS 1.3 in transit.')" class="hover:text-white transition-colors">Data Protection</a>""",
    """<a href="javascript:void(0)" onclick="viewWebsitePage('privacy')" class="hover:text-white transition-colors">Data Protection</a>"""
)

# Replace AI Copilot ask button with live clinical reasoning
content = content.replace(
    """<button onclick="showNotification('Hakeem AI Copilot: Su-e-Mizaj Barid Balghami identified. Prescriptions require Dr. Irfan signature.'); document.getElementById('ai-quick-input').value='';" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition">Ask</button>""",
    """<button onclick="askHakeemAI()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition">Ask Hakeem</button>"""
)
content = content.replace(
    """<button onclick="showNotification('Analyzing Hamza Farooqi: Barid Balghami dyscrasia along knee joint axis.')" class="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-slate-300 hover:border-teal-400">⚡ Analyze Hamza</button>""",
    """<button onclick="askHakeemAI('Analyze Hamza Farooqi knee dyscrasia')" class="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-slate-300 hover:border-teal-400">⚡ Analyze Hamza</button>"""
)
content = content.replace(
    """<button onclick="showNotification('Suggested Protocol: Tanqiya Stage 1 with Munzij-e-Balgham.')" class="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-slate-300 hover:border-teal-400">🌿 Suggest Protocol</button>""",
    """<button onclick="askHakeemAI('Suggest Tanqiya Stage 1 protocol')" class="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-slate-300 hover:border-teal-400">🌿 Suggest Protocol</button>"""
)
content = content.replace(
    """<button onclick="showNotification('Interaction Check: Suranjan + Colchicum. Safe with Kateera Musleh.')" class="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-slate-300 hover:border-teal-400">💊 Check Interactions</button>""",
    """<button onclick="askHakeemAI('Check Suranjan and Colchicum interaction')" class="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-slate-300 hover:border-teal-400">💊 Check Interactions</button>"""
)

# Insert Hakeem AI response container right below #ai-quick-input
old_ai_box = """<div class="flex gap-2">
                  <input id="ai-quick-input" placeholder="Ask symptoms, herbs, or clinical interaction..." class="flex-1 px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-400" />
                  <button onclick="askHakeemAI()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition">Ask Hakeem</button>
                </div>"""

new_ai_box = """<div class="flex gap-2">
                  <input id="ai-quick-input" onkeydown="if(event.key==='Enter') askHakeemAI()" placeholder="Ask symptoms, herbs, or clinical interaction..." class="flex-1 px-3 py-2 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-400" />
                  <button onclick="askHakeemAI()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition">Ask Hakeem</button>
                </div>
                <div id="hakeem-ai-response-box" class="hidden"></div>"""

content = content.replace(old_ai_box, new_ai_box)

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✓ Replaced prototype button stubs with real action calls")
