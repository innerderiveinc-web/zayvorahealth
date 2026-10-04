#!/usr/bin/env python3
"""
Upgrade ZAYVORA Products Catalog Page:
1. Category Filter Pills & Real-Time Search Bar
2. B2B Doctor Wholesale Banner (40% clinic margin)
3. Instant '⚡ Buy Now', '+ Cart', and '🔍 Quick View' on all 32 cards
4. MRP Strikethrough, Special Price, and 15% Subscribe & Save price
"""

CORE_FILE = "js/zayvora-core.js"

with open(CORE_FILE, "r", encoding="utf-8") as f:
    js = f.read()

OLD_PRODUCTS_TAB = '''      // TAB: PRODUCTS
      if (state.tab === 'products') {
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="max-w-6xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                  <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Botanical Therapeutics</span>
                  <h1 class="text-3xl font-extrabold text-white mt-1">ZAYVORA Herbals Portfolio</h1>
                  <p class="text-xs text-[var(--muted)] mt-1">AYUSH-GMP certified, HPLC active fingerprinted, Schedule E(1) Mudabbar detoxified.</p>
                </div>
                <div class="flex items-center gap-3 flex-wrap">
                  <a href="/formulary.pdf" target="_blank" download="ZAYVORA_32_Master_Products_Formulary.pdf" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700 shadow flex items-center gap-2 transition cursor-pointer">
                    <span>📄</span> Download 32-Product Formulary (PDF)
                  </a>
                  <button onclick="viewWebsitePage('contact')" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                    Consult Tabeeb for Prescription
                  </button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              ${herbalsProducts.map(p => `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col justify-between space-y-4 hover:border-emerald-500/50 transition">
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">${p.category}</span>
                      <span class="text-base font-bold text-white">₹${p.price}</span>
                    </div>
                    <h3 class="text-sm font-bold text-white">${p.name}</h3>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${p.desc}</p>
                    <div class="text-[11px] text-slate-300 bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)] space-y-1">
                      <div><strong class="text-emerald-400">Dose:</strong> ${p.dosage}</div>
                      <div><strong class="text-slate-400">Indications:</strong> ${p.indications}</div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
                    <span class="text-[10px] text-emerald-400 font-semibold">✓ HPLC Fingerprinted</span>
                    <button onclick="addToHerbalsCart('${p.id}')" class="px-4 py-1.5 bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold rounded-lg transition shadow">
                      + Add to Cart
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }'''

