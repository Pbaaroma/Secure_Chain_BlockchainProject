#!/usr/bin/env bash

set -e

echo "===== SECURECHAIN CLOUD STARTUP ====="

docker start securechain-ganache
docker start securechain-backend

echo "Checking SecureChain containers..."

docker ps --filter name=securechain

echo "Waiting for backend..."

for i in {1..30}; do
    if curl -fsS http://127.0.0.1:9000/api/blockchain/status; then
        echo
        echo "===== CLOUD SERVICES READY ====="
        exit 0
    fi

    sleep 2
done

echo "[FAIL] Backend did not become ready"
exit 1
