from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.blockchain_client import blockchain_status

app = FastAPI(
    title="SecureChain API",
    description="Blockchain-Based Secure File Transfer System",
    version="1.0.0"
)

# Allow the local React frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "project": "SecureChain",
        "server": "Google Cloud Main Server",
        "status": "running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "SecureChain Backend"
    }


@app.get("/api/blockchain/status")
def get_blockchain_status():
    try:
        return blockchain_status()

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )


# SecureChain encrypted file transfer endpoints
from backend.file_routes import router as file_router

app.include_router(file_router)
