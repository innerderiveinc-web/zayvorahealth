#!/usr/bin/env python3
"""
scripts/build_dist.py

Synchronizes all production assets into `dist/` so that Netlify succeeds
regardless of whether the Dashboard Publish directory is configured as
`dist`, `.`, or `docs`.
"""

import shutil
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")
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

    # Docs directory
    docs_src = ROOT / "docs"
    if docs_src.exists():
        shutil.copytree(docs_src, DIST / "docs")
        print("✓ Copied docs/ to dist/docs/")

    print("=== Dist build completed successfully ===")

if __name__ == "__main__":
    build()
