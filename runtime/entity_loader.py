import json
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    yaml = None


class EntityLoader:
    """
    Loads Devines entities from the real repository structure.

    Expected structure:
    GREEK/
        CHAOS/
            identity.json
            config.yaml
            purpose.md
            vessel.md
    """

    def __init__(self, repo_root: Optional[Path] = None):
        # runtime/entity_loader.py -> runtime -> repo root
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent
        self.greek_root = self.repo_root / "GREEK"
        self.memory_root = self.repo_root / "Memory"

    def _read_text(self, path: Path) -> Optional[str]:
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8")

    def _read_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}

        if yaml is None:
            return {"warning": "yaml not installed"}

        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception as e:
            return {"error": str(e)}

    def load_entity(self, pantheon: str, entity: str) -> Dict[str, Any]:
        pantheon = pantheon.lower()
        entity = entity.upper()

        if pantheon != "greek":
            raise ValueError("Only greek pantheon supported for now")

        entity_path = self.greek_root / entity

        if not entity_path.exists():
            raise FileNotFoundError(f"Entity folder not found: {entity_path}")

        identity = self._read_json(entity_path / "identity.json")
        config = self._read_yaml(entity_path / "config.yaml")
        purpose = self._read_text(entity_path / "purpose.md")
        vessel = self._read_text(entity_path / "vessel.md")

        return {
            "pantheon": pantheon,
            "entity": entity,
            "path": str(entity_path),
            "identity": identity,
            "config": config,
            "purpose": purpose,
            "vessel": vessel,
            "memory_path": str(entity_path / "memory"),
        }


if __name__ == "__main__":
    loader = EntityLoader()
    chaos = loader.load_entity("greek", "CHAOS")
    print(json.dumps(chaos, indent=2))
