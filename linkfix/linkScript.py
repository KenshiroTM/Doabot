from jsonreader import load_cfg, save_cfg
links_name = "linkfix/links.json"

def addSiteLink(site, fixer_link):
    data = load_cfg(links_name)
    if site in data["sites"]:
        data["sites"][site].append(fixer_link)
    save_cfg(links_name, data)

def removeSiteLink(site, fixer_link):
    data = load_cfg(links_name)
    if site in data["sites"]:
        data["sites"][site].remove(fixer_link)
    save_cfg(links_name, data)

removeSiteLink("instagram", "ddinstagram")