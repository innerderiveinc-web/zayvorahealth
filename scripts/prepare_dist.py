#!/usr/bin/env python3
"""
scripts/prepare_dist.py

Prepares a comprehensive `dist/` directory containing all production files
so that Netlify succeeds whether configured for `publish = "."`, `publish = "dist"`, or `publish = "docs"`.
"""

import shutil
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")
DIST = ROOT / "dist"

def prepare_dist():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    # Core HTML entry points
    for fn in ["index.html", "app.html", "science_and_research.html", "_redirects", "CNAME", "manifest.json", "sw.js", "tailwind.min.js", "favicon.ico", "zayvora-logo.png"]:
        src = ROOT / fn
        if src.exists():
            shutil.copy2(src, DIST / fn)
            print(f"✓ Copied {fn} to dist/")

    # JS folder
    js_src = ROOT / "js"
    if js_src.exists():
        shutil.copytree(js_src, DIST / "js")
        print("✓ Copied js/ to dist/js/")

    # Docs folder
    docs_src = ROOT / "docs"
    if docs_src.exists():
        shutil.copytree(docs_src, DIST / "docs")
        print("✓ Copied docs/ to dist/docs/")

    # Also static / packages if needed
    for folder in ["static", "packages", "knowledge", "design-system"]:
        f_src = ROOT / folder
        if f_src.exists():
            shutil.copytree(f_src, DIST / folder)
            print(f"✓ Copied {folder}/ to dist/{folder}/")

    print("=== Dist Preparation Complete ===")

if __name__ == "__main__":
    prepare_dist()
