from typing import Optional

from config_helpers.general import load_file, save_file

last_bans_name = "last_bans.json"

def add_to_last_bans(username: str, userid: int):
    data = load_file(last_bans_name)
    banned_user = {"name": username, "userid": int(userid)}
    # Keep only last 3 bans
    if len(data.get("last_bans", [])) >= 3:
        data["last_bans"] = data["last_bans"][-2:]
    # Check if already exists
    for user in data.get("last_bans", []):
        if user["userid"] == int(userid):
            return 1  # Already in list
    data.setdefault("last_bans", []).append(banned_user)
    save_file(last_bans_name, data)
    return 0


def remove_from_last_bans(userid: int) -> bool:
    data = load_file(last_bans_name)
    original_length = len(data.get("last_bans", []))
    data["last_bans"] = [u for u in data.get("last_bans", []) if u["userid"] != int(userid)]
    if len(data["last_bans"]) < original_length:
        save_file(last_bans_name, data)
        return True
    return False


def get_ban_by_position(position: int) -> Optional[dict]:
    """Non-destructive lookup: returns the ban record at `position`
    (1 = most recent), or None if there aren't that many bans on record.

    Doesn't remove anything - use this to peek at a ban BEFORE acting on
    it (e.g. before attempting to unban), so a failed action doesn't leave
    last_bans out of sync with what's actually banned on Discord.
    """
    last_bans = load_file(last_bans_name).get("last_bans", [])
    index = len(last_bans) - position
    if index < 0:
        return None
    return last_bans[index]


def remove_ban(position: int) -> Optional[dict]:
    record = get_ban_by_position(position)
    if record is None:
        return None
    remove_from_last_bans(record["userid"])
    return record

def get_last_bans():
    return load_file(last_bans_name).get("last_bans", [])