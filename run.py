#!/usr/bin/env python
from pyngrok import ngrok
import subprocess
import time
import os
import signal

BASE_DIR = "/app/working/workspaces/default/sbti-test"

# Kill existing server if any
try:
    subprocess.run("pkill -f 'python server.py'", shell=True)
except:
    pass
time.sleep(1)

# Start server
proc = subprocess.Popen(
    ["/app/venv/bin/python", "server.py"],
    cwd=BASE_DIR
)
time.sleep(3)

# Expose via ngrok
url = ngrok.connect(8080, "http")
print(f"Access URL: {url}")
print("Server is running... Press Ctrl+C to stop.")

try:
    proc.wait()
except KeyboardInterrupt:
    ngrok.disconnect(url)
    proc.terminate()
