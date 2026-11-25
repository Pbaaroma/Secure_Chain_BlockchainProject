import os
import json
from pathlib import Path

STORAGE_DIR = Path(
    os.getenv("STORAGE_DIR", "/app/storage")
)

STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_file(file_id, encrypted_data, metadata):
    file_id = int(file_id)

    package_path = STORAGE_DIR / f"{file_id}.encrypted"
    metadata_path = STORAGE_DIR / f"{file_id}.json"

    package_temp = STORAGE_DIR / f"{file_id}.encrypted.tmp"
    metadata_temp = STORAGE_DIR / f"{file_id}.json.tmp"

    package_temp.write_bytes(encrypted_data)
    package_temp.replace(package_path)

    metadata_temp.write_text(
        json.dumps(metadata, indent=4)
    )
    metadata_temp.replace(metadata_path)

    return package_path


def list_files():
    files = []

    for path in STORAGE_DIR.glob("*.json"):
        metadata = json.loads(path.read_text())

        if get_file_path(metadata["file_id"]).is_file():
            files.append(metadata)

    return sorted(
        files,
        key=lambda item: item["file_id"]
    )


def get_file_path(file_id):
    return STORAGE_DIR / f"{int(file_id)}.encrypted"


def get_metadata(file_id):
    path = STORAGE_DIR / f"{int(file_id)}.json"

    if not path.exists():
        raise FileNotFoundError("File metadata not found")

    return json.loads(path.read_text())
