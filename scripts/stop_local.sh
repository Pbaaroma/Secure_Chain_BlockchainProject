#!/usr/bin/env bash

cd "$(dirname "$0")/.."

CLOUD_HOST="${SECURECHAIN_CLOUD_HOST:-csci311@35.237.171.134}"

echo "===== SECURECHAIN LOCAL SHUTDOWN ====="

for service in frontend mirror local_api; do
    pidfile="storage/pids/$service.pid"

    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")

        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            echo "[PASS] Stopped $service"
        fi

        rm -f "$pidfile"
    else
        echo "[INFO] $service not managed by startup script"
    fi
done

for port in 7545 9000; do
    socket="$PWD/storage/pids/ssh-$port.sock"

    if [ -S "$socket" ]; then
        ssh -S "$socket" -O exit "$CLOUD_HOST"
        echo "[INFO] Closed SSH tunnel on port $port"
    fi
done

echo "===== LOCAL SHUTDOWN COMPLETE ====="
echo "Cloud services and stored files preserved."
