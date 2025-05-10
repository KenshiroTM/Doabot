import json

cfg_name = "config.json"

def load_cfg(name):
    with open(name, encoding='utf-8') as jsonFile:  # opens json
        data = json.load(jsonFile)
        return data

def save_cfg(name, content):
    with open(name, 'w') as jsonFile:
        json.dump(content, jsonFile)

def add_to_last_bans(username, userid):
    banned_user = {"name": username, "userid": int(userid)}
    data = load_cfg(cfg_name)
    if len(data["last_bans"]) >= 3: #if more than 3 then pop first element and add last element
        data["last_bans"].pop(0)
    for user in data["last_bans"]: #checks if user is already in
        if user["userid"] == int(userid):
            print("already in last bans!")
            return 1
    data["last_bans"].append(banned_user)
    save_cfg(cfg_name, data)


def remove_from_last_bans(userid):
    data = load_cfg(cfg_name)
    for user in data["last_bans"]:
        if user["userid"] == int(userid):
            data["last_bans"].remove(user)
            save_cfg(cfg_name, data)
            return 0