import os
import json
from cryptography.fernet import Fernet


class MemoryManager:

    def __init__(self, entity_path):

        self.entity_path = entity_path
        self.memory_path = os.path.join(entity_path, "memory")

        if not os.path.exists(self.memory_path):
            os.makedirs(self.memory_path)

        self.key_path = os.path.join(self.memory_path, "memory.key")

        self.identity_file = os.path.join(self.memory_path, "identity.enc")
        self.knowledge_file = os.path.join(self.memory_path, "knowledge.enc")
        self.reflections_file = os.path.join(self.memory_path, "reflections.enc")
        self.chat_file = os.path.join(self.memory_path, "chat.enc")

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

        serialized = json.dumps(data).encode()

        encrypted = self.fernet.encrypt(serialized)

        with open(filepath, "wb") as f:
            f.write(encrypted)

    def _load_and_decrypt(self, filepath):

        if not os.path.exists(filepath):
            return []

        with open(filepath, "rb") as f:
            encrypted = f.read()

        try:
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception:
            return []

    # --------------------------
    # REFLECTION STORAGE
    # --------------------------

    def store_reflection(self, reflection):

        reflections = self._load_and_decrypt(self.reflections_file)

        reflections.append({
            "type": "reflection",
            "content": reflection
        })

        self._encrypt_and_store(self.reflections_file, reflections)

    def get_reflections(self):

        return self._load_and_decrypt(self.reflections_file)

    # --------------------------
    # CHAT MEMORY
    # --------------------------

    def store_chat(self, role, message):

        chat = self._load_and_decrypt(self.chat_file)

        chat.append({
            "role": role,
            "content": message
        })

        self._encrypt_and_store(self.chat_file, chat)

    def get_chat_history(self):

        return self._load_and_decrypt(self.chat_file)

    # --------------------------
    # KNOWLEDGE STORAGE
    # --------------------------

    def store_knowledge(self, data):

        knowledge = self._load_and_decrypt(self.knowledge_file)

        knowledge.append(data)

        self._encrypt_and_store(self.knowledge_file, knowledge)

    def get_knowledge(self):

        return self._load_and_decrypt(self.knowledge_file)
