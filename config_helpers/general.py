# config_helpers/general.py
import json
import os

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_file(filename: str) -> dict:
    """Load ANY JSON file from project root."""
    filepath = os.path.join(CONFIG_DIR, filename)
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_file(filename: str, data: dict) -> None:
    """Save ANY dictionary to a JSON file in project root."""
    filepath = os.path.join(CONFIG_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# ==================== General Config (config.json) ====================

cfg_name = "config.json"

def read_config_key(key: str, default=None):
    return load_file(cfg_name).get(key, default)

def write_config_key(key: str, value):
    data = load_file(cfg_name)
    data[key] = value
    save_file(cfg_name, data)
    return value

def toggle_config_key(key: str, default=False):
    current = read_config_key(key, default)
    return write_config_key(key, not current)

def validate_and_write_numeric(key: str, value: int, min_val: int, max_val: int) -> bool:
    if not (min_val <= value <= max_val):
        return False
    return write_config_key(key, value)