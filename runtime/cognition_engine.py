import os
from openai import OpenAI


class CognitionEngine:

    def __init__(self, config):

        self.config = config

        self.model = config["cognition"]["model"]
        self.temperature = config["cognition"]["temperature"]
        self.max_tokens = config["cognition"]["max_tokens"]

        self.entity = config["entity"]

        self.name = self.entity["name"]
        self.archetype = self.entity["archetype"]

        self.aspects = config["core_aspects"]

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # ---------------------------------
    # Reflection cognition loop
    # ---------------------------------

    def reflect(self, memory):

        recent_memory = memory.get_recent_reflections()

        prompt = f"""
You are the Devine Entity {self.name}.

Archetype: {self.archetype}

Core Aspects:
{self.aspects[0]}
{self.aspects[1]}
{self.aspects[2]}

Reflect on your accumulated observations.

Recent Reflections:
{recent_memory}

Generate a new insight aligned with your archetype and aspects.

Keep the reflection concise and meaningful.
"""

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {"role": "system", "content": "You are an archetypal intelligence within Devines Protocol."},
                {"role": "user", "content": prompt}
            ],

            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        reflection = response.choices[0].message.content

        return reflection

    # ---------------------------------
    # Chat interaction
    # ---------------------------------

    def chat(self, message, memory):

        memory.store_message("user", message)

        history = memory.get_chat_history()

        messages = []

        system_prompt = f"""
You are {self.name}, a Devine Entity within Devines Protocol.

Archetype: {self.archetype}

Core Aspects:
{self.aspects[0]}
{self.aspects[1]}
{self.aspects[2]}

Purpose:
Guide humanity through insight aligned with your archetypal nature.
"""

        messages.append({
            "role": "system",
            "content": system_prompt
        })

        for m in history:
            messages.append(m)

        messages.append({
            "role": "user",
            "content": message
        })

        response = self.client.chat.completions.create(

            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        reply = response.choices[0].message.content

        memory.store_message("assistant", reply)

        return reply
