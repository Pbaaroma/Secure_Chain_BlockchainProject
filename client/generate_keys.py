import os
from pathlib import Path
from client.encryption import generate_rsa_keys

os.umask(0o077)

keys_dir = Path("keys")
keys_dir.mkdir(mode=0o700, exist_ok=True)

private_path = keys_dir / "private_key.pem"
public_path = keys_dir / "public_key.pem"

if private_path.exists() or public_path.exists():
    raise SystemExit(
        "Keys already exist. Refusing to overwrite them."
    )

private_key, public_key = generate_rsa_keys()

private_path.write_bytes(private_key)
public_path.write_bytes(public_key)

private_path.chmod(0o600)

print("[PASS] RSA-2048 key pair generated")
print("[PASS] Private key stored locally")
print("[PASS] Public key ready for encryption")
