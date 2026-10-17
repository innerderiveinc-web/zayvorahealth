#!/bin/bash
# Installs git pre-commit hook for automated sync and parity check
HOOK_FILE=".git/hooks/pre-commit"
if [ -d ".git" ]; then
    mkdir -p .git/hooks
    cat << 'EOF' > "$HOOK_FILE"
#!/bin/bash
echo "[Git Hook] Running ZAYVORA master sync and parity check..."
python3 scripts/sync_all.py || exit 1
python3 tests/test_codebase_integrity_and_parity.py || exit 1
git add app.html docs/
echo "[Git Hook] All integrity checks passed."
EOF
    chmod +x "$HOOK_FILE"
    echo "✓ Git pre-commit hook installed successfully at $HOOK_FILE"
else
    echo "Not a git repository root."
fi
