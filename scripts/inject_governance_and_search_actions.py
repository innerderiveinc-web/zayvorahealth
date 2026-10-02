import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update search items in handleGlobalSearch to include suggested clinical quick actions
old_search_items_start = 'const searchItems = ['
new_search_items = """const searchItems = [
        // Suggested Clinical Actions (Prompt Section 12)
        { title: '🩺 New Encounter / Clinical Desk', category: 'Action • Start Patient Consultation', type: 'protocol', action: () => { switchRole('doctor'); switchTab('consultation'); toggleSearchModal(); } },
        { title: '⏱️ Open Clinic OPD Queue', category: 'Action • View Live Waiting Tokens', type: 'protocol', action: () => { switchRole('clinic'); switchTab('queue'); toggleSearchModal(); } },
        { title: '🤖 Consult Hakeem Sahab AI Copilot', category: 'Action • Clinical Decision Support', type: 'protocol', action: () => { switchRole('doctor'); switchTab('consultation'); toggleSearchModal(); toggleHakeemDrawer(true); } },
        { title: '🛡️ Inspect Safety Rails & Mudabbar', category: 'Action • Safety Firewall Check', type: 'protocol', action: () => { switchRole('pharmacy'); switchTab('detox'); toggleSearchModal(); } },
        { title: '📚 Search ZKB Pharmacopoeia & Monographs', category: 'Action • UPI & Classical Literature', type: 'protocol', action: () => { switchRole('doctor'); switchTab('knowledge'); toggleSearchModal(); } },
        { title: '💊 Open Nuskha Composer & Preflight', category: 'Action • Formulate Multi-Pillar Rx', type: 'protocol', action: () => { switchRole('doctor'); switchTab('consultation'); toggleSearchModal(); jumpToSection(11); } },
        { title: '🔬 View RWE Observational Registries', category: 'Action • Real-World Evidence Hub', type: 'protocol', action: () => { switchRole('research'); switchTab('studies'); toggleSearchModal(); } },"""

if 'Action • Start Patient Consultation' not in html:
    html = html.replace(old_search_items_start, new_search_items, 1)
    print("✓ Added Suggested Clinical Quick Actions to Command Palette ⌘K")

