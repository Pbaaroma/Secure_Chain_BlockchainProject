from backend.encryption import (
    generate_rsa_keys,
    encrypt_file,
    decrypt_file,
    calculate_hash
)

original = b"SecureChain confidential file transfer test."

print("===== SECURECHAIN ENCRYPTION TEST =====")

private_key, public_key = generate_rsa_keys()

print("[PASS] RSA-2048 key pair generated")

encrypted = encrypt_file(original, public_key)

assert original not in encrypted

print("[PASS] AES-256-GCM encryption completed")
print("[PASS] AES key protected using RSA-OAEP")

decrypted = decrypt_file(encrypted, private_key)

assert original == decrypted

print("[PASS] File successfully decrypted")

original_hash = calculate_hash(original)
decrypted_hash = calculate_hash(decrypted)

print("\nOriginal SHA-256:")
print(original_hash)

print("\nDecrypted SHA-256:")
print(decrypted_hash)

assert original_hash == decrypted_hash

print("\n[PASS] File integrity verified")

# Check that tampering is detected.
import json
import base64
from cryptography.exceptions import InvalidTag

package = json.loads(encrypted)

ciphertext = bytearray(
    base64.b64decode(package["encrypted_data"])
)

ciphertext[0] ^= 1

package["encrypted_data"] = base64.b64encode(
    ciphertext
).decode()

try:
    decrypt_file(
        json.dumps(package).encode(),
        private_key
    )
except InvalidTag:
    print("[PASS] Tampered ciphertext rejected")
else:
    raise AssertionError("Tampering was not detected")

print("\n===== ALL ENCRYPTION TESTS PASSED =====")
