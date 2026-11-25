import os
import json
from pathlib import Path
from web3 import Web3

# Blockchain connection configuration
RPC_URL = os.getenv(
    "BLOCKCHAIN_RPC_URL",
    "http://securechain-ganache:7545"
)

CONTRACT_ADDRESS = os.getenv(
    "CONTRACT_ADDRESS",
    "0x0835659B2725c0Cb797F5306FbBcA002cB383ff8"
)

ARTIFACT_PATH = Path(
    os.getenv(
        "CONTRACT_ARTIFACT",
        "/app/build/contracts/SecureFileTransfer.json"
    )
)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Load the compiled smart contract ABI
with ARTIFACT_PATH.open() as artifact_file:
    artifact = json.load(artifact_file)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=artifact["abi"]
)


def blockchain_status():
    if not w3.is_connected():
        raise ConnectionError("Cannot connect to Ganache")

    return {
        "connected": True,
        "chain_id": w3.eth.chain_id,
        "block_number": w3.eth.block_number,
        "contract_address": contract.address,
        "contract_deployed": bool(
            w3.eth.get_code(contract.address)
        ),
        "registered_files": contract.functions.getFileCount().call()
    }


def register_file(filename, file_hash, recipient=None):
    sender = w3.eth.accounts[0]

    if recipient is None:
        recipient = sender

    recipient = Web3.to_checksum_address(recipient)

    tx_hash = contract.functions.registerFile(
        filename,
        Web3.to_bytes(hexstr=file_hash),
        recipient
    ).transact({"from": sender})

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status != 1:
        raise RuntimeError("Blockchain transaction failed")

    events = contract.events.FileRegistered().process_receipt(
        receipt
    )

    return {
        "file_id": events[0]["args"]["fileId"],
        "transaction_hash": Web3.to_hex(tx_hash),
        "block_number": receipt.blockNumber,
        "sender": sender,
        "recipient": recipient
    }


def verify_file(file_id, file_hash):
    return contract.functions.verifyFile(
        int(file_id),
        Web3.to_bytes(hexstr=file_hash)
    ).call()


def get_file(file_id):
    record = contract.functions.getFile(int(file_id)).call()

    return {
        "filename": record[0],
        "file_hash": Web3.to_hex(record[1]),
        "sender": record[2],
        "recipient": record[3],
        "timestamp": record[4]
    }
