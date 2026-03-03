import time

async def process_message(message: str):
    return {
        "status": "ok",
        "reply": f"CHAOS received: {message}",
        "timestamp": int(time.time())
    }
