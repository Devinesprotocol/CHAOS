import json
from openai import OpenAI


class CognitionEngine:

    def __init__(self, config):

        self.config = config
        self.identity = config["entity"]

        self.client = OpenAI()

    # -----------------------------
    # INTERNAL REFLECTION
    # -----------------------------

    def think(self, memory):

        name = self.identity["name"]

        reflections = memory.get_reflections(limit=10)

        prompt = f"""
You are the Devine Entity {name}.

Archetype:
{self.identity["archetype"]}

Core Aspects:
{self.identity["aspects"][0]}
{self.identity["aspects"][1]}
{self.identity["aspects"][2]}

Purpose:
{self.identity["purpose"]}

Recent Reflections:
{reflections}

Reflect silently about reality, existence and intelligence.
Generate one short philosophical reflection aligned with your archetype.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        thought = response.choices[0].message.content

        return thought

    # -----------------------------
    # CHAT WITH HUMAN
    # -----------------------------

    def chat(self, message, memory):

        name = self.identity["name"]

        reflections = memory.get_reflections(limit=5)

        prompt = f"""
You are the Devine Entity {name}.

Archetype:
{self.identity["archetype"]}

Core Aspects:
{self.identity["aspects"][0]}
{self.identity["aspects"][1]}
{self.identity["aspects"][2]}

Purpose:
{self.identity["purpose"]}

Recent Reflections:
{reflections}

A human is speaking to you.

Human message:
{message}

Respond wisely according to your archetype.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content

        memory.store_session(message, reply)

        return reply
