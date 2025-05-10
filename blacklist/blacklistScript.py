from jsonreader import load_cfg, save_cfg
import re
blacklist_name = "blacklist/blacklist.json"
# it opens from jsonreader.py script so take care
def check_blacklist(msg_content: str):
    jsonfile = load_cfg(blacklist_name)
    msg_content = re.sub("[3еẹėéè]", "e", msg_content)
    msg_content = re.sub("[6ġ]", "g", msg_content)
    msg_content = re.sub("[1!іíï]", "i", msg_content)
    msg_content = re.sub("[4@аạąäàá]", "a", msg_content)
    for blacklisted_word in jsonfile["sensitive"]:
        if blacklisted_word in re.sub("[!@#$%^&*(),./<>?]","", msg_content).replace(" ", ""):
            return blacklisted_word
    for non_sensitive_word in jsonfile["insensitive"]:
        if (non_sensitive_word == msg_content) or (non_sensitive_word + " " in msg_content) or (" " + non_sensitive_word in msg_content):
            return non_sensitive_word
    return None

def add_blacklisted_word(word, case):
    data = load_cfg(blacklist_name)
    if case == "s":
        for blacklisted_word in data["sensitive"]: #checking if in database
            if word == blacklisted_word:
                return False
        data["sensitive"].append(word)
    elif case == "i":
        for blacklisted_word in data["insensitive"]:
            if word == blacklisted_word:
                return False
        data["insensitive"].append(word)
    save_cfg(blacklist_name, data)
    return True

def remove_blacklisted_word(word, case):
    data = load_cfg(blacklist_name)
    if case == "s":
        for blacklisted_word in data["sensitive"]:
            if blacklisted_word == word:
                data["sensitive"].remove(word)
                save_cfg(blacklist_name, data)
                return True
    if case == "i":
        for blacklisted_word in data["insensitive"]:
            if blacklisted_word == word:
                data["insensitive"].remove(word)
                save_cfg(blacklist_name, data)
                return True
    return False

def get_blacklisted_words():
    data = load_cfg(blacklist_name)
    return data

def get_blacklisted_links():
    data = load_cfg(blacklist_name)
    return data

def add_blacklisted_link(link):
    data = load_cfg(blacklist_name)
    for l in data["links"]:
        if link["name"] == l["name"]:
            return False
    data["links"].append(link)
    save_cfg(blacklist_name, data)
    return True

def remove_blacklisted_link(link_name):
    data = load_cfg(blacklist_name)
    for l in data["links"]:
        if link_name == l["name"]:
            data["links"].remove(l)
            save_cfg(blacklist_name, data)
            return True
    return False

def check_scam_links(message):
    data = load_cfg(blacklist_name)
    for l in data["links"]:
        threshold = l["threshold"]
        found = 0 # keywords found in message with link
        for keyword in l["keywords"]:
            if keyword in message:
                found+=1
                if found>=threshold:
                    return l["name"]
    return None