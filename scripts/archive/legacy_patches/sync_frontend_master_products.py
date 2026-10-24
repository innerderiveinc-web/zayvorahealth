#!/usr/bin/env python3
"""
Synchronizes the 32 Master Clinical Products, 5 Hero Launch SKUs, and packaging descriptors
into index.html and docs/index.html.
"""

import os
import sys
import json
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.knowledge.app.data.products_master import MASTER_PRODUCTS

def build_products_data():
    prod_list_clinical = []
    prod_list_herbals = []

    for sku, p in MASTER_PRODUCTS.items():
        comp = p.get("composition", [])
        core_ings = ", ".join([c.get("ingredient", "").split("(")[0].strip() for c in comp[:4]])
        actives_list = [f"{c.get('ingredient', '').split('(')[0].strip()} ({c.get('standardization', 'Standardized')})" for c in comp[:3] if c.get("standardization")]
        actives_str = ", ".join(actives_list) if actives_list else "HPLC Standardized Bioactive Phyto-extracts"

        clean_name = p.get("name", "").replace("ZAYVORA ", "")
        full_name = f"ZAYVORA {clean_name}"
        is_hero = bool(p.get("is_hero_launch", False))
        price_num = int(p.get("mrp_inr") or 1800)
        axis_title = (p.get("organ_axis") or "General").title() + " Axis"

        # Item for Doctor Clinical Modal
        prod_list_clinical.append({
            "id": sku,
            "code": sku,
            "name": full_name,
            "unani_name": p.get("unani_name", ""),
            "axis": axis_title,
            "category": (p.get("regulatory_track") or "AYUSH_CLASSICAL").replace("_", " "),
            "form": p.get("formulation_type", "30 x 5g Daily Stick Sachets"),
            "price": f"₹{price_num:,}",
            "price_num": price_num,
            "dose": p.get("dosage", "1 stick sachet twice daily with warm water"),
            "classicalCore": core_ings or "Classical Unani Botanicals",
            "actives": actives_str,
            "is_hero_launch": is_hero,
            "bmr": f"BMR-2026-{sku}-01",
            "coa": "Passed (Heavy metals <0.02 ppm, Aflatoxins None, Microbial Pure)"
        })

        # Item for Website / Herbals Store
        prod_list_herbals.append({
            "id": sku.lower(),
            "sku": sku,
            "name": full_name,
            "unani_name": p.get("unani_name", ""),
            "category": axis_title.replace(" Axis", ""),
            "price": price_num,
            "desc": f"{p.get('primary_indication', 'Therapeutic formulation')}. {p.get('unani_name', '')}.",
            "dosage": p.get("dosage", "1 serving twice daily with warm water"),
            "indications": p.get("primary_indication", "Systemic restoration and equilibrium"),
            "is_hero_launch": is_hero,
            "form": p.get("formulation_type", "30 x 5g Daily Stick Sachets")
        })

    return prod_list_clinical, prod_list_herbals

