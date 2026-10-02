#!/usr/bin/env bash
# ==============================================================================
# ZAYVORA Health OS™ — Platform Mirror Synchronization Utility
# Keeps standalone offline HTML files and database mirrors 100% synchronized.
# ==============================================================================

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

echo "🔄 [ZAYVORA] Synchronizing HTML mirrors..."
cp -f index.html docs/index.html
cp -f index.html app.html
cp -f index.html docs/app.html

echo "🔄 [ZAYVORA] Synchronizing Database mirrors..."
if [ -f "database/zayvora_live.db" ]; then
  cp -f database/zayvora_live.db zayvora_live.db
fi

echo "🔄 [ZAYVORA] Synchronizing Website HTML mirrors..."
if [ -f "website.html" ]; then
  cp -f website.html docs/website.html
  cp -f website.html public_website.html
fi

echo "✅ [ZAYVORA] All platform mirrors synchronized successfully!"
