#!/usr/bin/env python3
"""Quick startup - launches sbti test server and creates tunnel"""
import os
import sys
import time
import subprocess
import json

# Add venv site-packages
sys.path.insert(0, "/app/venv/lib/python3.11/site-packages")

from pyngrok import ngrok
from pyngrok.conf import PyngrokConfig

BASE = "/app/working/workspaces/default/sbti-test"

# Try to get authtoken from env
authtoken = os.environ.get("NGROK_AUTHTOKEN", "")

config = PyngrokConfig()
if authtoken:
    config.auth_token = authtoken

# Kill existing server
subprocess.run(["pkill", "-f", "server.py"], capture_output=True)
time.sleep(1)

# Start server
proc = subprocess.Popen(
    [sys.executable, "server.py"],
    cwd=BASE,
    stdout=open("/tmp/sbti_server.log", "w"),
    stderr=subprocess.STDOUT
)

# Wait for server
for i in range(10):
    time.sleep(1)
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:8080/", timeout=2)
        print("Server is up!")
        break
    except:
        if i == 9:
            print("Server failed to start")
            sys.exit(1)

if authtoken:
    url = ngrok.connect(8080, "http")
    print(f"PUBLIC_URL={url}")
else:
    print("NO_NGROK_TOKEN")
    print("LOCAL_URL=http://localhost:8080")

# Keep running
try:
    proc.wait()
except:
    pass
