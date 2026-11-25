import os
import json
import base64
import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()


def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


def encrypt_file(data, public_key_pem):
    public_key = serialization.load_pem_public_key(
        public_key_pem
    )

    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)

    aes = AESGCM(aes_key)

    encrypted_data = aes.encrypt(
        nonce,
        data,
        None
    )

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    package = {
        "algorithm": "RSA-2048-OAEP + AES-256-GCM",
        "encrypted_key": base64.b64encode(
            encrypted_key
        ).decode(),
        "nonce": base64.b64encode(
            nonce
        ).decode(),
        "encrypted_data": base64.b64encode(
            encrypted_data
        ).decode()
    }

    return json.dumps(package).encode()


def decrypt_file(package_data, private_key_pem):
    package = json.loads(package_data)

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )

    encrypted_key = base64.b64decode(
        package["encrypted_key"]
    )

    nonce = base64.b64decode(
        package["nonce"]
    )

    encrypted_data = base64.b64decode(
        package["encrypted_data"]
    )

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    aes = AESGCM(aes_key)

    return aes.decrypt(
        nonce,
        encrypted_data,
        None
    )
