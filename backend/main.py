import os
import time
import asyncio
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from founder_auth import generate_nonce, verify_founder_signature
from chaos_runtime import process_message
from memory_manager import load_memory, append_interaction
from infra_manager import audit_and_correct_service_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_HEALTH_ENV = [
    "OPENAI_API_KEY",
    "RPC_URL",
    "FOUNDER_WALLET_PUBLIC_KEY",
    "CHAOS_TOKEN_MINT",
    "MIN_TOKEN_HOLDING",
    "VAULT_MASTER_SECRET",
    "VAULT_FILE_PATH",
    "RENDER_API_KEY",
    "RENDER_SERVICE_ID",
]

REQUIRED_CHAT_INTEGRITY_ENV = [
    "OPENAI_API_KEY",
    "RPC_URL",
    "FOUNDER_WALLET_PUBLIC_KEY",
    "CHAOS_TOKEN_MINT",
    "MIN_TOKEN_HOLDING",
    "VAULT_MASTER_SECRET",
]

RPC_HEALTH_CACHE_TTL_SECONDS = 60
_rpc_health_cache = {
    "checked_at": 0,
    "ok": True,
    "error": None,
}

_audit_task = None


class ChatRequest(BaseModel):
    message: str
    wallet: str | None = None
    founder_command: bool | None = False
    infra_action: str | None = None
    infra_payload: dict | None = None


class FounderNonceRequest(BaseModel):
    wallet: str


def _safe_log_integrity_failure(reason: str):
    try:
        append_interaction("CONFIG_INTEGRITY_FAILURE", reason)
    except Exception:
        pass


def _validate_chat_config_integrity() -> tuple[bool, str | None]:
    vault_path = os.getenv("VAULT_FILE_PATH", "")
    if not vault_path.startswith("/data"):
        return False, "VAULT_FILE_PATH must begin with /data."

    missing = [key for key in REQUIRED_CHAT_INTEGRITY_ENV if not os.getenv(key)]
    if missing:
        return False, "Missing required environment variables for runtime integrity."

    return True, None


def _rpc_health_cached() -> dict:
    now = time.time()
    if now - _rpc_health_cache["checked_at"] < RPC_HEALTH_CACHE_TTL_SECONDS:
        return _rpc_health_cache

    rpc_url = os.getenv("RPC_URL", "")
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getHealth"}

    try:
        resp = requests.post(rpc_url, json=payload, timeout=6)
        ok = resp.status_code < 400
        _rpc_health_cache.update({
            "checked_at": now,
            "ok": ok,
            "error": None if ok else f"HTTP {resp.status_code}",
        })
    except Exception as exc:
        _rpc_health_cache.update({
            "checked_at": now,
            "ok": False,
            "error": type(exc).__name__,
        })

    return _rpc_health_cache


@app.get("/")
async def root():
    return {"status": "CHAOS backend active"}


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": int(time.time())}


@app.post("/chat")
async def chat(req: ChatRequest):
    response = await process_message(
        req.message,
        req.wallet,
        None,
        req.founder_command,
        req.infra_action,
        req.infra_payload
    )
    return response
