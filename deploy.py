#!/usr/bin/env python3
import subprocess, time, os, sys, signal

os.chdir('/app/working/workspaces/default/sbti-test')

# Kill existing
for p in subprocess.run(['ps', 'aux'], capture_output=True, text=True).stdout.split('\n'):
    if 'server.py' in p and 'grep' not in p:
        try:
            pid = int(p.split()[1])
            os.kill(pid, 9)
            print(f"Killed PID {pid}")
        except:
            pass

time.sleep(2)

# Start server
server = subprocess.Popen(
    [sys.executable, 'server.py', '--host', '0.0.0.0', '--port', '8080'],
    stdout=open('/tmp/sbti_server.log','w'),
    stderr=subprocess.STDOUT
)
print(f"Server PID: {server.pid}", flush=True)
time.sleep(3)

# Check server is up
import urllib.request
try:
    r = urllib.request.urlopen('http://localhost:8080/', timeout=5)
    print(f"Server OK: {r.status}", flush=True)
except Exception as e:
    print(f"Server failed: {e}", flush=True)
    sys.exit(1)

# Start tunnel and capture URL
tunnel = subprocess.Popen(
    ['lt', '--port', '8080'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)
print("Waiting for tunnel URL...", flush=True)

start = time.time()
url = None
while time.time() - start < 12:
    line = tunnel.stdout.readline().strip()
    print(f"LT: {line}", flush=True)
    if 'url' in line.lower() and 'https' in line.lower():
        parts = line.split(':')
        url = parts[-2].strip() + ':' + parts[-1].strip()
        break

if url:
    print(f"\n=== PUBLIC URL: {url} ===", flush=True)
    with open('/tmp/sbti_public_url.txt', 'w') as f:
        f.write(url)
else:
    print("\nFailed to get tunnel URL", flush=True)
    sys.exit(1)

signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
server.wait()
