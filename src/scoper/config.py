"""Scoper Configuration Module."""

from pathlib import Path
import json
from typing import Any

DEFAULT_CONFIG = {
    "author": "ZeroDevLLC",
    "default_format": "md",
    "default_template": "standard",
    "output_dir": ".",
    "variables": {
        "company": "ZeroDevLLC",
        "version": "1.0"
    },
    "compliance_forms": [
        {"file": "COMPLIANCE_SCOPE_TEMPLATE.md", "kicker": "PART V: REGULATORY EXECUTION"},
        {"file": "SCOPE_STATEMENT_TEMPLATE.md", "kicker": "PART VI: SCOPE DEFINITION"},
        {"file": "ASSET_INVENTORY_TEMPLATE.md", "kicker": "PART VII: ASSET INVENTORY"},
        {"file": "RULES_OF_ENGAGEMENT_TEMPLATE.md", "kicker": "PART VIII: RULES OF ENGAGEMENT"},
        {"file": "FINDING_TRACKER_TEMPLATE.md", "kicker": "PART IX: REMEDIATION TRACKER"}
    ]
}


def get_config_path() -> Path:
    """Get config file path."""
    return Path.home() / ".config" / "scoper" / "config.json"


def load_config() -> dict:
    """Load configuration from file."""
    config_path = get_config_path()

    if config_path.exists():
        with open(config_path) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}

    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Save configuration to file."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific config value."""
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """Set a specific config value."""
    config = load_config()
    config[key] = value
    save_config(config)


def init_config() -> None:
    """Initialize default config."""
    config_path = get_config_path()
    if not config_path.exists():
        save_config(DEFAULT_CONFIG)
        print(f"Created config at: {config_path}")
    else:
        print(f"Config already exists at: {config_path}")


if __name__ == "__main__":
    init_config()
