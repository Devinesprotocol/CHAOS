import secrets
import hashlib
import time

# Simple in-memory nonce store (replace with persistent storage later)
_NONCE_STORE = {}

NONCE_EXPIRATION_SECONDS = 300  # 5 minutes


def generate_nonce(wallet: str) -> str:
    nonce = secrets.token_hex(16)
    _NONCE_STORE[wallet] = {
        "nonce": nonce,
        "created_at": int(time.time())
    }
    return nonce


def verify_founder_signature(wallet: str, signature: str) -> bool:
    """
    Placeholder verification.
    Replace with real cryptographic wallet signature verification later.
    """

    record = _NONCE_STORE.get(wallet)
    if not record:
        return False

    if int(time.time()) - record["created_at"] > NONCE_EXPIRATION_SECONDS:
        return False

    # For now we simulate validation by checking:
    expected = hashlib.sha256((wallet + record["nonce"]).encode()).hexdigest()

    return signature == expected
