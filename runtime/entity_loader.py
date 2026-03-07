import json
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_entity(pantheon, entity_name):

    pantheon_dir = BASE_DIR / pantheon.upper()
    entity_dir = pantheon_dir / entity_name.upper()

    entity = {
        "name": entity_name,
        "pantheon": pantheon
    }

    # identity
    identity_file = entity_dir / "identity.json"
    if identity_file.exists():
        with open(identity_file) as f:
            entity["identity"] = json.load(f)

    # config (yaml)
    config_file = entity_dir / "config.yaml"
    if config_file.exists():
        with open(config_file) as f:
            entity["config"] = yaml.safe_load(f)

    # relationships
    rel_file = entity_dir / "relationships.json"
    if rel_file.exists():
        with open(rel_file) as f:
            entity["relationships"] = json.load(f)

    return entity
