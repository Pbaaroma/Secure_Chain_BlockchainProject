import sys
import requests
from pathlib import Path

from client.encryption import (
    decrypt_file,
    calculate_hash
)

API_URL = "http://127.0.0.1:9000"

if len(sys.argv) != 3:
    raise SystemExit(
        "Usage: python -m client.receiver <file_id> <main|mirror>"
    )

file_id = int(sys.argv[1])
source = sys.argv[2]

if file_id < 0 or source not in ["main", "mirror"]:
    raise SystemExit("Invalid file ID or source")

print("===== SECURECHAIN FILE RECOVERY =====")
print(f"File ID: {file_id}")
print(f"Recovery source: {source.upper()}")

# Retrieve blockchain and storage metadata
response = requests.get(
    f"{API_URL}/api/files/{file_id}/metadata",
    timeout=15
)

response.raise_for_status()

metadata = response.json()
blockchain = metadata["blockchain"]
storage = metadata["storage"]

# Retrieve encrypted package
if source == "mirror":
    package_path = Path(
        f"storage/mirror/{file_id}.encrypted"
    )

    encrypted_data = package_path.read_bytes()

else:
    response = requests.get(
        f"{API_URL}/api/files/{file_id}/download",
        timeout=30
    )

    response.raise_for_status()
    encrypted_data = response.content

print("[PASS] Encrypted package retrieved")

# Verify encrypted package integrity
package_hash = calculate_hash(encrypted_data)

if package_hash != storage["encrypted_package_hash"]:
    raise SystemExit("[FAIL] Encrypted package integrity mismatch")

print("[PASS] Encrypted package integrity verified")

# Load the local RSA private key
private_key = Path(
    "keys/private_key.pem"
).read_bytes()

# Recover the original file
original_data = decrypt_file(
    encrypted_data,
    private_key
)

print("[PASS] AES key recovered using RSA private key")
print("[PASS] File successfully decrypted")

# Compare recovered file with blockchain hash
actual_hash = calculate_hash(original_data)

expected_hash = blockchain["file_hash"].lower().removeprefix("0x")

print(f"Blockchain SHA-256: {expected_hash}")
print(f"Recovered SHA-256:  {actual_hash}")

if actual_hash != expected_hash:
    raise SystemExit("[FAIL] Blockchain integrity verification failed")

print("[PASS] Blockchain integrity verification successful")

# Save the recovered file
output_dir = Path("storage/received")
output_dir.mkdir(parents=True, exist_ok=True)

filename = Path(blockchain["filename"]).name

output_path = output_dir / f"{file_id}_{filename}"
output_path.write_bytes(original_data)

print(f"[PASS] Recovered file saved: {output_path}")
print("===== FILE RECOVERY SUCCESSFUL =====")
