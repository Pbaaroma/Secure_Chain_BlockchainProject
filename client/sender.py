import sys
import requests
from pathlib import Path

from client.encryption import (
    encrypt_file,
    calculate_hash
)

API_URL = "http://127.0.0.1:9000"

if len(sys.argv) != 2:
    raise SystemExit(
        "Usage: python -m client.sender <filename>"
    )

file_path = Path(sys.argv[1])

if not file_path.is_file():
    raise SystemExit("File not found")

original_data = file_path.read_bytes()

public_key = Path(
    "keys/public_key.pem"
).read_bytes()

file_hash = calculate_hash(original_data)

print("===== SECURECHAIN FILE TRANSFER =====")
print(f"File: {file_path.name}")
print(f"Original size: {len(original_data)} bytes")
print(f"SHA-256: {file_hash}")

encrypted_package = encrypt_file(
    original_data,
    public_key
)

print("[PASS] File encrypted using AES-256-GCM")
print("[PASS] AES key protected using RSA-OAEP")
print("[INFO] Sending encrypted package to Google Cloud")

response = requests.post(
    f"{API_URL}/api/files/upload",
    files={
        "file": (
            file_path.name + ".encrypted",
            encrypted_package,
            "application/octet-stream"
        )
    },
    data={
        "filename": file_path.name,
        "file_hash": file_hash
    },
    timeout=60
)

if not response.ok:
    print(response.text)
    raise SystemExit("Upload failed")

result = response.json()

print("[PASS] Encrypted file uploaded")
print("[PASS] File registered on blockchain")

print(f"File ID: {result['file_id']}")
print(f"Transaction: {result['transaction_hash']}")
print(f"Block number: {result['block_number']}")
print(f"Encrypted size: {result['encrypted_size']} bytes")

print("===== FILE TRANSFER SUCCESSFUL =====")
