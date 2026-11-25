#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

CLOUD_HOST="${SECURECHAIN_CLOUD_HOST:-csci311@35.237.171.134}"

mkdir -p storage/logs storage/pids storage/mirror storage/received

echo "===== SECURECHAIN LOCAL STARTUP ====="

if [ ! -x .venv/bin/python ]; then
    echo "[FAIL] Python virtual environment missing"
    exit 1
fi

if [ ! -f keys/private_key.pem ] || [ ! -f keys/public_key.pem ]; then
    echo "[FAIL] RSA keys missing"
    exit 1
fi

start_tunnel() {
    local port="$1"

    if ss -ltnH "sport = :$port" | grep -q .; then
        echo "[INFO] Port $port already active"
    else
        ssh -fN \
            -o ExitOnForwardFailure=yes \
            -o ServerAliveInterval=30 \
            -M -S "$PWD/storage/pids/ssh-$port.sock" \
            -L "127.0.0.1:$port:127.0.0.1:$port" \
            "$CLOUD_HOST"

        echo "[PASS] SSH tunnel established on port $port"
    fi
}

start_tunnel 7545
start_tunnel 9000

if ! curl -fsS http://127.0.0.1:9000/api/health >/dev/null; then
    echo "[FAIL] Cloud backend unavailable"
    exit 1
fi

if curl -fsS http://127.0.0.1:9100/api/status >/dev/null; then
    echo "[INFO] Local API already running"
elif ss -ltnH "sport = :9100" | grep -q .; then
    echo "[FAIL] Port 9100 occupied by an unavailable service"
    exit 1
else
    nohup .venv/bin/python -m uvicorn client.local_api:app \
        --host 127.0.0.1 --port 9100 \
        > storage/logs/local_api.log 2>&1 &

    echo $! > storage/pids/local_api.pid
    echo "[INFO] Local API starting"
fi

if pgrep -u "$(id -u)" -f '[p]ython.*-m mirror_server.sync' >/dev/null; then
    echo "[INFO] Mirror synchronization already running"
else
    nohup .venv/bin/python -m mirror_server.sync \
        > storage/logs/mirror.log 2>&1 &

    echo $! > storage/pids/mirror.pid
    echo "[INFO] Mirror synchronization starting"
fi

if curl -fsS http://127.0.0.1:5173 >/dev/null; then
    echo "[INFO] Frontend already running"
elif ss -ltnH "sport = :5173" | grep -q .; then
    echo "[FAIL] Port 5173 already occupied"
    exit 1
else
    (
        cd frontend
        exec nohup ./node_modules/.bin/vite \
            --host 127.0.0.1 --port 5173 --strictPort
    ) > storage/logs/frontend.log 2>&1 &

    echo $! > storage/pids/frontend.pid
    echo "[INFO] Frontend starting"
fi

for i in {1..30}; do
    if curl -fsS http://127.0.0.1:9100/api/status >/dev/null \
        && curl -fsS http://127.0.0.1:5173 >/dev/null; then

        echo
        echo "===== SECURECHAIN READY ====="
        echo "Frontend: http://127.0.0.1:5173"
        echo "Local API: http://127.0.0.1:9100"
        exit 0
    fi

    sleep 2
done

echo "[FAIL] Local services did not become ready"
echo "Check storage/logs/"
exit 1