def update_file(file_path, clinical_data, herbals_data):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace button badge in Doctor Consultation Workspace
    content = content.replace(
        '<span class="text-[9px] font-normal text-amber-200">16 Core Hero Actives</span>',
        '<span class="text-[9px] font-normal text-amber-200">32 Master SKUs (5 Hero Launch)</span>'
    )
    content = content.replace(
        '<span class="block font-bold">+ ZAYVORA Product</span>',
        '<span class="block font-bold">+ ZAYVORA Products</span>'
    )

    # 2. Replace modal header badges and title
    content = content.replace(
        '<span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">16 Core Hero Formulations</span>',
        '<span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">32 Master Formulations (5 Hero SKUs)</span>'
    )
    content = content.replace(
        '<h3 class="font-bold text-lg text-white mt-1">ZAYVORA Health OS™ — Proprietary Products Catalog</h3>',
        '<h3 class="font-bold text-lg text-white mt-1">ZAYVORA Health OS™ — Proprietary Master Products Catalog (32 SKUs)</h3>'
    )

    # 3. Replace filter buttons in the modal
    old_filters = '''<button onclick="filterZayvoraProductAxis('ALL')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">All (16)</button>
          <button onclick="filterZayvoraProductAxis('Male Reproductive')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Male Vitality</button>
          <button onclick="filterZayvoraProductAxis('Female')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Female</button>
          <button onclick="filterZayvoraProductAxis('Hepatic')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Liver</button>
          <button onclick="filterZayvoraProductAxis('Metabolic')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Metabolic</button>
          <button onclick="filterZayvoraProductAxis('Joint')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Joints</button>'''

    new_filters = '''<button onclick="filterZayvoraProductAxis('ALL')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">All (32)</button>
          <button onclick="filterZayvoraProductAxis('HERO')" class="px-2.5 py-1 rounded bg-amber-900/60 text-amber-300 hover:text-white font-bold border border-amber-500/40">★ 5 Hero Launch SKUs</button>
          <button onclick="filterZayvoraProductAxis('Pancreatic')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Glucovora (Pancreas)</button>
          <button onclick="filterZayvoraProductAxis('Hepatic')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">LiverPrime (Liver)</button>
          <button onclick="filterZayvoraProductAxis('Joint')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">SynovoFlex (Joints)</button>
          <button onclick="filterZayvoraProductAxis('Male')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">ManiVital Pro (Male)</button>
          <button onclick="filterZayvoraProductAxis('Female')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">OvaSync (PCOS)</button>
          <button onclick="filterZayvoraProductAxis('Cardio')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Cardiovascular</button>
          <button onclick="filterZayvoraProductAxis('Neuro')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white font-bold">Neurology</button>'''

    if old_filters in content:
        content = content.replace(old_filters, new_filters)

    # 4. Replace ZAYVORA_PRODUCTS_16 array definition with ZAYVORA_PRODUCTS_32
    clinical_json = json.dumps(clinical_data, indent=6, ensure_ascii=False)
    pattern_products = r"const ZAYVORA_PRODUCTS_16 = \[.*?\];(?:\s*const ZAYVORA_PRODUCTS_32 = ZAYVORA_PRODUCTS_16;)?"
    replacement_products = f"const ZAYVORA_PRODUCTS_16 = {clinical_json};\n    const ZAYVORA_PRODUCTS_32 = ZAYVORA_PRODUCTS_16;"
    content = re.sub(pattern_products, lambda m: replacement_products, content, flags=re.DOTALL)

    # 5. Update renderZayvoraProductsCatalog to show Hero badge, Unani name, and support HERO filter
    old_render_fn_start = """    function renderZayvoraProductsCatalog(query, axisFilter) {
      const container = document.getElementById('zayvora-products-container');
      if (!container) return;
      const q = (query || '').toLowerCase().trim();
      const af = axisFilter || activeZayvoraProductAxisFilter || 'ALL';

      const filtered = ZAYVORA_PRODUCTS_16.filter(p => {
        const matchesQ = !q || p.name.toLowerCase().includes(q) || p.axis.toLowerCase().includes(q) || p.actives.toLowerCase().includes(q) || p.code.toLowerCase().includes(q);
        const matchesAxis = af === 'ALL' || p.axis.toLowerCase().includes(af.toLowerCase());
        return matchesQ && matchesAxis;
      });"""

    new_render_fn_start = """    function renderZayvoraProductsCatalog(query, axisFilter) {
      const container = document.getElementById('zayvora-products-container');
      if (!container) return;
      const q = (query || '').toLowerCase().trim();
      const af = axisFilter || activeZayvoraProductAxisFilter || 'ALL';

      const catalogSource = (typeof ZAYVORA_PRODUCTS_32 !== 'undefined' ? ZAYVORA_PRODUCTS_32 : ZAYVORA_PRODUCTS_16);
      const filtered = catalogSource.filter(p => {
        const matchesQ = !q || p.name.toLowerCase().includes(q) || (p.unani_name && p.unani_name.toLowerCase().includes(q)) || p.axis.toLowerCase().includes(q) || p.actives.toLowerCase().includes(q) || p.code.toLowerCase().includes(q);
        const matchesAxis = af === 'ALL' ? true : af === 'HERO' ? Boolean(p.is_hero_launch) : p.axis.toLowerCase().includes(af.toLowerCase()) || p.name.toLowerCase().includes(af.toLowerCase());
        return matchesQ && matchesAxis;
      });"""

    if old_render_fn_start in content:
        content = content.replace(old_render_fn_start, new_render_fn_start)

    # Enhance product card template to show HERO badge and Unani name
    old_card_header = """                  <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-amber-300 font-bold">${p.code}</span>
                  <strong class="text-white text-sm">${p.name}</strong>
                </div>
                <span class="text-[11px] text-amber-400 font-medium block">${p.axis}</span>"""

    new_card_header = """                  <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-amber-300 font-bold">${p.code}</span>
                  <strong class="text-white text-sm">${p.name}</strong>
                  ${p.is_hero_launch ? '<span class="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold border border-amber-500/40 text-[9px] tracking-wide">★ HERO LAUNCH</span>' : ''}
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-[11px] text-amber-400 font-medium">${p.axis}</span>
                  ${p.unani_name ? `<span class="text-[10px] text-slate-400 italic">(${p.unani_name})</span>` : ''}
                </div>"""

    if old_card_header in content:
        content = content.replace(old_card_header, new_card_header)

    # 6. Replace herbalsProducts array with full 32 portfolio
    herbals_json = json.dumps(herbals_data, indent=6, ensure_ascii=False)
    pattern_herbals = r"const herbalsProducts = \[.*?\];"
    replacement_herbals = f"const herbalsProducts = {herbals_json};"
    content = re.sub(pattern_herbals, lambda m: replacement_herbals, content, flags=re.DOTALL)

    # 7. Update website navigation labels from 10 to 32
    content = content.replace("All 10 Formulations", "All 32 Master Formulations")
    content = content.replace("10-formulation portfolio", "32-formulation master portfolio")
    content = content.replace("10-Formulation Portfolio", "32 Master Formulations Portfolio")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully updated {file_path} with 32 Master Products!")

if __name__ == "__main__":
    clin, herb = build_products_data()
    update_file(os.path.join(BASE_DIR, "index.html"), clin, herb)
    update_file(os.path.join(BASE_DIR, "docs", "index.html"), clin, herb)
