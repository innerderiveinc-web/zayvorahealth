#!/usr/bin/env bash
# ==============================================================================
# ZAYVORA Health OS™ & Public Healthcare Platform — Unified Production Launcher
# ==============================================================================
# Usage:
#   bash launch.sh
#   or ./launch.sh [--port 8080] [--api-port 8000]
# ==============================================================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

WEB_PORT="${1:-8080}"
API_PORT="${2:-8000}"

echo "================================================================================"
echo " 🌿 ZAYVORA Health OS™ — Production Launch Sequence Initiated"
echo "================================================================================"
echo " Directory: $REPO_ROOT"
echo " Web Port:  $WEB_PORT"
echo " API Port:  $API_PORT"
echo "================================================================================"

# 1. Check & provision SQLite database
if [ ! -f "database/zayvora_live.db" ]; then
  echo "[DB] Provisioning initial live database..."
  python3 database/provision.py --mode sqlite
fi

# 2. Trap SIGINT and SIGTERM for clean shutdown
cleanup() {
  echo ""
  echo "[SHUTDOWN] Terminating ZAYVORA Health OS services..."
  kill $(jobs -p) 2>/dev/null || true
  echo "[SHUTDOWN] All daemons halted cleanly."
  exit 0
}
trap cleanup SIGINT SIGTERM

# 3. Start Live REST API Server (Port 8000)
echo "[1/2] Starting Live REST API Backend on port $API_PORT..."
python3 services/live_api_server.py "$API_PORT" &
API_PID=$!

sleep 1

# 4. Start ZAYVORA Web Platform & Clinical Cockpit (Port 8080)
echo "[2/2] Starting ZAYVORA Health OS Web Platform on port $WEB_PORT..."
python3 scripts/launch_zayvora_os.py --port "$WEB_PORT" &
WEB_PID=$!

sleep 1

echo ""
echo "================================================================================"
echo "  ZAYVORA Health OS™ & Public Website IS NOW LIVE AND SERVING"
echo "================================================================================"
echo "  1. Public Front-Door (Website):      http://localhost:$WEB_PORT"
echo "     → Patient Portal:                 http://localhost:$WEB_PORT/patient"
echo "     → Clinician & Staff Gateway:      http://localhost:$WEB_PORT/doctor"
echo ""
echo "  2. Private Health OS (Intranet):     http://localhost:$WEB_PORT/doctor"
echo "     → Doctor Clinical Desk:           http://localhost:$WEB_PORT/doctor"
echo "     → Pharmacy FEFO & Inventory:      http://localhost:$WEB_PORT/pharmacy"
echo "     → Administration & Compliance:    http://localhost:$WEB_PORT/admin"
echo ""
echo "  3. Live REST API & SQL Database:     http://localhost:$API_PORT"
echo "     → API Health Check:               http://localhost:$API_PORT/api/v1/health"
echo "     → Patient 360 & EMR Registry:     http://localhost:$API_PORT/api/v1/patients"
echo "     → Prescription & Merkle Ledger:   http://localhost:$API_PORT/api/v1/prescriptions"
echo "================================================================================"
echo "  Press [Ctrl + C] to safely shut down all ZAYVORA services."
echo "================================================================================"

wait
