# Secure_Chain_Blockchain
Implematation of Blockchain and develop a file transfer using blockchain

![Python](https://img.shields.io/badge/Python-3.12-blue)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Solidity](https://img.shields.io/badge/Solidity-0.8.34-gray)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum-purple)
![Google Cloud](https://img.shields.io/badge/Deployment-Google%20Cloud-orange)
![Status](https://img.shields.io/badge/Status-Operational-green)

## 1. Project Overview

SecureChain is a blockchain-based secure file transfer system developed as part of our CSCI 311 Systems Programming final project.

The main purpose of this project is to demonstrate how encryption, blockchain technology, cloud computing and distributed storage can work together to provide secure and verifiable file transmission.

The system allows users to encrypt files locally, transmit encrypted data to a remote cloud server, register file information on a blockchain and automatically synchronize encrypted files with a mirror server.

We developed a React-based dashboard that allows users to upload, verify and recover files without manually interacting with the blockchain or using an external cryptocurrency wallet.

The project combines traditional cryptographic techniques with blockchain technology to improve data confidentiality, integrity, traceability and redundancy.

---

## 2. Project Objectives

- Establish a remotely accessible main server using Google Cloud.
- Implement secure file transmission using RSA encryption.
- Use AES-256-GCM for efficient file encryption.
- Integrate an Ethereum-based blockchain using Truffle and Ganache.
- Register file hashes and transaction information on a smart contract.
- Verify file integrity using SHA-256.
- Implement automatic mirror server synchronization.
- Support encrypted file recovery from the main and mirror storage.
- Detect unauthorized file modifications and corrupted encrypted data.
- Develop an interactive graphical user interface.
- Automate system startup and service monitoring.

---

## 3. Key Features

### Secure File Transfer

Files are encrypted on the local client before being transmitted to the remote cloud server.

The cloud server receives and stores encrypted file packages rather than the original plaintext files.

### Hybrid Encryption

SecureChain combines RSA-2048 and AES-256-GCM encryption.

AES encrypts the actual file content, while RSA protects the AES encryption key. This approach combines the advantages of asymmetric encryption with the efficiency of symmetric encryption.

### Blockchain Integration

Every successfully registered file receives a blockchain record containing its original SHA-256 hash and associated transaction information.

Blockchain registration is performed automatically through the Python Web3.py backend.

MetaMask is not required.

### File Integrity Verification

Users can verify whether a file matches its original blockchain record.

If the file has been modified, its calculated SHA-256 hash will no longer match the registered hash.

### Automatic Mirror Synchronization

The mirror server continuously checks the main server for new or updated encrypted file packages.

Synchronization occurs approximately every five seconds.

Encrypted package checksums are verified before replicated files are accepted into mirror storage.

### File Recovery

Users can recover encrypted files from either the main server or the mirror storage.

Files are decrypted locally using the RSA private key, and their integrity is verified against the blockchain record.

### Interactive Dashboard

The React dashboard provides:

- Blockchain connection status
- Smart contract status
- Current block number
- Main server status
- Mirror synchronization status
- Secure file uploads
- Blockchain-based integrity verification
- Main and mirror file recovery
- File transaction history

### Automated Service Management

Shell scripts simplify the startup and monitoring of cloud and local services.

---

## 4. System Architecture

SecureChain uses a distributed architecture consisting of a local client, a remote cloud server, an Ethereum development blockchain and a local mirror server.

```text
+-------------------------------------------------------+
|                    LOCAL PC                       |
|                                                       |
|  +--------------------+                               |
|  |  React Dashboard   |                               |
|  |     Port 5173      |                               |
|  +---------+----------+                               |
|            |                                          |
|  +---------v----------+                               |
|  |  Local Client API  |                               |
|  |     Port 9100      |                               |
|  +---------+----------+                               |
|            |                                          |
|  +---------v----------+     +----------------------+  |
|  | RSA + AES + SHA256 |     | Local Mirror Server  |  |
|  | Encryption Engine  |     | Encrypted Storage    |  |
|  +---------+----------+     +----------+-----------+  |
|            |                           |              |
+------------|---------------------------|--------------+
             |                           |
             |       SSH Tunnels         |
             |                           |
+------------v---------------------------v--------------+
|                     GOOGLE CLOUD                      |
|                                                       |
|  +-------------------------------------------------+  |
|  |           Docker Network                        |  |
|  |                                                 |  |
|  |  +------------------+    +-------------------+  |  |
|  |  | FastAPI Backend  +--->| Ganache Blockchain|  |  |
|  |  |    Port 9000     |    |    Port 7545      |  |  |
|  |  +--------+---------+    +---------+---------+  |  |
|  |           |                        |            |  |
|  |  +--------v---------+    +---------v---------+  |  |
|  |  | Encrypted File   |    | Solidity Smart    |  |  |
|  |  | Main Storage     |    | Contract          |  |  |
|  |  +------------------+    +-------------------+  |  |
|  +-------------------------------------------------+  |
|                                                       |
+-------------------------------------------------------+
```

### Architecture Components

| Component | Responsibility |
|---|---|
| React Dashboard | User interaction and system monitoring |
| Local Client API | Connects the frontend to local encryption and remote services |
| Encryption Engine | Encrypts and decrypts files locally |
| Google Cloud Server | Hosts the remote backend and blockchain infrastructure |
| FastAPI Backend | Processes encrypted uploads, downloads and blockchain registration |
| Ganache | Provides the Ethereum development blockchain |
| Truffle | Compiles and deploys Solidity smart contracts |
| Smart Contract | Registers file hashes and transaction information |
| Main Storage | Stores encrypted file packages |
| Mirror Server | Automatically replicates encrypted files |
| SSH Tunnels | Provides protected remote connectivity |

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend, encryption and synchronization |
| FastAPI | REST API development |
| Uvicorn | Python API server |
| React | Graphical user interface |
| Vite | Frontend development environment |
| JavaScript | Frontend functionality |
| CSS | Dashboard styling |
| Solidity | Smart contract development |
| Truffle | Smart contract compilation and deployment |
| Ganache | Ethereum development blockchain |
| Web3.py | Python-to-blockchain communication |
| Docker | Application containerization |
| Google Cloud Platform | Remote cloud infrastructure |
| Ubuntu | Local development and client environment |
| AlmaLinux | Cloud server operating system |
| Bash | Startup and monitoring automation |
| Git and GitHub | Version control and collaboration |

---

## 6. Security Implementation

SecureChain uses three primary cryptographic mechanisms.

### RSA-2048

RSA is an asymmetric encryption algorithm that uses a public and private key pair.

In SecureChain:

- The public key encrypts the AES encryption key.
- The private key decrypts the AES encryption key.
- RSA-OAEP padding with SHA-256 is used.
- The private key remains on the local client.

The private key is excluded from the GitHub repository.

### AES-256-GCM

AES is used to encrypt the actual file content.

SecureChain generates a random 256-bit AES key and a random nonce for file encryption.

Galois/Counter Mode provides authenticated encryption, allowing the system to detect modifications to encrypted file content.

### SHA-256

SHA-256 is used to generate a digital fingerprint of the original file.

The original file hash is registered on the blockchain.

A separate SHA-256 checksum is calculated for the encrypted package to verify storage and mirror consistency.

| Security Mechanism | Purpose |
|---|---|
| RSA-2048 | Protects the AES encryption key |
| AES-256-GCM | Protects file confidentiality and detects ciphertext modification |
| SHA-256 | Verifies file integrity |
| Blockchain | Maintains a traceable file registration record |
| SSH | Protects remote network communication |
| Mirror Synchronization | Provides encrypted file redundancy |

---

## 7. File Transmission Workflow

The secure file transmission process follows these steps:

1. The user selects a file through the React dashboard.
2. The local client calculates the original file's SHA-256 hash.
3. A random AES-256 encryption key is generated.
4. The original file is encrypted using AES-GCM.
5. The AES key is encrypted using the RSA public key.
6. An encrypted file package is created.
7. The encrypted package is transmitted to the remote cloud backend.
8. The backend registers the original file hash on the blockchain.
9. The blockchain returns a transaction receipt and file identifier.
10. The encrypted package and associated metadata are stored on the main server.
11. The mirror server detects the newly stored file.
12. The encrypted package is downloaded and its checksum is verified.
13. The encrypted package is stored in mirror storage.
14. The dashboard displays the updated file and blockchain information.

```text
Original File
      |
      v
SHA-256 Hash
      |
      v
AES-256-GCM Encryption
      |
      v
RSA Encryption of AES Key
      |
      v
Encrypted File Package
      |
      v
Remote Cloud Backend
      |
      +-------> Blockchain Registration
      |
      v
Main Server Storage
      |
      v
Automatic Mirror Synchronization
```

---

## 8. Blockchain Implementation

SecureChain uses a Solidity smart contract deployed to an Ethereum development blockchain provided by Ganache.

Truffle is used to compile and deploy the smart contract, while Web3.py allows the Python backend to interact with the deployed contract.

### Smart Contract Functions

| Function | Description |
|---|---|
| registerFile() | Registers file information and its SHA-256 hash |
| verifyFile() | Checks whether a supplied hash matches a registered file |
| getFile() | Retrieves registered file information |
| getFileCount() | Returns the total number of registered files |

### Blockchain Records

The smart contract maintains information including:

- File identifier
- File name
- Original file hash
- Sender address
- Recipient address
- Registration timestamp

The backend also records the transaction hash and block number as part of the file metadata.

The blockchain stores file registration information rather than the complete encrypted file.

### Current Development Blockchain

| Configuration | Value |
|---|---|
| Blockchain Platform | Ethereum |
| Blockchain Environment | Ganache |
| Chain ID | 1337 |
| RPC Port | 7545 |
| Solidity Version | 0.8.34 |
| Truffle Version | 5.11.5 |
| Ganache Version | 7.9.2 |

The current implementation uses Ganache development accounts to perform blockchain transactions automatically.

---

## 9. Mirror Server Implementation

The mirror server provides an additional copy of encrypted files stored on the main server.

A Python synchronization service periodically communicates with the main server to retrieve its file inventory.

### Synchronization Process

1. Request the current file inventory from the main server.
2. Identify new or changed encrypted packages.
3. Download the required encrypted files.
4. Calculate their SHA-256 checksums.
5. Compare the checksums with the main server metadata.
6. Store verified encrypted packages in mirror storage.
7. Repeat the process approximately every five seconds.

```text
Main Server
    |
    | File Inventory
    v
Mirror Synchronization Service
    |
    | Detect New or Changed Files
    v
Download Encrypted Packages
    |
    | Verify SHA-256 Checksums
    v
Local Mirror Storage
```

The mirror server stores encrypted data rather than plaintext files.

During testing, all four registered files were successfully replicated, and the main and mirror storage were confirmed to be synchronized.

---

## 10. Project Structure

The following structure shows the main components of the SecureChain repository.

```text
Secure_Chain_BlockchainProject/
|
|-- backend/
|   |-- __init__.py
|   |-- app.py
|   |-- blockchain_client.py
|   |-- encryption.py
|   |-- file_routes.py
|   |-- storage_manager.py
|   |-- test_encryption.py
|   |-- requirements.txt
|
|-- client/
|   |-- __init__.py
|   |-- encryption.py
|   |-- generate_keys.py
|   |-- local_api.py
|   |-- receiver.py
|   |-- sender.py
|   |-- test_security.py
|   |-- requirements.txt
|
|-- contracts/
|   |-- SecureFileTransfer.sol
|
|-- truffle-contracts/
|   |-- SecureFileTransfer.sol
|
|-- migrations/
|   |-- 1_deploy_secure_file_transfer.js
|
|-- deployment/
|   |-- Dockerfile.backend
|   |-- Dockerfile.truffle
|
|-- mirror_server/
|   |-- __init__.py
|   |-- sync.py
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   |-- api.js
|   |   |-- SecureChain.css
|   |   |-- SecureFileTransfer.json
|   |-- package.json
|
|-- scripts/
|   |-- start_cloud.sh
|   |-- start_local.sh
|   |-- stop_local.sh
|   |-- check_status.sh
|
|-- keys/                       # Generated locally, ignored by Git
|-- storage/                    # Runtime data, ignored by Git
|-- .venv/                      # Python environment, ignored by Git
|
|-- .gitignore
|-- truffle-config.cjs
|-- truffle-cloud-config.cjs
|-- README.md
```

---

## 11. Installation and Setup

### Prerequisites

The following software is required:

- Linux environment
- Python 3.12
- Node.js and npm
- Docker
- Git
- OpenSSH client
- curl
- Access to a remote Linux cloud server

### Clone the Repository

```bash
git clone -b cloud-deployment \
https://github.com/Pbaaroma/Secure_Chain_BlockchainProject.git

cd Secure_Chain_BlockchainProject
```

### Create the Python Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Install Client Dependencies

```bash
pip install -r client/requirements.txt
```

### Generate RSA Keys

```bash
mkdir -p keys

chmod 700 keys

python -m client.generate_keys
```

The RSA public and private keys are generated locally.

Do not upload the private key to GitHub or transfer it to the cloud server.

Existing private keys must be preserved to recover previously encrypted files.

### Install Frontend Dependencies

```bash
cd frontend

npm install

cd ..
```

### Prepare Runtime Storage

```bash
mkdir -p storage/mirror
mkdir -p storage/received
mkdir -p storage/test
mkdir -p storage/logs
mkdir -p storage/pids
```

---

## 12. Cloud Deployment

The remote infrastructure is hosted on Google Cloud using Docker containers.

### Create the Docker Network

On the remote cloud server:

```bash
docker network create securechain-network
```

### Create Persistent Docker Volumes

```bash
docker volume create securechain-blockchain-data

docker volume create securechain-main-storage
```

### Deploy Ganache

```bash
docker run -d \
  --name securechain-ganache \
  --network securechain-network \
  --restart unless-stopped \
  -p 127.0.0.1:7545:7545 \
  -v securechain-blockchain-data:/data \
  trufflesuite/ganache:v7.9.2 \
  --server.host 0.0.0.0 \
  --server.port 7545 \
  --chain.chainId 1337 \
  --chain.networkId 1337 \
  --wallet.totalAccounts 10 \
  --wallet.defaultBalance 1000 \
  --database.dbPath /data \
  --logging.quiet true
```

### Build the Truffle Container

```bash
docker build \
  -t securechain-truffle:1.0 \
  -f deployment/Dockerfile.truffle .
```

### Compile and Deploy the Smart Contract

```bash
docker run --rm \
  --network securechain-network \
  -v "$PWD:/app:Z" \
  -w /app \
  securechain-truffle:1.0 \
  truffle migrate \
  --network development \
  --config truffle-cloud-config.cjs
```

The `:Z` volume option is used for the AlmaLinux deployment with SELinux.

Save the contract address returned during deployment.

The migration generates the contract artifact required by the Python backend:

```text
build/contracts/SecureFileTransfer.json
```

### Build the Backend Container

```bash
docker build \
  -t securechain-backend:1.2 \
  -f deployment/Dockerfile.backend .
```

### Start the Backend

Replace `YOUR_DEPLOYED_CONTRACT_ADDRESS` with the actual address returned by Truffle.

```bash
docker run -d \
  --name securechain-backend \
  --network securechain-network \
  --restart unless-stopped \
  -p 127.0.0.1:9000:9000 \
  -v securechain-main-storage:/app/storage \
  -e STORAGE_DIR=/app/storage \
  -e BLOCKCHAIN_RPC_URL=http://securechain-ganache:7545 \
  -e CONTRACT_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS \
  securechain-backend:1.2
```

### Verify Cloud Services

```bash
docker ps --filter name=securechain
```

```bash
curl http://127.0.0.1:9000/api/blockchain/status
```

The blockchain and backend ports are bound to the cloud server's loopback interface rather than being directly exposed to the public internet.

These deployment commands are intended for initial setup. Existing deployments should use the startup scripts instead of recreating containers or redeploying the contract.

---

## 13. Running SecureChain

### Automated Startup

The project includes shell scripts to simplify service management.

Make the scripts executable:

```bash
chmod +x scripts/*.sh
```

### Start Cloud Services

On the remote cloud server:

```bash
./scripts/start_cloud.sh
```

### Start Local Services

On the local Ubuntu machine:

```bash
export SECURECHAIN_CLOUD_HOST="username@cloud-server-ip"

./scripts/start_local.sh
```

The local startup script manages:

- SSH tunnel connections
- Local FastAPI service
- Mirror synchronization
- React frontend

### Access the Application

| Service | Address |
|---|---|
| React Dashboard | http://127.0.0.1:5173 |
| Local Client API | http://127.0.0.1:9100 |
| Local API Documentation | http://127.0.0.1:9100/docs |
| Cloud Backend through SSH | http://127.0.0.1:9000 |
| Cloud API Documentation | http://127.0.0.1:9000/docs |
| Blockchain RPC through SSH | http://127.0.0.1:7545 |

### Check System Status

```bash
./scripts/check_status.sh
```

### Stop Managed Local Services

```bash
./scripts/stop_local.sh
```

The shutdown script is designed to stop local processes started by the automation script without deleting files or stopping the cloud infrastructure.

Manually started services are not automatically managed by this shutdown script.

---

## 14. Manual Startup

The individual services can also be started manually.

### SSH Tunnel for Blockchain

```bash
ssh -N \
  -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:7545:127.0.0.1:7545 \
  username@cloud-server-ip
```

### SSH Tunnel for Backend

```bash
ssh -N \
  -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:9000:127.0.0.1:9000 \
  username@cloud-server-ip
```

Keep both SSH connections running in separate terminals.

### Start the Local Client API

```bash
source .venv/bin/activate

python -m uvicorn client.local_api:app \
  --host 127.0.0.1 \
  --port 9100
```

### Start Mirror Synchronization

In a separate terminal:

```bash
source .venv/bin/activate

python -m mirror_server.sync
```

### Start the React Frontend

In another terminal:

```bash
cd frontend

npm run dev -- \
  --host 127.0.0.1 \
  --port 5173 \
  --strictPort
```

Open the React dashboard at:

```text
http://127.0.0.1:5173
```

---

## 15. API Endpoints

### Cloud Backend API

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Backend information |
| GET | /api/health | Backend health status |
| GET | /api/blockchain/status | Blockchain connection and contract status |
| GET | /api/files | List stored files |
| POST | /api/files/upload | Upload encrypted file packages |
| GET | /api/files/{file_id}/download | Download an encrypted file |
| GET | /api/files/{file_id}/metadata | Retrieve storage and blockchain metadata |

### Local Client API

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/status | Retrieve overall system status |
| GET | /api/files | Retrieve file history |
| POST | /api/upload | Encrypt and transmit a file |
| POST | /api/verify/{file_id} | Verify original file integrity |
| GET | /api/recover/{file_id}/{source} | Recover and decrypt a file |

The local client API performs encryption and decryption operations before communicating with the remote backend or returning recovered files to the browser.

---

## 16. Command-Line File Transfer

SecureChain supports both graphical and command-line interaction.

Activate the local Python environment:

```bash
source .venv/bin/activate
```

### Create a Test File

```bash
mkdir -p storage/test

echo "SecureChain encrypted file transfer test." \
  > storage/test/demo.txt
```

### Send a File

```bash
python -m client.sender storage/test/demo.txt
```

The sender encrypts the file locally, uploads the encrypted package and displays blockchain transaction information.

### Recover a File from the Main Server

```bash
python -m client.receiver 1 main
```

### Recover a File from the Mirror Server

```bash
python -m client.receiver 1 mirror
```

Replace `1` with the appropriate registered file identifier.

Recovered files are stored in:

```text
storage/received/
```

The receiver verifies the encrypted package checksum, decrypts the file and compares its original hash against the blockchain record.

---

## 17. Testing and Validation

Several tests were performed throughout the development process to verify the functionality and security of SecureChain.

### Encryption Testing

The following operations were tested:

- RSA key generation
- AES-256 file encryption
- RSA encryption of the AES key
- Successful file decryption
- Original and decrypted file comparison
- Ciphertext modification detection

Run the backend encryption test:

```bash
docker run --rm \
  securechain-backend:1.2 \
  python -m backend.test_encryption
```

### Security Testing

Security tests were performed to verify that unauthorized modifications could be detected.

```bash
python -m client.test_security
```

The security test uses the existing demonstration files and requires the local RSA keys and relevant runtime data.

| Security Test | Result |
|---|---|
| Valid encrypted mirror file | PASS |
| Modified plaintext detection | PASS |
| Encrypted package checksum verification | PASS |
| Modified ciphertext detection | PASS |
| Original and decrypted hash comparison | PASS |

### Mirror Synchronization Testing

Encrypted file checksums were compared between the main server and mirror storage.

On the cloud server:

```bash
docker exec securechain-backend \
  sh -c 'sha256sum /app/storage/*.encrypted'
```

On the local Ubuntu machine:

```bash
sha256sum storage/mirror/*.encrypted
```

Matching checksums confirm that the replicated encrypted packages are identical.

### Graphical Interface Testing

The following dashboard operations were successfully demonstrated:

- Secure file upload
- Automatic blockchain registration
- File history updates
- Main and mirror synchronization
- Blockchain-based file verification
- File recovery

---

## 18. Experimental Results

The final system status during our demonstration testing was:

| System Component | Result |
|---|---|
| Blockchain Connected | True |
| Blockchain Chain ID | 1337 |
| Blockchain Block Number | 5 |
| Smart Contract Deployed | True |
| Registered Blockchain Files | 4 |
| Main Server Status | Online |
| Main Server Files | 4 |
| Mirror Server Files | 4 |
| Mirror Synchronized | True |
| Local Client API | Running |
| React Frontend | Reachable |

These results demonstrate that SecureChain successfully integrates encrypted file transmission, blockchain registration, remote storage and automatic mirror synchronization.

### Verified System Output

```json
{
    "connected": true,
    "chain_id": 1337,
    "block_number": 5,
    "contract_deployed": true,
    "registered_files": 4,
    "main_server": "online",
    "main_files": 4,
    "mirror_files": 4,
    "mirror_synchronized": true
}
```

The block number and registered file count will increase as additional files are registered.

---

## 19. Data Protection and Storage

The project separates source code from sensitive and runtime information.

The following directories and files are excluded from version control:

```text
keys/
storage/
backend/storage/
.venv/
__pycache__/
*.pyc
.env
```

This prevents private RSA keys, encrypted runtime files, recovered plaintext files and local environment information from being unintentionally committed to GitHub.

Docker volumes provide persistent storage for the blockchain database and main server encrypted files.

---

## 20. Project Challenges and Solutions

| Challenge | Solution |
|---|---|
| Establishing remote blockchain connectivity | Configured SSH port forwarding |
| Managing cloud dependencies | Used Docker containers |
| Integrating Python with Ethereum | Implemented Web3.py communication |
| Encrypting files efficiently | Combined RSA and AES encryption |
| Maintaining file integrity | Implemented SHA-256 verification |
| Maintaining consistent storage | Developed automatic mirror synchronization |
| Detecting modified encrypted files | Used checksums and AES-GCM authentication |
| Connecting the frontend to local encryption | Developed a dedicated local FastAPI service |
| Avoiding manual wallet interactions | Automated blockchain registration through the backend |
| Managing multiple running services | Developed Bash startup and monitoring scripts |
| Combining local and cloud development | Used Git branches and GitHub version control |

---

## 21. Current Limitations

SecureChain is an academic proof-of-concept rather than a production-ready file transfer platform.

The current implementation has the following limitations:

- Ganache is a development blockchain rather than a decentralized production blockchain.
- Blockchain transactions use Ganache development accounts.
- The current encryption workflow uses a locally generated RSA key pair.
- Multi-user authentication and authorization have not been implemented.
- The local private key is protected through file permissions but is not password-encrypted.
- Mirror synchronization uses periodic polling rather than event-driven replication.
- Mirror recovery currently requires access to blockchain metadata through the main backend.
- Blockchain registration and file storage are separate operations rather than a single atomic transaction.
- The shutdown script and complete fresh installation procedure have not been fully runtime-tested.

These limitations provide opportunities for future development.

---

## 22. Future Improvements

Potential improvements to SecureChain include:

- Multi-user authentication and authorization
- Individual sender and recipient RSA key pairs
- Role-based access control
- Password-protected private keys
- Production blockchain integration
- HTTPS and production API deployment
- Independent remote mirror servers
- Event-driven file synchronization
- Offline mirror recovery
- Blockchain and storage transaction reconciliation
- Automated backup and disaster recovery
- File versioning
- Performance and scalability testing
- Automated CI/CD pipelines
- Production-ready container orchestration

---

## 23. Project Collaboration

The project was developed collaboratively using Git and GitHub.

Development responsibilities included smart contract implementation, frontend development, cloud deployment, encryption, backend integration, mirror synchronization and system testing.

### Development Branches

| Branch | Purpose |
|---|---|
| main | Main project integration branch |
| blockchain_development | Initial blockchain and frontend development |
| cloud-deployment | Cloud deployment and integrated SecureChain implementation |

The development branches allow different components to be implemented and tested before integration into the main branch.

---

## 24. Conclusion

SecureChain demonstrates how blockchain technology can be combined with traditional encryption methods to improve secure file transmission.

Throughout this project, we implemented a complete file transfer workflow that includes local encryption, remote cloud communication, blockchain registration, encrypted storage, automatic mirror synchronization and file recovery.

One of the most important aspects of this project is that the original file is encrypted before leaving the local client. The blockchain provides a traceable record that can be used to verify the integrity of recovered files, while the mirror server provides an additional encrypted copy.

This project also gave us practical experience with distributed systems, cloud computing, cryptography, blockchain development, Docker containerization, network communication and full-stack application development.

The successful testing of these components demonstrates how different technologies can work together to create a functional secure file transfer prototype.

---

## 25. References and Documentation

- Python Documentation: https://docs.python.org/3/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- Solidity Documentation: https://docs.soliditylang.org/
- Ethereum Documentation: https://ethereum.org/en/developers/docs/
- Web3.py Documentation: https://web3py.readthedocs.io/
- Truffle Repository: https://github.com/trufflesuite/truffle
- Ganache Repository: https://github.com/trufflesuite/ganache
- Docker Documentation: https://docs.docker.com/
- Google Cloud Documentation: https://cloud.google.com/docs
- Python Cryptography Documentation: https://cryptography.io/en/latest/
- Vite Documentation: https://vite.dev/

---

## Academic Information

**Course:** CSCI 311 — Systems Programming

**Project:** SecureChain — Blockchain-Based Secure File Transfer System

**Institution:** Saint Cloud State University

**Semester:** Fall 2026

**Project Type:** Collaborative Final Project

**Development Environment:** Ubuntu and Google Cloud Platform

**Project Status:** Implemented and tested as an academic prototype.

---

<div align="center">

### SecureChain

**Encrypt Locally. Transfer Securely. Verify with Blockchain.**

Built with Python, React, Solidity, Docker and Google Cloud.

</div>
