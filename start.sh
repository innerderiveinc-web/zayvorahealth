#!/bin/bash
# ZAYVORA Platform Starter
cd "$(dirname "$0")"

echo "=================================="
echo " ZAYVORA Health OS — Starting Up"
echo "=================================="

# Kill any existing process on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 1

# Start the server
echo "Starting server on http://localhost:8000 ..."
python3 services/live_api_server.py 8000 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
sleep 2

# Verify
if curl --noproxy "*" -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q '200'; then
    echo ""
    echo "✅ ZAYVORA is running!"
    echo "🌐 Open in browser: http://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop the server."
    wait $SERVER_PID
else
    echo "❌ Server failed to start. Check logs above."
    exit 1
fi
