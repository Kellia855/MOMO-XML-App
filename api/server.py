# server.py (moved into api/ package)
from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
from pydantic import BaseModel
import secrets
import os
import uvicorn
from datetime import datetime
from contextlib import asynccontextmanager

# --- Security (Basic Auth) ---
security = HTTPBasic()

# Prefer environment variables; fall back to development defaults for local testing.
# Set these in your environment (or a .env not committed to source control):
#   API_BASIC_USERNAME
#   API_BASIC_PASSWORD
USERNAME = os.getenv("API_BASIC_USERNAME", "apiuser")
PASSWORD = os.getenv("API_BASIC_PASSWORD", "apipass")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- Data Model ---
class Transaction(BaseModel):
    transaction_id: int
    sender_id: int
    receiver_id: int
    category_id: int
    amount: float
    transaction_date: str
    status: str

# In-memory "database"
transactions_db: List[Transaction] = []

# Seed data using FastAPI lifespan (recommended over on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed data
    if not transactions_db:
        transactions_db.append(
            Transaction(
                transaction_id=1,
                sender_id=100,
                receiver_id=200,
                category_id=1,
                amount=50.0,
                transaction_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="completed",
            )
        )
    yield
    # Shutdown: nothing to clean up

# Create the app with lifespan registered (recommended API)
app = FastAPI(title="MoMo Transactions API", version="1.0", lifespan=lifespan)

# --- CRUD Endpoints ---
@app.get("/transactions", response_model=List[Transaction])
def get_transactions(user: str = Depends(authenticate)):
    return transactions_db

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, user: str = Depends(authenticate)):
    for txn in transactions_db:
        if txn.transaction_id == transaction_id:
            return txn
    raise HTTPException(status_code=404, detail="Transaction not found")

@app.post("/transactions", response_model=Transaction, status_code=201)
def create_transaction(transaction: Transaction, user: str = Depends(authenticate)):
    transactions_db.append(transaction)
    return transaction

@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, updated_txn: Transaction, user: str = Depends(authenticate)):
    for idx, txn in enumerate(transactions_db):
        if txn.transaction_id == transaction_id:
            transactions_db[idx] = updated_txn
            return updated_txn
    raise HTTPException(status_code=404, detail="Transaction not found")

@app.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, user: str = Depends(authenticate)):
    for idx, txn in enumerate(transactions_db):
        if txn.transaction_id == transaction_id:
            del transactions_db[idx]
            return
    raise HTTPException(status_code=404, detail="Transaction not found")

# --- Convenience Endpoints ---
@app.get("/", include_in_schema=False)
def root():
    return {"message": "MoMo Transactions API is running", "docs_url": "/docs"}

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

# --- Minimal access log (screenshot-like) ---
@app.middleware("http")
async def simple_access_log(request: Request, call_next):
    # Only log /transactions* requests to mimic the desired console output
    path = request.url.path
    response = await call_next(request)
    if path.startswith("/transactions"):
        ts = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        client = request.client.host if request.client else "-"
        line = f"{client} - - [{ts}] \"{request.method} {path} HTTP/1.1\" {response.status_code} -"
        print(line, flush=True)
    return response

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    # Run the ASGI server programmatically so you can simply do: python api/server.py
    # Friendly startup message similar to your screenshot
    printable_host = "localhost" if host in ("127.0.0.1", "0.0.0.0") else host
    print(f"Starting server on http://{printable_host}:{port} ...")
    uvicorn.run(app, host=host, port=port, log_level="warning", access_log=False)
