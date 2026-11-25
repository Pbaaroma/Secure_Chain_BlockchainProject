#!/usr/bin/env bash

cd "$(dirname "$0")/.."

echo "===== SECURECHAIN SYSTEM STATUS ====="

echo
echo "Cloud Blockchain:"
curl -fsS http://127.0.0.1:9000/api/blockchain/status \
    | python3 -m json.tool

echo
echo "Local Client and Mirror Status:"
curl -fsS http://127.0.0.1:9100/api/status \
    | python3 -m json.tool

echo
echo "Mirror Process:"
pgrep -af '[p]ython.*-m mirror_server.sync' \
    || echo "Mirror process not running"

echo
echo "Frontend:"
curl -fsS http://127.0.0.1:5173 >/dev/null \
    && echo "[PASS] Frontend reachable" \
    || echo "[FAIL] Frontend unavailable"

echo
echo "Local Mirror Files:"
ls -lh storage/mirror/

echo "===== STATUS CHECK COMPLETE ====="
