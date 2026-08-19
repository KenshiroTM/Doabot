# jsonchecker.py
import os
import json

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All JSON files the bot uses
json_files = [
    {"file": "config.json", "defaults": {
        "Version": "2.0.0",
        "server_id": 0,
        "delete_msg_days": 7,
        "timeout_amount": 6,
        "prefix": "^",
        "blacklist_on": False,
        "linkfixer_on": False,
        "antispam_on": False,
        "spammer_timeout": 4,
        "expose_delete_hours": 1,
    }},
    {"file": "blacklist.json", "defaults": {
        "sensitive": [],
        "insensitive": [],
        "links": []
    }},
    {"file": "last_bans.json", "defaults": {
        "last_bans": []
    }},
    {"file": "warns.json", "defaults": {
        "users": []
    }},
    {"file": "link_fixers.json", "defaults": {
        "fixers": []
    }},
    {
        "file": "fixer_links.json", "defaults": {
        "links": []
    }}
]


def ensure_json_exists():
    """Ensure all JSON files exist with default values."""
    for entry in json_files:
        filepath = os.path.join(CONFIG_DIR, entry["file"])
        if not os.path.exists(filepath):
            print(f"Creating {entry['file']} with defaults...")
            with open(filepath, "w") as f:
                json.dump(entry["defaults"], f, indent=4)


def fix_missing_keys():
    """Add any missing keys to existing JSON files."""
    for entry in json_files:
        filepath = os.path.join(CONFIG_DIR, entry["file"])
        if not os.path.exists(filepath):
            continue

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            for key, default_value in entry["defaults"].items():
                if key not in data:
                    data[key] = default_value
                    print(f"Added missing key '{key}' to {entry['file']}")

            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Updated: {entry['file']}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in {entry['file']}, skipping.")


def mass_check_json():
    """Run full validation: create missing files + fix keys."""
    print("Running JSON validation...")
    ensure_json_exists()
    fix_missing_keys()
    print("JSON validation complete!")
