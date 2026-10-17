#!/bin/bash
# ZAYVORA Health OS — Production Daemon Controller
# Manages the zero-crash background watchdog and live API server.

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

WATCHDOG_PID_FILE="$BASE_DIR/.watchdog.pid"
SERVER_PID_FILE="$BASE_DIR/.server.pid"
LOGS_DIR="$BASE_DIR/logs"
mkdir -p "$LOGS_DIR"

case "$1" in
  start)
    if [ -f "$WATCHDOG_PID_FILE" ] && kill -0 "$(cat "$WATCHDOG_PID_FILE")" 2>/dev/null; then
        echo "⚠️ ZAYVORA Watchdog is already running (PID $(cat "$WATCHDOG_PID_FILE"))."
        exit 0
    fi

    echo "=========================================================="
    echo " Starting ZAYVORA Health OS (Production Crash-Proof Mode) "
    echo "=========================================================="
    
    # Auto-sync mirrors & verify health
    python3 scripts/sync_all.py > /dev/null 2>&1
    python3 scripts/health_check_360.py > /dev/null 2>&1 || {
        echo "❌ Pre-flight health check failed. Run 'python3 scripts/health_check_360.py' for details."
        exit 1
    }

    nohup python3 scripts/watchdog_service.py > /dev/null 2>&1 &
    sleep 2

    if [ -f "$WATCHDOG_PID_FILE" ] && kill -0 "$(cat "$WATCHDOG_PID_FILE")" 2>/dev/null; then
        echo "✅ Watchdog Daemon active (PID $(cat "$WATCHDOG_PID_FILE"))."
        echo "✅ Server active on: http://localhost:8000"
        echo "📁 Logs: $LOGS_DIR/watchdog.log & $LOGS_DIR/server.log"
        echo "💡 Use './daemon.sh status' or './daemon.sh stop' to manage."
    else
        echo "❌ Failed to start watchdog daemon. Check $LOGS_DIR/watchdog.log"
        exit 1
    fi
    ;;

  stop)
    echo "Stopping ZAYVORA Health OS..."
    if [ -f "$WATCHDOG_PID_FILE" ]; then
        PID=$(cat "$WATCHDOG_PID_FILE")
        kill -15 "$PID" 2>/dev/null
        rm -f "$WATCHDOG_PID_FILE"
        echo "Stopped Watchdog (PID $PID)."
    fi

    if [ -f "$SERVER_PID_FILE" ]; then
        SPID=$(cat "$SERVER_PID_FILE")
        kill -15 "$SPID" 2>/dev/null
        rm -f "$SERVER_PID_FILE"
        echo "Stopped API Server (PID $SPID)."
    fi

    # Clean port 8000 holder if any remains
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo "✅ ZAYVORA stopped cleanly."
    ;;

  restart)
    $0 stop
    sleep 2
    $0 start
    ;;

  status)
    echo "=== ZAYVORA Health OS Status ==="
    WATCHDOG_RUNNING=0
    SERVER_RUNNING=0

    if [ -f "$WATCHDOG_PID_FILE" ] && kill -0 "$(cat "$WATCHDOG_PID_FILE")" 2>/dev/null; then
        echo "🛡️ Watchdog Daemon: RUNNING (PID $(cat "$WATCHDOG_PID_FILE"))"
        WATCHDOG_RUNNING=1
    else
        echo "🛡️ Watchdog Daemon: STOPPED"
    fi

    if [ -f "$SERVER_PID_FILE" ] && kill -0 "$(cat "$SERVER_PID_FILE")" 2>/dev/null; then
        echo "🌐 Live API Server: RUNNING (PID $(cat "$SERVER_PID_FILE"))"
        SERVER_RUNNING=1
    else
        echo "🌐 Live API Server: STOPPED"
    fi

    HTTP_STATUS=$(curl --noproxy "*" -s -o /dev/null -w "%{http_code}" http://localhost:8000/ 2>/dev/null)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "⚡ HTTP Gateway (Port 8000): HEALTHY (HTTP 200 OK)"
    else
        echo "⚠️ HTTP Gateway (Port 8000): NOT RESPONDING ($HTTP_STATUS)"
    fi

    echo ""
    echo "Recent Watchdog Logs:"
    tail -n 5 "$LOGS_DIR/watchdog.log" 2>/dev/null || echo "(No logs yet)"
    ;;

  logs)
    tail -f "$LOGS_DIR/watchdog.log" "$LOGS_DIR/server.log"
    ;;

  *)
    echo "Usage: ./daemon.sh {start|stop|restart|status|logs}"
    exit 1
    ;;
esac
