import os
import json
from cryptography.fernet import Fernet


class MemoryManager:
    """
    Privacy-safe encrypted memory manager for a single entity.

    Rules:
    - Only accesses the current entity_path memory folder
    - Does not read other entities' memory
    - Stores chat history in history.enc
    - Keeps reflections and knowledge in separate encrypted files
    """

    def __init__(self, entity_path, shared_memory_path=None):
        self.entity_path = entity_path
        self.memory_path = os.path.join(entity_path, "memory")

        if not os.path.exists(self.memory_path):
            os.makedirs(self.memory_path)

        # Entity-private encrypted files
        self.key_path = os.path.join(self.memory_path, "memory.key")
        self.history_file = os.path.join(self.memory_path, "history.enc")
        self.identity_file = os.path.join(self.memory_path, "identity.enc")
        self.knowledge_file = os.path.join(self.memory_path, "knowledge.enc")
        self.reflections_file = os.path.join(self.memory_path, "reflections.enc")

        # Shared Devines memory path is optional and not loaded automatically.
        # It exists only for future explicit scoped access.
        self.shared_memory_path = shared_memory_path

        self.fernet = self._load_or_create_key()

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)

        return Fernet(key)

    def _encrypt_and_store(self, filepath, data):
        serialized = json.dumps(data, ensure_ascii=False).encode("utf-8")
        encrypted = self.fernet.encrypt(serialized)

        with open(filepath, "wb") as f:
            f.write(encrypted)

    def _load_and_decrypt(self, filepath, default=None):
        if default is None:
            default = []

        if not os.path.exists(filepath):
            return default

        with open(filepath, "rb") as f:
            encrypted = f.read()

        if not encrypted:
            return default

        try:
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception:
            return default

    # --------------------------
    # ENTITY-PRIVATE HISTORY
    # --------------------------
    def store_history_message(self, role, message):
        history = self._load_and_decrypt(self.history_file, default=[])

        history.append({
            "role": role,
            "content": message
        })

        # Keep only a bounded amount for now
        history = history[-40:]
        self._encrypt_and_store(self.history_file, history)

    def get_history(self):
        return self._load_and_decrypt(self.history_file, default=[])

    # --------------------------
    # ENTITY-PRIVATE REFLECTIONS
    # --------------------------
    def store_reflection(self, reflection):
        reflections = self._load_and_decrypt(self.reflections_file, default=[])

        reflections.append({
            "type": "reflection",
            "content": reflection
        })

        self._encrypt_and_store(self.reflections_file, reflections)

    def get_reflections(self):
        return self._load_and_decrypt(self.reflections_file, default=[])

    # --------------------------
    # ENTITY-PRIVATE KNOWLEDGE
    # --------------------------
    def store_knowledge(self, data):
        knowledge = self._load_and_decrypt(self.knowledge_file, default=[])
        knowledge.append(data)
        self._encrypt_and_store(self.knowledge_file, knowledge)

    def get_knowledge(self):
        return self._load_and_decrypt(self.knowledge_file, default=[])

    # --------------------------
    # USER-SAFE VIEW
    # --------------------------
    def get_user_visible_history(self):
        """
        Returns only the conversation history.
        This is what users may view as their interaction history.
        It does NOT expose reflections, knowledge, keys, or internal files.
        """
        return self.get_history()
