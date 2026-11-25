import hashlib
import json
import base64
import re

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.responses import FileResponse

from backend.blockchain_client import (
    register_file,
    get_file
)

from backend.storage_manager import (
    save_file,
    list_files,
    get_file_path,
    get_metadata
)

router = APIRouter(prefix="/api/files")

MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    filename: str = Form(...),
    file_hash: str = Form(...)
):
    file_hash = file_hash.lower().removeprefix("0x")

    if not re.fullmatch(r"[0-9a-f]{64}", file_hash):
        raise HTTPException(
            status_code=400,
            detail="Invalid SHA-256 hash"
        )

    if not filename or len(filename) > 255:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

    encrypted_data = await file.read(MAX_FILE_SIZE + 1)

    if not encrypted_data:
        raise HTTPException(
            status_code=400,
            detail="Empty file package"
        )

    if len(encrypted_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Encrypted package exceeds 20 MB"
        )

    try:
        package = json.loads(encrypted_data)

        if package["algorithm"] != "RSA-2048-OAEP + AES-256-GCM":
            raise ValueError("Unsupported encryption algorithm")

        encrypted_key = base64.b64decode(
            package["encrypted_key"], validate=True
        )

        nonce = base64.b64decode(
            package["nonce"], validate=True
        )

        ciphertext = base64.b64decode(
            package["encrypted_data"], validate=True
        )

        if len(encrypted_key) != 256:
            raise ValueError("Invalid RSA encrypted key")

        if len(nonce) != 12 or len(ciphertext) < 16:
            raise ValueError("Invalid encrypted data")

    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid encrypted file package"
        )

    try:
        transaction = register_file(
            filename,
            "0x" + file_hash
        )

        metadata = {
            **transaction,
            "filename": filename,
            "file_hash": file_hash,
            "encrypted_package_hash": hashlib.sha256(
                encrypted_data
            ).hexdigest(),
            "encrypted_size": len(encrypted_data)
        }

        save_file(
            transaction["file_id"],
            encrypted_data,
            metadata
        )

        return {
            "status": "success",
            "message": "Encrypted file stored and registered",
            **metadata
        }

    except Exception as error:
        print(f"Upload failed: {error}")

        raise HTTPException(
            status_code=500,
            detail="File registration or storage failed"
        )


@router.get("")
def files():
    return {
        "files": list_files()
    }


@router.get("/{file_id}/download")
def download_file(file_id: int):
    path = get_file_path(file_id)

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Encrypted file not found"
        )

    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=f"{file_id}.encrypted"
    )


@router.get("/{file_id}/metadata")
def file_metadata(file_id: int):
    try:
        metadata = get_metadata(file_id)

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "storage": metadata,
        "blockchain": get_file(file_id)
    }
