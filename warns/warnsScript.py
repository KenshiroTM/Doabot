from jsonreader import load_cfg, save_cfg
warns_name = "warns/warns.json"
def create_user(userid, data):
    new_user = {
        "user_id": userid,
        "warns": []
    }
    data["users"].append(new_user)
    return data

def remove_user(userid):
    data = load_cfg(warns_name)

    for user in data["users"]:
        if user["user_id"] == userid:
            data["users"].remove(user)
            save_cfg(warns_name, data)
    return None

def add_warn(userid, description):
    data = load_cfg(warns_name)

    for user in data["users"]:
        if user["user_id"]==userid:
            user["warns"].append(description)
            save_cfg(warns_name, data)
            return

    data = create_user(userid, data)
    save_cfg(warns_name, data)
    add_warn(userid, description)

def get_warns(userid):
    data = load_cfg(warns_name)

    for user in data["users"]:
        if user["user_id"] == userid:
            return user["warns"]
    return None