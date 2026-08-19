# config_helpers/warns.py
from config_helpers import read_config_key
from config_helpers.general import load_file, save_file

warns_name = "warns.json"

def create_user_data(userid: int, description: str = "") -> dict:
    return {"user_id": userid, "warns": []}

def remove_user_warn_data(userid: int) -> bool:
    data = load_file(warns_name)
    for i, user in enumerate(data.get("users", [])):
        if user["user_id"] == userid:
            data["users"].pop(i)
            save_file(warns_name, data)
            return True
    return False

def add_warn(userid: int, description: str):
    data = load_file(warns_name)
    for user in data.get("users", []):
        if user["user_id"] == userid:
            user["warns"].append(description)
            save_file(warns_name, data)
            return
    data.setdefault("users", []).append({
        "user_id": userid,
        "warns": [description]
    })
    save_file(warns_name, data)

def get_warns(userid: int) -> list:
    data = load_file(warns_name)
    for user in data.get("users", []):
        if user["user_id"] == userid:
            return user.get("warns", [])
    return []

def clean_non_existent_users(bot) -> None:
    server_id = read_config_key("server_id")
    if not server_id or server_id == 0:
        return  # No server configured yet

    warn_data = load_file(warns_name)
    cleaned = False
    for warn_user in warn_data.get("users", []):
        if bot.get_user(warn_user["user_id"]):
            continue
        # User exists in warn data but not in Discord
        remove_user_warn_data(warn_user["user_id"])
        cleaned = True
    if cleaned:
        print("Cleared non-existent users from warn data.")
