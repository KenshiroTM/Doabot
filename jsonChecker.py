import os
import json

json_files = [
    'blacklist/blacklist.json',
    'warns/warns.json',
    'config.json',
]

default_data = [
    {"sensitive": [], "insensitive": [], "links": []},
    {"users": []},
    {"Version": "1.0.0", "server_id": 713475017957965945, "delete_msg_days": 7, "mute_amount": 2, "prefix": "^", "blacklist_on": False, "linkfixer_on":False, "antispam_on":False, "spammer_timeout": 4, "last_bans": [], "expose_delete_hours": 1, "instagram_fixer_idx":0}
]

def mass_check_variables():
    for i in range(len(json_files)):
        path = json_files[i] # current path
        defaults = default_data[i] # default variables

        if not os.path.exists(path):
            continue  # skip if file doesn't exist

        with open(path, 'r') as file:
            try:
                data = json.load(file) # loaded json file
                for key, value in defaults.items(): # checks if key exists
                    if key not in data: # if it doesn't then add to it
                        data[key] = value
                        print(f"Added missing key '{key}' to {path}")
            except json.JSONDecodeError:
                print(f"Invalid JSON in {path}, skipping.")
                continue

        with open(path, 'w') as file:
            json.dump(data, file)
            print(f"Updated: {path}")

def mass_check_json():
    for i in range(len(json_files)):
        if not os.path.exists(json_files[i]):
            print(f"path to {json_files[i]}")
            with open(json_files[i], 'w') as file:
                json.dump(default_data[i] or {}, file)
        else:
            print(f"file {json_files[i]} already exists.")
    mass_check_variables()