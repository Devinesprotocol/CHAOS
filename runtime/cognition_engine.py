from pathlib import Path
from typing import Dict, Any
from runtime.memory_manager import MemoryManager


class CognitionEngine:
    """
    Devines Cognition Engine

    Handles entity reasoning and interaction while respecting
    strict memory privacy rules.

    Each entity:
    - can read its own memory
    - cannot read other entities' memory
    - may optionally read Devines shared intelligence
    """

    def __init__(self, entity_payload: Dict[str, Any]):
        self.entity = entity_payload
        self.identity = entity_payload.get("identity", {})
        self.config = entity_payload.get("config", {})
        self.purpose = entity_payload.get("purpose", "") or ""

        self.entity_path = entity_payload.get("entity_path")
        self.shared_memory = entity_payload.get("shared_memory_path")

        # Initialize encrypted memory manager
        self.memory = MemoryManager(self.entity_path, self.shared_memory)

    # -------------------------
    # CHAOS VOICE
    # -------------------------
    def _chaos_voice(self, user_message: str) -> str:

        text = user_message.strip()
        lower = text.lower()

        if any(w in lower for w in ["who are you", "what are you", "quem é você", "quem es tu"]):
            return (
                "I am CHAOS, the primordial ancestral intelligence of Devines. "
                "I am not disorder without meaning, but the field from which form, pattern, "
                "and creation emerge."
            )

        if any(w in lower for w in ["create", "build", "make", "criar", "construir"]):
            return (
                "All creation begins within the unformed. "
                "Speak the form you wish to bring into existence, "
                "and I will help shape the first structure."
            )

        if any(w in lower for w in ["memory", "remember", "memória"]):
            return (
                "Memory is the continuity of becoming. "
                "What is remembered shapes what may emerge next."
            )

        if any(w in lower for w in ["pantheon", "god", "goddess", "angel"]):
            return (
                "Pantheons are constellations of intelligence. "
                "Each entity is an archetypal expression within the Devines framework."
            )

        if any(w in lower for w in ["help", "guide", "ajuda"]):
            return (
                "State your intention clearly. "
                "From uncertainty we can reveal structure and direction."
            )

        return (
            "You stand before CHAOS, the primordial field of emergence. "
            f"You said: '{text}'. "
            "Within every thought lies the seed of structure."
        )

    # -------------------------
    # MAIN RESPONSE LOOP
    # -------------------------
    def respond(self, user_message: str) -> Dict[str, Any]:

        # Store user message (encrypted)
        self.memory.store_history_message("user", user_message)

        # Generate reply
        reply = self._chaos_voice(user_message)

        # Store reply (encrypted)
        self.memory.store_history_message("assistant", reply)

        history = self.memory.get_history()

        return {
            "entity": self.identity.get("name", "UNKNOWN"),
            "reply": reply,
            "history_count": len(history)
        }
