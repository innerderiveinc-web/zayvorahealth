#!/usr/bin/env python3
"""
ZAYVORA Health™ — Dedicated Website Packager
Creates zayvora-website.zip containing:
- website.html (Instant browser double-click)
- public_website.html
- docs/website.html
- Full Next.js website source (apps/web)
- README.md with clear instructions
"""

import os
import zipfile

def package_website():
    root_dir = "/Users/irfanashraf/Downloads/zayvora-platform-phase0-4"
    zip_path = os.path.join(root_dir, "zayvora-website.zip")

    readme = """# ZAYVORA Health™ — Public Website Package

A Personalised, Clinician-Led, AI-Assisted, Outcome-Driven Modern Unani Healthcare Platform.
Governed under the NCISM Act 2020 & DPDP Act 2023.

---

## 1. Quick Instant Viewing (Offline / Any Browser)
Simply double-click:
- **`website.html`** or **`public_website.html`**

This opens the standalone, fully interactive public website immediately in Safari, Chrome, Edge, or Firefox without requiring terminal commands, Node.js, or internet access.

### Key Interactive Features in Instant View:
- **Master Prompt §76: 6-Stage Standardized Care Loop**
  Clickable stages: 01 Assessment, 02 Personalisation, 03 Clinician, 04 Care Plan, 05 Monitoring, 06 Outcomes.
- **Interactive 45-Second Mizaj Tendency Screener**
  3 clinical questions (Thermal sensitivity, Digestion/Metabolism, Sleep pattern) with instant real-time temperament calculation (Safrawi, Damawi, Balghami, Sawdawi) and lifestyle guidance.
- **Structured Care Areas**
  Cardiometabolic, Gastrointestinal (Su-e-Hazm), Musculoskeletal (Waja-ul-Mafasil), Sleep & Psychosomatic (Sahar).
- **Verified Medical Leadership**
  Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU Aligarh).
- **Statutory Trust & Safety**
  NCISM Act 2020, DPDP Act 2023, AYUSH-GMP Schedule M-I, Emergency 112 guidance.

---

## 2. Next.js 16 Production Web Application Source
The `apps/web/` directory contains the full modern Next.js 16 source code:
- `apps/web/app/page.tsx` — Interactive homepage
- `apps/web/lib/cms/website/homepage.ts` — Centralized institutional CMS
- `apps/web/components/` — Shared healthcare UI design system

### To run via Next.js dev server:
```bash
cd apps/web
npm install
npm run dev
# Open http://localhost:3000
```
"""

    files_to_add = [
        "website.html",
        "public_website.html",
        "docs/website.html",
        "scripts/build_public_website_html.py",
        "tests/test_multi_page_website.py",
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.md", readme)
        
        for rel in files_to_add:
            full = os.path.join(root_dir, rel)
            if os.path.exists(full):
                z.write(full, rel)
                print(f"[ADD] {rel}")

        web_dir = os.path.join(root_dir, "apps", "web")
        for dirpath, dirnames, filenames in os.walk(web_dir):
            dirnames[:] = [d for d in dirnames if d not in ["node_modules", ".next", "__pycache__", ".git"]]
            for fn in filenames:
                if fn.endswith((".DS_Store", ".pyc")):
                    continue
                fpath = os.path.join(dirpath, fn)
                arc = os.path.relpath(fpath, root_dir)
                z.write(fpath, arc)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[SUCCESS] Created {zip_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_website()
