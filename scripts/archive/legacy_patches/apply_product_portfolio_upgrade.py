#!/usr/bin/env python3
"""
ZAYVORA Health OS™ - Portfolio & Commercial Brand Upgrade Script
Safely upgrades product branding to trademark-defensible coined names,
modernizes packaging (HPMC veg capsules & 5g daily stick sachets),
and designates Phase-1 Hero Launch SKUs.
"""

import os
import sys
import sqlite3
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

UPGRADE_MAP = {
    "ZAY-001": {"name": "TensioCalm™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-002": {"name": "Glucovora™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-003": {"name": "CardioVora™", "form": "Majoon Granules (30 x 5g Daily Stick Sachets)", "hero": False},
    "ZAY-004": {"name": "LiverPrime™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": True},
    "ZAY-005": {"name": "LipidoVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-006": {"name": "GastroVora™", "form": "Effervescent Micro-Granules (30 Sachets)", "hero": False},
    "ZAY-007": {"name": "SynovoFlex™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-008": {"name": "NeuroVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-009": {"name": "NeuroShield-Rx™", "form": "Habb / Coated Micro-Tablets (60 Tabs)", "hero": False},
    "ZAY-010": {"name": "NephroVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-011": {"name": "DermaVora™", "form": "Standardized Micro-Granules (30 Sachets)", "hero": False},
    "ZAY-012": {"name": "PulmoVora™", "form": "Herbal Infusion / Decoction Elixir (200ml)", "hero": False},
    "ZAY-013": {"name": "ImmunoVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-014": {"name": "VigorVora™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": False},
    "ZAY-015": {"name": "LithoVora™", "form": "Targeted Micro-Granules (30 x 5g Daily Sachets)", "hero": False},
    "ZAY-016": {"name": "OsteoVora™", "form": "Micro-Calcified Tablets (60 Tabs)", "hero": False},
    "ZAY-017": {"name": "MetaboBurn-M™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-018": {"name": "MetaboBurn-F™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-019": {"name": "ThyroVora™", "form": "Compressed Tablets (60 Tabs)", "hero": False},
    "ZAY-020": {"name": "OcuVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-021": {"name": "EntoVora™", "form": "Purified Herbal Granules (30 Sachets)", "hero": False},
    "ZAY-022": {"name": "AlerVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-023": {"name": "Habb-e-Azaraqi Mudabbar™", "form": "Classical Sugar-Coated Habb (60 Pills)", "hero": False},
    "ZAY-024": {"name": "Majoon-e-Suranjan Mudabbar™", "form": "Single-Serve Paste Sachets (30 x 7g)", "hero": False},
    "ZAY-025": {"name": "ManiVital Pro™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-026": {"name": "ProstaVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-027": {"name": "AndroVora™", "form": "Targeted HPMC Veg Capsules (60 Caps)", "hero": False},
    "ZAY-028": {"name": "LeucoVora™", "form": "Micro-Granules (30 x 3g Daily Stick Sachets)", "hero": False},
    "ZAY-029": {"name": "OvaSync-PCOS™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-030": {"name": "MensoCalm™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-031": {"name": "MenoVora™", "form": "Micro-Granules (30 x 3g Daily Stick Sachets)", "hero": False},
    "ZAY-032": {"name": "PilesVora™", "form": "Compressed Tablets (60 Tabs)", "hero": False},
}


def upgrade_products_master_py():
    pm_path = os.path.join(BASE_DIR, "services", "knowledge", "app", "data", "products_master.py")
    with open(pm_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update names and formulation_types safely for each SKU block
    for sku, info in UPGRADE_MAP.items():
        # Find block for SKU
        sku_pattern = rf'("{sku}":\s*\{{.*?)(}})'
        # Replace name within SKU block
        name_sub = rf'("name":\s*")[^"]*(")'
        form_sub = rf'("formulation_type":\s*")[^"]*(")'

        def replacer(match):
            block = match.group(1)
            # update name
            block = re.sub(name_sub, rf'\g<1>{info["name"]}\g<2>', block)
            # update formulation_type
            block = re.sub(form_sub, rf'\g<1>{info["form"]}\g<2>', block)
            # add is_hero_launch if not present
            if '"is_hero_launch"' not in block:
                hero_val = "True" if info["hero"] else "False"
                block = block.rstrip() + f',\n        "is_hero_launch": {hero_val}\n    '
            return block + match.group(2)

        content = re.sub(sku_pattern, replacer, content, flags=re.DOTALL)

    with open(pm_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Updated services/knowledge/app/data/products_master.py")


def upgrade_kits_master_py():
    km_path = os.path.join(BASE_DIR, "services", "knowledge", "app", "data", "kits_master.py")
    with open(km_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update product names inside kits master while preserving SKUs and roles
    for sku, info in UPGRADE_MAP.items():
        # Look for {'sku': 'ZAY-xxx', 'name': '...'}
        pat = rf"('sku':\s*'{sku}',\s*'name':\s*')[^']*(')"
        content = re.sub(pat, rf"\g<1>{info['name']}\g<2>", content)

    with open(km_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Updated services/knowledge/app/data/kits_master.py")


def upgrade_sqlite_database():
    db_path = os.path.join(BASE_DIR, "database", "zayvora_live.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check if is_hero_launch column exists
    cur.execute("PRAGMA table_info(master_products)")
    cols = [c[1] for c in cur.fetchall()]
    if "is_hero_launch" not in cols:
        cur.execute("ALTER TABLE master_products ADD COLUMN is_hero_launch INTEGER DEFAULT 0")
        print("  Added is_hero_launch column to master_products")

    for sku, info in UPGRADE_MAP.items():
        cur.execute("""
            UPDATE master_products
            SET name = ?,
                dosage_form = ?,
                is_hero_launch = ?
            WHERE sku = ?
        """, (
            info["name"],
            info["form"],
            1 if info["hero"] else 0,
            sku
        ))

    conn.commit()
    conn.close()
    print("✓ Synchronized SQLite database master_products table")


def main():
    print("=" * 70)
    print("ZAYVORA Health OS™ - Portfolio Commercial Upgrade")
    print("=" * 70)

    upgrade_products_master_py()
    upgrade_kits_master_py()
    upgrade_sqlite_database()

    print("\n✓ Core catalog files and database successfully upgraded!")


if __name__ == "__main__":
    main()
