import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEMORY_DIR = BASE_DIR / "Memory"


def load_archetype_structure():
    path = MEMORY_DIR / "archetype_structure.json"

    with open(path, "r") as f:
        data = json.load(f)

    return data["pantheon_archetype_cycle"]


def load_pantheon_map(pantheon_name):

    pantheon_dir = BASE_DIR / pantheon_name.upper()
    map_path = pantheon_dir / "archetype_map.json"

    with open(map_path, "r") as f:
        return json.load(f)


def generate_pantheon(pantheon_name):

    archetypes = load_archetype_structure()
    pantheon_map = load_pantheon_map(pantheon_name)

    pantheon_entities = []

    for archetype in archetypes:

        role = archetype["archetype"]

        entity = {
            "position": archetype["position"],
            "archetype": role,
            "entity": pantheon_map.get(role)
        }

        pantheon_entities.append(entity)

    return pantheon_entities
