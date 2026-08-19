# config_helpers/linkfixer.py
from config_helpers.general import load_file, save_file

linkfixer_file = "link_fixers.json"

def load_linkfixers() -> dict:
    data = load_file(linkfixer_file)
    return data if data else {"fixers": []}

def save_linkfixers(data: dict) -> None:
    save_file(linkfixer_file, data)

def add_fixer(name: str, links: list[str]) -> tuple[bool, str]:
    data = load_linkfixers()
    for fixer in data["fixers"]:
        if fixer["name"] == name:
            existing_set = set(fixer["link"])
            new_links = [l for l in links if l not in existing_set]
            if not new_links:
                return False, f"Fixer '{name}' already has all these links"
            fixer["link"].extend(new_links)
            save_linkfixers(data)
            return True, f"Updated fixer '{name}': added {', '.join(new_links)}"
    all_links = {l: f["name"] for f in data["fixers"] for l in f["link"]}
    conflicts = [f"'{l}' (in '{all_links[l]}')" for l in links if l in all_links]
    if conflicts:
        return False, f"Link conflicts: {', '.join(conflicts)}"
    data["fixers"].append({"name": name, "link": links, "index": 0})
    save_linkfixers(data)
    return True, f"Added fixer '{name}' with links: {', '.join(links)}"

def remove_fixer(name: str) -> bool:
    data = load_linkfixers()
    before = len(data["fixers"])
    data["fixers"] = [f for f in data["fixers"] if f["name"] != name]
    if len(data["fixers"]) < before:
        for fixer in data["fixers"]:
            fixer["index"] = 0
        save_linkfixers(data)
        return True
    return False

def increment_index(name: str) -> int:
    data = load_linkfixers()
    for fixer in data["fixers"]:
        if fixer["name"] == name:
            count = len(fixer["link"])
            if count > 1:
                fixer["index"] = (fixer["index"] + 1) % count
                save_linkfixers(data)
            return fixer["index"]
    return 0


def check_and_replace_links(message: str, fixers_data: dict) -> tuple[str, bool, bool]:
    result = message
    modified = False
    can_swap = False

    for fixer in fixers_data.get("fixers", []):
        if not fixer["link"]:
            continue
        if len(fixer["link"]) > 1:
            can_swap = True

        raw_domain = fixer["link"][fixer["index"]]
        new_full_link = f"https://www.{raw_domain}.com"

        patterns = [
            f"https://www.{fixer['name']}.com",
            f"http://www.{fixer['name']}.com",
            f"https://{fixer['name']}.com",
            f"http://{fixer['name']}.com",
            f"www.{fixer['name']}.com",
        ]

        for pattern in patterns:
            if pattern in result:
                result = result.replace(pattern, new_full_link, 1)
                modified = True
                break

    return result, modified, can_swap