import time
from memory_manager import store_message, get_memory


async def process_message(
    message: str,
    wallet: str | None,
    ip: str | None,
    founder_command: bool | None,
    infra_action: str | None,
    infra_payload: dict | None,
):
    user_id = wallet or ip or "anonymous"

    # Store user message
    store_message(user_id, "user", message)

    # Simple echo runtime (replace with AI logic later)
    reply = f"CHAOS received: {message}"

    # Store assistant reply
    store_message(user_id, "assistant", reply)

    return {
        "status": "ok",
        "reply": reply,
        "memory_length": len(get_memory(user_id)),
        "timestamp": int(time.time())
    }
