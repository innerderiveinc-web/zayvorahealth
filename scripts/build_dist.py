#!/usr/bin/env python3
"""
scripts/build_dist.py

Synchronizes all production assets into `dist/` so that Netlify succeeds
regardless of whether the Dashboard Publish directory is configured as
`dist`, `.`, or `docs`.
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    # Core files
    core_files = [
        "index.html",
        "app.html",
        "science_and_research.html",
        "_redirects",
        "CNAME",
        "manifest.json",
        "sw.js",
        "tailwind.min.js",
        "favicon.ico",
        "zayvora-logo.png",
        "netlify.toml"
    ]

    for fn in core_files:
        src = ROOT / fn
        if src.exists():
            shutil.copy2(src, DIST / fn)
            print(f"✓ Copied {fn} to dist/")

    # JS directory
    js_src = ROOT / "js"
    if js_src.exists():
        shutil.copytree(js_src, DIST / "js")
        print("✓ Copied js/ to dist/js/")

    # Design system assets if present
    design_system_src = ROOT / "design-system"
    if design_system_src.exists():
        shutil.copytree(design_system_src, DIST / "design-system")
        print("✓ Copied design-system/ to dist/design-system/")

    print("=== Dist build completed successfully ===")

if __name__ == "__main__":
    build()
