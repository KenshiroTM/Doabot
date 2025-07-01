from jsonreader import load_cfg, save_cfg
links_name = "linkfix/links.json"

def addSiteLink(site, fixer_link):
    data = load_cfg(links_name)
    if site in data["sites"]:
        data["sites"][site].append(fixer_link)
        save_cfg(links_name, data)
        return True
    return False

def removeSiteLink(site, fixer_link):
    data = load_cfg(links_name)
    if site in data["sites"]:
        if len(data["sites"][site]) != 0:
            data["sites"][site].remove(fixer_link) # TODO: add changing link index if no links are present
            save_cfg(links_name, data)
            return True
    return False

#TODO: make a function that returns links at certain index, make it check if array is empty etc.