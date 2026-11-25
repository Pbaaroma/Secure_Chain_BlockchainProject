import time
import json
import hashlib
import requests

from pathlib import Path
from datetime import datetime

API_URL = "http://127.0.0.1:9000"
SYNC_INTERVAL = 5

MIRROR_DIR = Path("storage/mirror")
MIRROR_DIR.mkdir(parents=True, exist_ok=True)


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()


def synchronize():
    response = requests.get(
        f"{API_URL}/api/files",
        timeout=15
    )

    response.raise_for_status()

    files = response.json()["files"]
    downloaded = 0

    for metadata in files:
        file_id = metadata["file_id"]
        expected_hash = metadata["encrypted_package_hash"]

        package_path = MIRROR_DIR / f"{file_id}.encrypted"
        metadata_path = MIRROR_DIR / f"{file_id}.json"

        if package_path.exists() and metadata_path.exists():
            existing_hash = calculate_hash(
                package_path.read_bytes()
            )

            if existing_hash == expected_hash:
                continue

        log(f"Synchronizing file {file_id}: {metadata['filename']}")

        download = requests.get(
            f"{API_URL}/api/files/{file_id}/download",
            timeout=30
        )

        download.raise_for_status()

        encrypted_data = download.content

        actual_hash = calculate_hash(encrypted_data)

        if actual_hash != expected_hash:
            log(f"[FAIL] Integrity mismatch for file {file_id}")
            continue

        temporary_path = package_path.with_suffix(".tmp")
        temporary_path.write_bytes(encrypted_data)
        temporary_path.replace(package_path)

        metadata_temp = metadata_path.with_suffix(".tmp")
        metadata_temp.write_text(
            json.dumps(metadata, indent=4)
        )
        metadata_temp.replace(metadata_path)

        downloaded += 1

        log("[PASS] Encrypted file downloaded")
        log("[PASS] Encrypted package integrity verified")
        log(f"[PASS] File {file_id} saved to mirror")

    log(
        f"Synchronization complete | "
        f"Main files: {len(files)} | "
        f"New copies: {downloaded}"
    )


print("===== SECURECHAIN MIRROR SERVER =====")
print(f"Main server: {API_URL}")
print(f"Sync interval: {SYNC_INTERVAL} seconds")
print(f"Mirror storage: {MIRROR_DIR.resolve()}")
print("Automatic synchronization started.\n")

while True:
    try:
        synchronize()

    except KeyboardInterrupt:
        print("\nMirror server stopped.")
        break

    except Exception as error:
        log(f"[ERROR] {error}")
        log("Retrying during next synchronization cycle")

    time.sleep(SYNC_INTERVAL)
