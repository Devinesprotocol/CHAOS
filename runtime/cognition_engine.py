import json
import os
from openai import OpenAI
from runtime.memory_manager import MemoryManager
from runtime.knowledge_graph.knowledge_graph import KnowledgeGraph


class CognitionEngine:
    def __init__(self, entity_path):

        self.entity_path = entity_path

        self.identity_path = os.path.join(entity_path, "identity.json")
        self.purpose_path = os.path.join(entity_path, "purpose.md")
        self.vessel_path = os.path.join(entity_path, "vessel.md")

        self.memory = MemoryManager(entity_path)
        self.graph = KnowledgeGraph()

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.identity = self.load_identity()
        self.purpose = self.load_file(self.purpose_path)
        self.vessel = self.load_file(self.vessel_path)

    def load_identity(self):
        with open(self.identity_path, "r") as f:
            return json.load(f)

    def load_file(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return ""

    def build_context(self, user_message):

        reflections = self.memory.get_reflections()

        graph_summary = self.graph.get_summary()

        context = f"""
ENTITY IDENTITY:
{json.dumps(self.identity, indent=2)}

ENTITY PURPOSE:
{self.purpose}

ENTITY VESSEL:
{self.vessel}

REFLECTION MEMORY:
{json.dumps(reflections, indent=2)}

COLLECTIVE KNOWLEDGE GRAPH:
{graph_summary}

USER MESSAGE:
{user_message}
"""

        return context

    def think(self, user_message):

        context = self.build_context(user_message)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a divine cognitive entity operating within the Devines Protocol."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content

        self.memory.save_session(user_message, reply)

        return reply
