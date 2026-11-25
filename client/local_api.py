import requests

from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from client.encryption import (
    encrypt_file,
    decrypt_file,
    calculate_hash
)

app = FastAPI(title="SecureChain Local Client API")

MAIN_API = "http://127.0.0.1:9000"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


def main_get(endpoint):
    response = requests.get(
        f"{MAIN_API}{endpoint}",
        timeout=30
    )
    response.raise_for_status()
    return response


@app.get("/api/status")
def status():
    try:
        blockchain = main_get(
            "/api/blockchain/status"
        ).json()

        files = main_get("/api/files").json()["files"]

        mirror = Path("storage/mirror")

        mirrored = sum(
            1 for item in files
            if (
                mirror / f"{item['file_id']}.encrypted"
            ).is_file()
            and calculate_hash(
                (mirror / f"{item['file_id']}.encrypted").read_bytes()
            ) == item["encrypted_package_hash"]
        )

        return {
            **blockchain,
            "main_server": "online",
            "main_files": len(files),
            "mirror_files": mirrored,
            "mirror_synchronized": mirrored == len(files)
        }

    except Exception as error:
        raise HTTPException(503, str(error))


@app.get("/api/files")
def files():
    try:
        return main_get("/api/files").json()
    except Exception as error:
        raise HTTPException(503, str(error))


@app.post("/api/upload")
def upload(file: UploadFile = File(...)):
    try:
        original = file.file.read(14 * 1024 * 1024 + 1)

        if len(original) > 14 * 1024 * 1024:
            raise HTTPException(413, "File exceeds 14 MiB")

        public_key = Path(
            "keys/public_key.pem"
        ).read_bytes()

        file_hash = calculate_hash(original)

        encrypted = encrypt_file(
            original,
            public_key
        )

        response = requests.post(
            f"{MAIN_API}/api/files/upload",
            files={
                "file": (
                    file.filename + ".encrypted",
                    encrypted,
                    "application/octet-stream"
                )
            },
            data={
                "filename": file.filename,
                "file_hash": file_hash
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(500, str(error))


@app.post("/api/verify/{file_id}")
def verify(file_id: int, file: UploadFile = File(...)):
    try:
        metadata = main_get(
            f"/api/files/{file_id}/metadata"
        ).json()

        actual = calculate_hash(file.file.read())

        expected = metadata["blockchain"]["file_hash"]
        expected = expected.lower().removeprefix("0x")

        return {
            "verified": actual == expected,
            "file_id": file_id,
            "expected_hash": expected,
            "actual_hash": actual
        }

    except Exception as error:
        raise HTTPException(500, str(error))


@app.get("/api/recover/{file_id}/{source}")
def recover(file_id: int, source: str):
    if source not in ["main", "mirror"]:
        raise HTTPException(400, "Invalid recovery source")

    try:
        metadata = main_get(
            f"/api/files/{file_id}/metadata"
        ).json()

        if source == "mirror":
            encrypted = Path(
                f"storage/mirror/{file_id}.encrypted"
            ).read_bytes()
        else:
            encrypted = main_get(
                f"/api/files/{file_id}/download"
            ).content

        expected_package_hash = metadata[
            "storage"
        ]["encrypted_package_hash"]

        if calculate_hash(encrypted) != expected_package_hash:
            raise HTTPException(
                409,
                "Encrypted package integrity mismatch"
            )

        private_key = Path(
            "keys/private_key.pem"
        ).read_bytes()

        original = decrypt_file(
            encrypted,
            private_key
        )

        expected = metadata["blockchain"]["file_hash"]
        expected = expected.lower().removeprefix("0x")

        if calculate_hash(original) != expected:
            raise HTTPException(
                409,
                "Blockchain integrity verification failed"
            )

        return Response(
            content=original,
            media_type="application/octet-stream"
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(500, str(error))
