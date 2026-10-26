#!/bin/zsh
set -e

cd "$(dirname "$0")"

PORT=8080
URL="http://127.0.0.1:${PORT}"
PYTHON_BIN="/usr/bin/python3"

echo "================================================================================"
echo " 🚀 ZAYVORA HEALTH OS™ — ONE-CLICK SYSTEM LAUNCHER"
echo "================================================================================"
echo " Initializing ZAYVORA Health OS on ${URL}..."

# Check if port 8080 is already active
if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "✓ Server is already running on ${URL}."
else
    echo "Starting background server daemon..."
    "$PYTHON_BIN" scripts/launch_zayvora_os.py --port "$PORT" > server.log 2>&1 &
    sleep 2
fi

# Automatically open browser
if command -v open >/dev/null 2>&1; then
    echo "✓ Opening ${URL} in your default web browser..."
    open "$URL"
fi

echo ""
echo "================================================================================"
echo " ✅ ZAYVORA HEALTH OS™ IS LIVE"
echo "================================================================================"
echo " Dashboard:    ${URL}"
echo " Health Check: ${URL}/health"
echo " API Base:     ${URL}/api/v1"
echo "================================================================================"
echo ""
echo "Keep this window open while using the application."
echo "Press Control+C anytime to exit."

while true; do
    sleep 60
done