# 2. Add 12-Stage Knowledge Governance Workspace into doctor knowledge tab
governance_workspace_html = """
            <!-- 12-STAGE KNOWLEDGE GOVERNANCE & PROMOTION PIPELINE (PROMPT SECTION 24) -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm space-y-5">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="text-lg">⚖️</span>
                    <h3 class="text-base font-bold text-white">12-Stage Knowledge Governance & AI Promotion Pipeline</h3>
                    <span class="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-mono text-[10px] border border-purple-500/30">Quorum 3/3 Certified</span>
                  </div>
                  <p class="text-xs text-[var(--muted)] mt-0.5">Strict separation of research candidates from clinical-approved knowledge. Unpromoted items cannot alter prescribing rules.</p>
                </div>
                <span class="text-[11px] text-emerald-400 font-mono font-bold">ZKB Governance Protocol v5.2</span>
              </div>

              <!-- 12-Stage Visual Progress Bar -->
              <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2 text-xs">
                <span class="text-[10px] font-bold text-[var(--muted)] uppercase tracking-wider block">Canonical Review Lifecycle</span>
                <div class="flex items-center gap-1 overflow-x-auto pb-1 text-[10px] font-mono scrollbar-thin">
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">01. Candidate</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">02. Identity</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">03. Source Match</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">04. Classical Verified</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">05. Pharmacopoeia</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">06. Pharmacognosy</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">07. Evidence E0-E6</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">08. Safety Rail</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">09. Regulatory</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">10. Clinician Signoff</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-emerald-500/30 text-emerald-200 border border-emerald-500/50 font-bold whitespace-nowrap">11. Approved</span>
                  <span class="text-slate-500">→</span>
                  <span class="px-2 py-1 rounded bg-purple-500/30 text-purple-200 border border-purple-500/50 font-bold whitespace-nowrap">12. AI Available</span>
                </div>
              </div>

              <!-- Two Distinct Candidate Review Cards -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                
                <!-- Card 1: Approved Knowledge -->
                <div class="p-4 rounded-2xl bg-[var(--background)] border-2 border-emerald-500/40 space-y-3">
                  <div class="flex justify-between items-start">
                    <span class="px-2 py-0.5 rounded font-bold text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                      ✓ CLINICAL APPROVED • STAGE 12/12
                    </span>
                    <span class="text-[10px] font-mono text-emerald-400">AI PROMOTED</span>
                  </div>
                  <div>
                    <h4 class="font-bold text-white text-sm">Zanjabeel Extract Fraction B (*Zingiber officinale*)</h4>
                    <p class="text-[11px] text-[var(--muted)]">ZKB Canonical ID: ZMF-042 • UPI Vol II, p. 89 • HPLC 6-gingerol > 5.2%</p>
                  </div>
                  <div class="space-y-1 text-[11px] text-slate-300 border-t border-[var(--border)] pt-2">
                    <div>Reviewer: <strong class="text-white">Dr. K. Saxena & Dr. Tariq Mansoor</strong></div>
                    <div>Decision: <strong class="text-emerald-400">Unanimous 3/3 Quorum Passed (2026-06-14)</strong></div>
                    <div>AI Retrieval Status: <strong class="text-purple-300">Active in Hakeem Sahab™ Decision Graph</strong></div>
                  </div>
                </div>

                <!-- Card 2: Research Candidate (Not Approved for Clinical Use) -->
                <div class="p-4 rounded-2xl bg-[var(--background)] border-2 border-amber-500/40 space-y-3">
                  <div class="flex justify-between items-start">
                    <span class="px-2 py-0.5 rounded font-bold text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/40">
                      🔬 RESEARCH CANDIDATE • STAGE 06/12
                    </span>
                    <span class="text-[10px] font-mono text-rose-400 font-bold">AI PRESCRIBING BLOCKED</span>
                  </div>
                  <div>
                    <h4 class="font-bold text-white text-sm">Asaroon Phyto-Isolate (*Asarum europaeum*)</h4>
                    <p class="text-[11px] text-[var(--muted)]">ZKB Candidate ID: ZKB-CAND-2026-14 • Classical Source: Kitab al-Hawi</p>
                  </div>
                  <div class="space-y-1 text-[11px] text-slate-300 border-t border-[var(--border)] pt-2">
                    <div>Current Stage: <strong class="text-amber-300">06. Pharmacognosy Testing (Aristolochic Acid GC-MS)</strong></div>
                    <div>Reviewer: <strong class="text-white">Dr. Arshad Qureshi, Manufacturing QC</strong></div>
                    <div>Clinical Governance Barrier: <strong class="text-rose-400">Strictly isolated in Research Staging partition</strong></div>
                  </div>
                </div>

              </div>

            </div>"""

# Insert right after the 3 monograph cards in doctor knowledge tab
marker = '<!-- Mufradat Monographs Grid -->'
target_search = '</div>\n\n            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">'
if '12-Stage Knowledge Governance & AI Promotion Pipeline' not in html:
    # Find the closing tag of that grid
    idx_k = html.find("state.tab === 'knowledge'")
    idx_grid = html.find('<div class="grid grid-cols-1 md:grid-cols-3 gap-6">', idx_k)
    # Find the matching </div> for this grid
    idx_grid_end = html.find('</div>\n          </div>', idx_grid)
    if idx_grid_end != -1:
        html = html[:idx_grid_end] + '</div>' + governance_workspace_html + html[idx_grid_end+6:]
        print("✓ Injected 12-Stage Knowledge Governance Workspace into Doctor Knowledge Tab")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ Saved updated index.html and docs/index.html")
