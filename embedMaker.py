from datetime import datetime, timezone
import discord

badColor = discord.Color.red()

def get_normalized_time():
    return datetime.now(timezone.utc).strftime("%d %B %Y at %H:%M:%S")

def create_embed_base(title, color, description=None):
    embed = discord.Embed(
        title = title,
        color = color,
    )
    if description:
        embed.description = description
    return embed

def create_warns_embed(user, user_warns):
    embed = create_embed_base(f"Warns of {user.name}", badColor)

    if user_warns is None:
        embed.description = "No warns found!"
        return
    else:
        i=0
        for warn in user_warns:
            i+=1
            embed.add_field(name=f"No.{i}", value=warn)

    embed.set_author(icon_url=user.avatar.url, name=user.name)
    embed.add_field(name=f"User ID: {user.id}", value="", inline=False)
    return embed

def create_blacklist_word_show_embed(data):
    embed = create_embed_base("Blacklisted words", badColor)
    sensitive = "Case sensitive:"
    insensitive = "Case insensitive:"
    s_words = ""
    i_words = ""

    for word in data["sensitive"]:
        s_words += f" {word}"
    for word in data["insensitive"]:
        i_words += f" {word}"

    if not data["sensitive"]:
        sensitive = "No sensitive words added"
    if not data["insensitive"]:
        insensitive = "No insensitive words added"

    embed.add_field(name=sensitive, value=s_words, inline=False)
    embed.add_field(name=insensitive, value=i_words, inline=False)

    return embed
def create_scam_links_show_embed(data):
    embed = create_embed_base("Scam link blacklist", badColor)
    if data["links"]:
        for l in data["links"]:
            link_name = f"{l["name"]}"
            link_value = f"Word threshold: {str(l["threshold"])}\nKeywords:"
            for word in l["keywords"]:
                link_value += f" {word}"
            embed.add_field(name=link_name, value=link_value, inline=False)
    else:
        embed.description="No links added!"
    return embed

def create_expose_embed(user, content, delete_hours, date):
    embed = create_embed_base(f"🗑️ Deleted Message", badColor)
    embed.set_author(icon_url=user.avatar.url, name=user.name)
    embed.add_field(name="Content:", value=content, inline=False)
    embed.set_footer(text=f"Deleted at {date} • Removed from cache after {int(delete_hours)} hour(s)")
    return embed