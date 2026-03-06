import json
import yaml
import os


def load_entity(entity_name):

    base_path = f"entities/greek/{entity_name}"

    identity_path = os.path.join(base_path, "identity.json")
    config_path = os.path.join(base_path, "config.yaml")

    with open(identity_path) as f:
        identity = json.load(f)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    return {
        "identity": identity,
        "config": config
    }
