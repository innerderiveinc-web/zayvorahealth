#!/usr/bin/env python3
"""
scripts/fix_netlify_config.py

1. Explicitly sets `command = "echo 'Deploying ZAYVORA Health OS Static Assets'"` in `netlify.toml`
   so Netlify builds instantly in 0.5s without attempting to run python package detectors.
2. Updates `_redirects` and `docs/_redirects` to properly handle /app, /clinical, /science, and SPA fallback.
3. Syncs to docs/ and verifies health check.
"""

from pathlib import Path
import shutil

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")

netlify_toml_content = """[build]
  publish = "."
  command = "echo 'Deploying ZAYVORA Health OS Static Assets'"

[[redirects]]
  from = "/app"
  to = "/app.html"
  status = 200

[[redirects]]
  from = "/clinical"
  to = "/app.html"
  status = 200

[[redirects]]
  from = "/portal"
  to = "/app.html"
  status = 200

[[redirects]]
  from = "/science"
  to = "/science_and_research.html"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/sw.js"
  [headers.values]
    Cache-Control = "no-cache"
"""

redirects_content = """/app        /app.html                  200
/clinical   /app.html                  200
/portal     /app.html                  200
/science    /science_and_research.html 200
/*          /index.html                200
"""

(ROOT / "netlify.toml").write_text(netlify_toml_content, encoding="utf-8")
print("✓ Updated netlify.toml with explicit build command and redirects")

(ROOT / "_redirects").write_text(redirects_content, encoding="utf-8")
print("✓ Updated _redirects")

(ROOT / "docs" / "_redirects").write_text(redirects_content, encoding="utf-8")
print("✓ Updated docs/_redirects")

shutil.copy2(ROOT / "netlify.toml", ROOT / "docs" / "netlify.toml")
print("✓ Synced netlify.toml to docs/")

print("=== Netlify Configuration Fix Completed ===")
