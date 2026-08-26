from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

class ConfigNode:
    """
    Allows dictionary data to be accessed using dot notation.

    Example:
        cfg.A.B.C
        cfg.B.Q
    """

    def __init__(self, data: dict[str, Any]):
        self._data = data

        for key, value in data.items():
            setattr(self, key, self._convert(value))

    def _convert(self, value):
        if isinstance(value, dict):
            return ConfigNode(value)

        if isinstance(value, list):
            return [
                self._convert(item)
                for item in value
            ]

        return value

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __repr__(self):
        return repr(self._data)

def parse_env_value(value: str) -> Any:
    """
    Try to convert ENV strings into Python values.

    Examples:
        "123"          -> 123
        "1.5"          -> 1.5
        "true"         -> True
        "[1,2,3]"      -> [1, 2, 3]
        '"hello"'      -> "hello"
        "hello"        -> "hello"
    """

    if value is None:
        return None

    value = value.strip()

    # JSON-compatible values
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass

    # Regular string
    return value

def load_env(path: str | Path) -> dict[str, Any]:
    """
    Load .env and convert dotted keys into nested dictionaries.
    """

    raw = dotenv_values(path)

    result = {}

    for key, value in raw.items():

        if value is None:
            continue

        parts = key.split(".")
        current = result

        for part in parts[:-1]:
            current = current.setdefault(part, {})

        current[parts[-1]] = parse_env_value(value)

    return result

def load_json(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def deep_merge(
    base: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """
    Recursively merge dictionaries.

    Existing dictionaries are merged instead of replaced.

    Example:

        base:
        {
            "A": {
                "B": {
                    "C": 1
                }
            }
        }

        new:
        {
            "A": {
                "B": {
                    "D": 2
                }
            }
        }

        result:
        {
            "A": {
                "B": {
                    "C": 1,
                    "D": 2
                }
            }
        }
    """

    result = dict(base)

    for key, value in new.items():

        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)

        else:
            result[key] = value

    return result

def load_config(
    env_path: str | Path | None = None,
    json_path: str | Path | None = None,
    # TODO: add TOML, XML, YAML, ini, ...
) -> ConfigNode:

    config = {}

    if env_path:
        config = deep_merge(
            config,
            load_env(env_path)
        )

    if json_path:
        config = deep_merge(
            config,
            load_json(json_path)
        )

    return ConfigNode(config)