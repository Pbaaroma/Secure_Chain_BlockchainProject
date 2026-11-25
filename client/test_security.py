import json
import base64
import requests

from pathlib import Path
from cryptography.exceptions import InvalidTag
from client.encryption import decrypt_file, calculate_hash

API_URL = "http://127.0.0.1:9000"

print("===== SECURECHAIN SECURITY TEST =====")

package = Path("storage/mirror/0.encrypted").read_bytes()
private_key = Path("keys/private_key.pem").read_bytes()

response = requests.get(
    f"{API_URL}/api/files/0/metadata",
    timeout=15
)
response.raise_for_status()

metadata = response.json()

expected_hash = metadata["blockchain"]["file_hash"]
expected_hash = expected_hash.lower().removeprefix("0x")

# Test 1: Valid encrypted file
original = decrypt_file(package, private_key)

if calculate_hash(original) != expected_hash:
    raise SystemExit("[FAIL] Valid file verification failed")

print("[PASS] Valid file accepted")

# Test 2: Modified plaintext
modified = original + b"\nUnauthorized modification"

if calculate_hash(modified) == expected_hash:
    raise SystemExit("[FAIL] Modified file was accepted")

print("[PASS] Modified file rejected by blockchain hash comparison")

# Test 3: Modified encrypted package
tampered = json.loads(package)

ciphertext = bytearray(
    base64.b64decode(tampered["encrypted_data"])
)

ciphertext[0] ^= 1

tampered["encrypted_data"] = base64.b64encode(
    ciphertext
).decode()

tampered_package = json.dumps(tampered).encode()

if calculate_hash(tampered_package) == metadata["storage"]["encrypted_package_hash"]:
    raise SystemExit("[FAIL] Package modification was not detected")

print("[PASS] Encrypted package modification detected")

# Test 4: AES authentication
try:
    decrypt_file(tampered_package, private_key)
except InvalidTag:
    print("[PASS] AES-GCM rejected tampered ciphertext")
else:
    raise SystemExit("[FAIL] Tampered ciphertext was accepted")

print("===== ALL SECURITY TESTS PASSED =====")