NEW_PRODUCTS_TAB = '''      // TAB: PRODUCTS
      if (state.tab === 'products') {
        const subnav = getWebsiteHubSubnav(state.tab);
        if (!window.productFilterCategory) window.productFilterCategory = 'ALL';
        if (!window.productSearchQuery) window.productSearchQuery = '';

        const filterCategory = window.productFilterCategory;
        const searchQuery = window.productSearchQuery.toLowerCase().trim();

        const filteredProds = herbalsProducts.filter(p => {
          const matchCat = filterCategory === 'ALL' || (p.category && p.category.toLowerCase().includes(filterCategory.toLowerCase()));
          const matchSearch = !searchQuery || 
            (p.name && p.name.toLowerCase().includes(searchQuery)) ||
            (p.unani_name && p.unani_name.toLowerCase().includes(searchQuery)) ||
            (p.sku && p.sku.toLowerCase().includes(searchQuery)) ||
            (p.indications && p.indications.toLowerCase().includes(searchQuery));
          return matchCat && matchSearch;
        });

        container.innerHTML = `
          <div class="max-w-6xl mx-auto space-y-8 pb-12">
            ${subnav}

            <!-- Header Card -->
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                  <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold uppercase tracking-wider mb-1.5">
                    <span>🌿</span> AYUSH GMP Standardized Botanical Dispensary
                  </div>
                  <h1 class="text-2xl sm:text-3xl font-black text-white">ZAYVORA 32-Formulation Master Dispensary</h1>
                  <p class="text-xs text-[var(--muted)] mt-1">Conceived &amp; Architected by Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU). HPLC Fingerprinted • Heavy Metals &lt;0.02 ppm • Direct Cold-Chain FEFO Dispatch.</p>
                </div>
                <div class="flex items-center gap-3 flex-wrap shrink-0">
                  <button onclick="toggleCheckoutModal()" class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-2 cursor-pointer">
                    <span>🛍️</span> View Dispensary Cart (${herbalsCart.length})
                  </button>
                  <a href="/formulary.pdf" target="_blank" download="ZAYVORA_32_Master_Products_Formulary.pdf" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700 shadow flex items-center gap-2 transition cursor-pointer">
                    <span>📄</span> Download Formulary (PDF)
                  </a>
                </div>
              </div>

              <!-- B2B Doctor Wholesale Banner -->
              <div class="mt-4 p-4 rounded-2xl bg-gradient-to-r from-amber-950/60 via-slate-900 to-slate-950 border border-amber-500/40 flex flex-col sm:flex-row justify-between items-center gap-3">
                <div class="flex items-center gap-3">
                  <span class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-lg shrink-0">🏛️</span>
                  <div>
                    <strong class="text-white text-xs block">Are you a Licensed Clinician / Matab Practitioner?</strong>
                    <span class="text-[11px] text-amber-300">Get 40% Professional Clinic Margin on bulk clinic dispensing packs. Instant NCISM verification.</span>
                  </div>
                </div>
                <button onclick="toggleB2BWholesaleModal(true)" class="px-4 py-2 bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-400 text-slate-950 font-black text-xs rounded-xl shadow transition shrink-0 cursor-pointer">
                  Apply for 40% B2B Margin &rarr;
                </button>
              </div>

              <!-- Search Bar & Filters -->
              <div class="pt-2 flex flex-col sm:flex-row gap-3">
                <div class="relative flex-1">
                  <span class="absolute left-3.5 top-2.5 text-slate-400 text-xs">🔍</span>
                  <input type="text" id="product-search-input" value="${window.productSearchQuery || ''}" oninput="window.productSearchQuery = this.value; renderWebsiteApp(document.getElementById('workspace-container'));" placeholder="Search 32 formulations by name, herb, indication, or SKU (e.g. ArthroEase, Boswellia, Sugar)..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
                </div>
                <div class="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 text-xs shrink-0">
                  <button onclick="window.productFilterCategory='ALL'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='ALL' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">All (32)</button>
                  <button onclick="window.productFilterCategory='Metabolic'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Metabolic' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Metabolic</button>
                  <button onclick="window.productFilterCategory='Neuro'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Neuro' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Neuro</button>
                  <button onclick="window.productFilterCategory='Musculo'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Musculo' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Joints</button>
                  <button onclick="window.productFilterCategory='Hepato'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Hepato' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Liver &amp; Kidney</button>
                  <button onclick="window.productFilterCategory='Vitality'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Vitality' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Vitality</button>
                </div>
              </div>
            </div>

            <!-- Product Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              ${filteredProds.map(p => {
                const subPrice = Math.round(p.price * 0.85);
                return `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col justify-between space-y-4 hover:border-emerald-500/50 hover:shadow-xl transition group">
                  <div class="space-y-2.5">
                    <div class="flex justify-between items-center">
                      <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 uppercase tracking-wider">${p.category}</span>
                      <span class="text-xs font-mono text-slate-400">${p.sku}</span>
                    </div>

                    <div>
                      <h3 class="text-base font-bold text-white group-hover:text-emerald-300 transition-colors">${p.name}</h3>
                      <p class="text-[11px] font-mono text-emerald-400/90 mt-0.5">${p.unani_name || ''}</p>
                    </div>

                    <p class="text-xs text-[var(--muted)] leading-relaxed line-clamp-2">${p.desc}</p>

                    <div class="text-[11px] text-slate-300 bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] space-y-1">
                      <div><strong class="text-emerald-400">Clinical Indication:</strong> <span class="text-slate-200">${p.indications}</span></div>
                      <div><strong class="text-teal-400">Posology &amp; Badraqa:</strong> <span class="text-slate-300">${p.dosage}</span></div>
                    </div>

                    <!-- Commercial Pricing Breakdown -->
                    <div class="pt-2 border-t border-slate-800/80 flex justify-between items-end">
                      <div>
                        <span class="text-[10px] text-slate-500 line-through">MRP: ₹${p.price + 200}</span>
                        <div class="text-lg font-black font-mono text-emerald-400">₹${p.price.toLocaleString('en-IN')}</div>
                        <span class="text-[10px] text-emerald-500 font-bold">₹${subPrice}/mo on Subscribe (Save 15%)</span>
                      </div>
                      <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/30 text-emerald-300">GST 5% Incl.</span>
                    </div>
                  </div>

                  <!-- 3 High-Impact Action CTAs -->
                  <div class="pt-3 border-t border-[var(--border)] space-y-2">
                    <div class="grid grid-cols-2 gap-2">
                      <button onclick="addToHerbalsCart('${p.id}'); toggleCheckoutModal();" class="py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-1 cursor-pointer">
                        <span>⚡</span> Buy Now
                      </button>
                      <button onclick="addToHerbalsCart('${p.id}')" class="py-2.5 bg-slate-800 hover:bg-slate-700 text-emerald-300 font-bold text-xs rounded-xl border border-slate-700 transition flex items-center justify-center gap-1 cursor-pointer">
                        <span>+</span> Add to Cart
                      </button>
                    </div>
                    <button onclick="openProductQuickView('${p.sku}')" class="w-full py-1.5 text-center text-[11px] text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-lg transition border border-transparent hover:border-slate-700 cursor-pointer">
                      🔍 View Clinical Monograph &amp; COA &rarr;
                    </button>
                  </div>
                </div>
              `}).join('')}
            </div>
          </div>
        `;
        return;
      }'''

if OLD_PRODUCTS_TAB in js:
    js = js.replace(OLD_PRODUCTS_TAB, NEW_PRODUCTS_TAB)
    print("✓ Successfully upgraded Products Catalog page in js/zayvora-core.js")
else:
    print("! Could not find OLD_PRODUCTS_TAB in js/zayvora-core.js")

with open(CORE_FILE, "w", encoding="utf-8") as f:
    f.write(js)

print("Upgrade products script finished.")
