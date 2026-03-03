import time
from typing import Dict, List

# In-memory storage (replace with database later)
_MEMORY_STORE: Dict[str, List[dict]] = {}


def store_message(user_id: str, role: str, content: str):
    if user_id not in _MEMORY_STORE:
        _MEMORY_STORE[user_id] = []

    _MEMORY_STORE[user_id].append({
        "role": role,
        "content": content,
        "timestamp": int(time.time())
    })


def get_memory(user_id: str):
    return _MEMORY_STORE.get(user_id, [])


def clear_memory(user_id: str):
    _MEMORY_STORE[user_id] = []
