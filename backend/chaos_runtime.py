import time
from backend.memory_manager import store_message, get_memory


async def process_message(message: str):
    user_id = "global_user"

    # Store user message
    store_message(user_id, "user", message)

    reply = f"CHAOS received: {message}"

    # Store assistant reply
    store_message(user_id, "assistant", reply)

    return {
        "status": "ok",
        "reply": reply,
        "memory_length": len(get_memory(user_id)),
        "timestamp": int(time.time())
    }
