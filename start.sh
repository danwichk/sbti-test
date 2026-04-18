#!/bin/bash
# Start SBTI test server and localtunnel in background
cd /app/working/workspaces/default/sbti-test

# Kill existing instances
pkill -f "server.py" 2>/dev/null
pkill -f "lt --port" 2>/dev/null
sleep 1

# Start FastAPI server
/app/venv/bin/python server.py --host 0.0.0.0 --port 8080 > /tmp/sbti_server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server
sleep 3

# Start localtunnel (will be killed after we get URL)
timeout 10 lt --port 8080 2>&1 | grep -o 'https://[^ ]*' > /tmp/sbti_url.txt &
TUNNEL_PID=$!

# Wait for URL
sleep 8
TUNNEL_URL=$(cat /tmp/sbti_url.txt 2>/dev/null)

if [ -n "$TUNNEL_URL" ]; then
    echo "PUBLIC_URL=$TUNNEL_URL"
else
    # Start a persistent tunnel
    nohup lt --port 8080 > /tmp/sbti_tunnel.log 2>&1 &
    echo "Tunnel started (check /tmp/sbti_tunnel.log for URL)"
fi
