"""Load the toolkit's closed configuration schema and merge project overrides."""
import json
from pathlib import Path

RESOURCES = Path(__file__).resolve().parent
CONFIG_NAME = ".php-engineering-toolkit.json"


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    data = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain an object")
    return data


def merge(base, overrides, schema, prefix=""):
    result = dict(base)
    for key, value in overrides.items():
        name = prefix + key
        rule = schema["properties"].get(key)
        if rule is None:
            raise ValueError(f"Unknown setting: {name}")
        if rule["type"] == "object":
            if not isinstance(value, dict):
                raise ValueError(f"{name} must be an object")
            value = merge(base.get(key, {}), value, rule, name + ".")
        elif rule["type"] == "boolean" and type(value) is not bool:
            raise ValueError(f"{name} must be a boolean")
        elif rule["type"] == "integer" and (
            type(value) is not int or not rule["minimum"] <= value <= rule["maximum"]
        ):
            raise ValueError(f"{name} must be an integer from {rule['minimum']} to {rule['maximum']}")
        elif "enum" in rule and value not in rule["enum"]:
            raise ValueError(f"{name} must be one of {rule['enum']}")
        result[key] = value
    return result


def load_config(root):
    schema = read_json(RESOURCES / "schema.json")
    defaults = merge({}, read_json(RESOURCES / "default.json"), schema)
    path = root / CONFIG_NAME
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Project configuration must be local to the project")
    return merge(defaults, read_json(path), schema) if path.exists() else defaults
