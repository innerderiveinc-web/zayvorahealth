#!/usr/bin/env bash
# ZAYVORA Health OS™ — Development Startup Script
# Starts all microservices on their respective ports
# Usage: bash scripts/dev-start.sh

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Load env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "[OK] Environment loaded from .env"
fi

# Provision SQLite DB if not present
if [ ! -f database/zayvora_live.db ]; then
  echo "[DB] Provisioning SQLite database..."
  python3 database/provision.py --mode sqlite
fi

echo ""
echo "Starting ZAYVORA Health OS™ microservices..."
echo ""

# Start services in background
uvicorn services.identity.app.main:app   --port 8001 --reload --log-level warning &
uvicorn services.clinical.app.main:app   --port 8002 --reload --log-level warning &
uvicorn services.knowledge.app.main:app  --port 8003 --reload --log-level warning &
uvicorn services.therapeutic.app.main:app --port 8004 --reload --log-level warning &
uvicorn services.ai.app.main:app         --port 8005 --reload --log-level warning &
uvicorn services.gateway.app.main:app    --port 8000 --reload --log-level info    &

echo "[OK] Services started. Gateway at http://localhost:8000"
echo ""
echo "Service URLs:"
echo "  Gateway:     http://localhost:8000/api/health"
echo "  Identity:    http://localhost:8001/api/health"
echo "  Clinical:    http://localhost:8002/api/health"
echo "  Knowledge:   http://localhost:8003/api/health"
echo "  Therapeutic: http://localhost:8004/api/health"
echo "  AI:          http://localhost:8005/api/health"
echo ""
echo "Frontend (Next.js — run separately):"
echo "  cd apps/web && npm run dev"
echo ""
echo "Press Ctrl+C to stop all services."
wait
