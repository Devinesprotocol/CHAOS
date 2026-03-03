import os
import time
from openai import OpenAI

from backend.memory_manager import store_message, get_memory

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def process_message(message: str):
    user_id = "global_user"

    # Store user message
    store_message(user_id, "user", message)

    history = get_memory(user_id)

    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    store_message(user_id, "assistant", reply)

    return {
        "status": "ok",
        "reply": reply,
        "memory_length": len(get_memory(user_id)),
        "timestamp": int(time.time())
  }
