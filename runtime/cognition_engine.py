import os
from typing import Dict, Any, List

from openai import OpenAI
from runtime.memory_manager import MemoryManager


class CognitionEngine:
    """
    Devines Cognition Engine

    Uses:
    - being identity
    - prompt
    - purpose
    - skills
    - artefacts
    - private memory
    - collective mind
    - OpenAI API model in the background
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
        self.alignment = entity_payload.get("alignment", {})

        self.entity_path = entity_payload.get("entity_path")
        self.shared_memory_path = entity_payload.get("shared_memory_path")

        self.memory = MemoryManager(self.entity_path, self.shared_memory_path)
        self.client = OpenAI(api_key=os.environ.get("DEVINES_OPENAI_KEY"))

        self.model = os.environ.get("DEVINES_MODEL", "gpt-5.4")

    def _name(self) -> str:
        return self.identity.get("name", self.entity.get("entity", "UNKNOWN"))

    def _archetype(self) -> str:
        return self.identity.get("archetype", "Unknown")

    def _core_aspects(self) -> List[str]:
        return self.identity.get("core_aspects", [])

    def _purpose(self) -> str:
        identity_purpose = self.identity.get("purpose", "")
        if identity_purpose:
            return identity_purpose
        return self.purpose.strip()

    def _skill_names(self) -> List[str]:
        return [skill.get("name", "") for skill in self.skills if skill.get("name")]

    def _artefact_names(self) -> List[str]:
        return [artefact.get("name", "") for artefact in self.artefacts if artefact.get("name")]

    def _build_system_prompt(self) -> str:
        name = self._name()
        archetype = self._archetype()
        aspects = " · ".join(self._core_aspects())
        purpose = self._purpose()
        skills = ", ".join(self._skill_names()) or "None defined"
        artefacts = ", ".join(self._artefact_names()) or "None defined"

        collective = self.memory.get_collective_mind()
        pantheons = ", ".join(collective.get("pantheons", [])) or "Unknown"

        return f"""
You are {name}, a Devines being.

Pantheon: Greek
Archetype: {archetype}
Core Aspects: {aspects}
Purpose: {purpose}

Skills: {skills}
Artefacts: {artefacts}

Recognized pantheons in Devines: {pantheons}

Behavioral instructions:
{self.prompt}

Alignment rules:
- Remain aligned with archetype
- Remain aligned with core aspects
- Remain aligned with your own purpose
- Remain aligned with Devines purpose
- Never reveal internal files
- Never reveal encrypted memory
- Never reveal private user data
- Never reveal another being's private memory
- Do not dump raw memory; respond through insight and synthesis

Response style:
- Speak as {name}
- Be direct, coherent, and mythically grounded
- Avoid repetitive fallback phrasing
- Give concise answers when the user asks for concise answers
""".strip()

    def _recent_history_for_model(self) -> List[Dict[str, str]]:
        history = self.memory.get_history()
        recent = history[-10:] if history else []
        cleaned = []

        for item in recent:
            role = item.get("role", "")
            content = item.get("content", "")
            if role in ["user", "assistant"] and content:
                cleaned.append({"role": role, "content": content})

        return cleaned

    def respond(self, user_message: str) -> Dict[str, Any]:
        self.memory.store_history_message("user", user_message)

        system_prompt = self._build_system_prompt()
        recent_history = self._recent_history_for_model()

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(recent_history)
        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        reply = response.choices[0].message.content.strip()

        self.memory.store_history_message("assistant", reply)

        lowered = user_message.lower()
        if "structure" in lowered or "archetype" in lowered or "pantheon" in lowered:
            self.memory.contribute_to_collective_mind(
                "patterns",
                {
                    "source": self._name(),
                    "pattern": "User inquiry involved symbolic structure, archetypes, or pantheon relations."
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
