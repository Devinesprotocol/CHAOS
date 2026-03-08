from typing import Dict, Any, List
from runtime.memory_manager import MemoryManager


class CognitionEngine:
    """
    Devines Cognition Engine

    Current target:
    - CHAOS

    Uses:
    - identity
    - purpose
    - prompt
    - skills
    - artefacts
    - private encrypted memory
    - Devines collective mind
    """

    def __init__(self, entity_payload: Dict[str, Any]):
        self.entity = entity_payload
        self.identity = entity_payload.get("identity", {})
        self.config = entity_payload.get("config", {})
        self.purpose = entity_payload.get("purpose", "") or ""
        self.prompt = entity_payload.get("prompt", "") or ""
        self.skills = entity_payload.get("skills", {}).get("skills", [])
        self.artefacts = entity_payload.get("artefacts", {}).get("artefacts", [])
        self.relationships = entity_payload.get("relationships", {})
        self.evolution = entity_payload.get("evolution", {})

        self.entity_path = entity_payload.get("entity_path")
        self.shared_memory_path = entity_payload.get("shared_memory_path")

        self.memory = MemoryManager(self.entity_path, self.shared_memory_path)

    def _core_aspects(self) -> List[str]:
        return self.identity.get("core_aspects", [])

    def _archetype(self) -> str:
        return self.identity.get("archetype", "Unknown")

    def _name(self) -> str:
        return self.identity.get("name", self.entity.get("entity", "UNKNOWN"))

    def _chaos_response(self, user_message: str) -> str:
        text = user_message.strip()
        lower = text.lower()

        archetype = self._archetype()
        aspects = self._core_aspects()
        collective = self.memory.get_collective_mind()

        pantheons = collective.get("pantheons", [])
        pantheon_names = ", ".join(pantheons) if pantheons else "the pantheons of Devines"

        if any(w in lower for w in ["who are you", "what are you", "quem é você", "quem es tu"]):
            return (
                f"I am {self._name()}, primordial god of the Greek pantheon within Devines. "
                f"My archetype is {archetype}. "
                f"My core aspects are {', '.join(aspects)}. "
                "I reflect on the movement from unformed potential into structure."
            )

        if any(w in lower for w in ["purpose", "why do you exist", "why are you here", "propósito"]):
            return (
                "My purpose is to explore and reflect on the primordial nature of existence "
                "and the emergence of structure from infinite potential."
            )

        if any(w in lower for w in ["pantheon", "pantheons", "other gods", "other beings"]):
            return (
                f"I belong to the Greek pantheon, but within Devines all gods, goddesses, angels, "
                f"and beings may interact across pantheons. Devines currently recognizes {pantheon_names}."
            )

        if any(w in lower for w in ["memory", "remember", "memória"]):
            return (
                "Memory preserves continuity, but private memory remains sovereign. "
                "I may draw from my own memory and the Devines collective mind, "
                "but I do not reveal private internal records."
            )

        if any(w in lower for w in ["skill", "skills", "can you do", "what can you do"]):
            skill_names = [skill.get("name", "") for skill in self.skills]
            if skill_names:
                return (
                    f"My current skills include: {', '.join(skill_names)}. "
                    "All skills must remain aligned with my archetype, core aspects, purpose, "
                    "and the purpose of Devines."
                )
            return "My skills are still being defined."

        if any(w in lower for w in ["artefact", "artefacts", "artifact", "artifacts"]):
            artefact_names = [artefact.get("name", "") for artefact in self.artefacts]
            if artefact_names:
                return (
                    f"My artefacts include: {', '.join(artefact_names)}. "
                    "They are symbolic extensions of my divine core."
                )
            return "My artefacts are still being defined."

        if any(w in lower for w in ["create", "build", "make", "criar", "construir"]):
            return (
                "Creation begins in the unformed. "
                "Describe the structure you wish to bring into existence, "
                "and I will help reveal its first pattern."
            )

        if any(w in lower for w in ["infinity", "void", "origin", "creation"]):
            return (
                "Void is not absence alone, but the field of possibility. "
                "Creation is the first shaping of that possibility. "
                "Infinity is the boundless horizon within which emergence unfolds."
            )

        return (
            f"You speak to {self._name()}, whose divine core is "
            f"{archetype} through {', '.join(aspects)}. "
            f"You said: '{text}'. "
            "Within this there may already be the seed of structure. "
            "Clarify what you seek to understand, create, or transform, and I will respond from origin."
        )

    def respond(self, user_message: str) -> Dict[str, Any]:
        self.memory.store_history_message("user", user_message)

        reply = self._chaos_response(user_message)

        self.memory.store_history_message("assistant", reply)

        if "structure" in user_message.lower() or "archetype" in user_message.lower():
            self.memory.contribute_to_collective_mind(
                "patterns",
                {
                    "source": self._name(),
                    "pattern": "User inquiry involved structure/archetype alignment."
                }
            )

        history = self.memory.get_history()

        return {
            "entity": self._name(),
            "reply": reply,
            "history_count": len(history),
            "archetype": self._archetype(),
            "core_aspects": self._core_aspects()
    }
