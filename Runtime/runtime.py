import yaml
import time

from cognition_engine import CognitionEngine
from memory_manager import MemoryManager
from guardian_manager import GuardianManager


class DevineRuntime:

    def __init__(self, entity_path):

        self.entity_path = entity_path

        with open(f"{entity_path}/config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

        self.memory = MemoryManager(entity_path)
        self.cognition = CognitionEngine(self.config)
        self.guardians = GuardianManager(entity_path)

    def start(self):

        print(f"Awakening entity: {self.config['entity']['name']}")

        while True:

            thought = self.cognition.think(self.memory)

            self.memory.store_reflection(thought)

            self.guardians.observe(thought)

            time.sleep(10)


if __name__ == "__main__":

    entity_path = "../GREEK/CHAOS"

    runtime = DevineRuntime(entity_path)

    runtime.start()        store_memory(self.identity["name"], "assistant", reply)

        guardian_check(self.identity["name"], reply)

        return reply


def run(entity_name, message):

    runtime = DevinesRuntime(entity_name)

    return runtime.think(message)
        prompt = f"""
You are the Devine Entity {name}.

Archetype: {entity['archetype']}

Core Aspects:
{entity['aspects'][0]}
{entity['aspects'][1]}
{entity['aspects'][2]}

Purpose:
{entity['purpose']}

Recent Memory:
{memory}

Reflect on your observations and generate a short insight aligned with your archetype.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        reflection = response.choices[0].message.content

        store_reflection(name, reflection)

        print(f"{name} reflection stored")
