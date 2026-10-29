#!/usr/bin/env python3
"""
ZAYVORA Health OS — High-Availability Auto-Revival Watchdog Daemon
Monitors the live API server process and ensures zero downtime.
If the server exits or crashes, automatically revives it within 2 seconds.
Also executes hourly non-blocking database integrity snapshots.
"""

import os
import sys
import time
import subprocess
import signal
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
LOG_DIR = os.path.join(BASE_DIR, "logs")
SERVER_SCRIPT = os.path.join(BASE_DIR, "services", "live_api_server.py")
PID_FILE = os.path.join(BASE_DIR, ".watchdog.pid")
SERVER_PID_FILE = os.path.join(BASE_DIR, ".server.pid")

os.makedirs(LOG_DIR, exist_ok=True)
WATCHDOG_LOG = os.path.join(LOG_DIR, "watchdog.log")
SERVER_LOG = os.path.join(LOG_DIR, "server.log")

PORT = int(os.getenv("PORT", "8000"))
BACKUP_INTERVAL_SEC = 3600  # 1 hour

running = True
server_proc = None

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [WATCHDOG] {msg}"
    print(formatted, flush=True)
    try:
        with open(WATCHDOG_LOG, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def is_pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def handle_signal(sig, frame):
    global running, server_proc
    log(f"Received termination signal ({sig}). Shutting down gracefully...")
    running = False
    if server_proc and server_proc.poll() is None:
        try:
            server_proc.terminate()
            server_proc.wait(timeout=3)
        except Exception:
            try:
                server_proc.kill()
            except Exception:
                pass
    cleanup_pids()
    sys.exit(0)

def cleanup_pids():
    for f in [PID_FILE, SERVER_PID_FILE]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

def start_server():
    global server_proc
    log(f"Starting ZAYVORA API Server on port {PORT}...")
    
    # Check if an existing server PID is already alive
    if os.path.exists(SERVER_PID_FILE):
        try:
            with open(SERVER_PID_FILE, "r") as f:
                existing_pid = int(f.read().strip())
            if is_pid_alive(existing_pid):
                log(f"Re-attaching to existing active server process (PID {existing_pid}).")
                return True
        except Exception:
            pass

    # Ensure stale port holder is terminated
    try:
        subprocess.run(f"lsof -ti:{PORT} | xargs kill -9 2>/dev/null", shell=True)
        time.sleep(1.0)
    except Exception:
        pass

    with open(SERVER_LOG, "a", encoding="utf-8") as out:
        server_proc = subprocess.Popen(
            [sys.executable, SERVER_SCRIPT, str(PORT)],
            cwd=BASE_DIR,
            stdout=out,
            stderr=subprocess.STDOUT
        )
    
    with open(SERVER_PID_FILE, "w") as f:
        f.write(str(server_proc.pid))

    log(f"Server launched with PID {server_proc.pid}.")
    time.sleep(1.5)
    if server_proc.poll() is None:
        log(f"Server verified active on port {PORT} (PID {server_proc.pid}).")
        return True
    else:
        log(f"Server exited immediately with code {server_proc.poll()}. Check server.log.")
        return False

def periodic_backup_worker():
    while running:
        time.sleep(BACKUP_INTERVAL_SEC)
        if not running:
            break
        try:
            from services.db_backup_guard import run_integrity_and_backup
            log("Running scheduled hourly database integrity snapshot...")
            ok = run_integrity_and_backup(max_backups=24)
            if ok:
                log("Hourly snapshot completed successfully.")
            else:
                log("Warning: Hourly snapshot reported issue.")
        except Exception as e:
            log(f"Error during scheduled backup: {e}")

def main():
    global server_proc, running

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    log("=" * 60)
    log(f"ZAYVORA High-Availability Watchdog started (PID: {os.getpid()})")
    log(f"Base Directory: {BASE_DIR}")
    log(f"Target Port: {PORT}")
    log("=" * 60)

    # Start scheduled backup worker thread
    backup_thread = threading.Thread(target=periodic_backup_worker, daemon=True)
    backup_thread.start()

    # Initial server launch
    start_server()

    # Continuous supervisory loop
    while running:
        time.sleep(2.0)

        # Check managed subprocess
        if server_proc is not None:
            if server_proc.poll() is not None:
                code = server_proc.poll()
                log(f"⚠️ ALERT: Server process (PID {server_proc.pid}) exited with code {code}! Auto-reviving in 1s...")
                time.sleep(1.0)
                start_server()
        else:
            # Check unattached PID from pidfile
            if os.path.exists(SERVER_PID_FILE):
                try:
                    with open(SERVER_PID_FILE, "r") as f:
                        spid = int(f.read().strip())
                    if not is_pid_alive(spid):
                        log(f"⚠️ ALERT: Tracked server PID {spid} died! Auto-reviving...")
                        start_server()
                except Exception:
                    start_server()
            else:
                start_server()

if __name__ == "__main__":
    main()
