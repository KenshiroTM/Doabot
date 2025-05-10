from datetime import datetime, timezone
import discord

goodNeutralColor = discord.Color.green()
badColor = discord.Color.red()
levelingColor = discord.Color.gold()

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

def create_lvl_embed(username, user_stats, user_img, exp_per_msg):
    embed = create_embed_base(f"📊 **{username}'s Level Stats**", levelingColor)
    embed.set_thumbnail(url=user_img)

    embed.add_field(name="🏆 Current Level", value=f"**{str(user_stats["level"])}**", inline=False)
    embed.add_field(name="⚡ Experience Gained", value=f"**{str(user_stats["exp"])} XP**", inline=False)
    embed.add_field(name="⏭️ Next Level At", value=f"**{str(user_stats["exp_to_next"])} XP**", inline=False)

    embed.set_footer(text=f"💬 XP per Message: {str(exp_per_msg)} XP  •  🚀 keep chatting to level up!")

    return embed

def create_level_roles_embed(data):
    embed = create_embed_base("List of level roles", levelingColor)
    if data:
        for role in data:
            embed.add_field(name=f"Level {role["level_required"]}", value=f"<@&{role["role_id"]}>", inline=False)
    else:
        embed.description=f"no roles present!"
    return embed

def create_scam_link_embed(msg, link_name):
    date = get_normalized_time()
    embed = create_embed_base("Suspected scam link found, automatic ban carried out", badColor, msg.content)

    embed.add_field(name=f"Blacklisted link name", value=link_name, inline=False)

    embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
    embed.add_field(name=f"User ID: {msg.author.id}", value="", inline=False)
    embed.set_footer(text=f"Message ID: {msg.id}  •  {date}")

    return embed

def create_blacklisted_word_embed(msg, blacklisted_msg):
    date = get_normalized_time()
    embed = create_embed_base("Blacklisted word found, automatic ban carried out", badColor, msg.content)

    embed.add_field(name=f"Blacklisted word used:", value=blacklisted_msg, inline=False)

    embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
    embed.add_field(name=f"User ID: {msg.author.id}", value="", inline=False)
    embed.set_footer(text=f"Message ID: {msg.id}  •  {date}")
    return embed

def create_deletion_embed(msg):
    date = get_normalized_time()
    message = msg.content
    if msg.attachments:
        for attachment in msg.attachments:
            message += attachment.url

    embed = create_embed_base(f"Message Deleted in #{msg.channel.name}", badColor, msg.content)

    embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
    embed.add_field(name=f"User ID: {msg.author.id}", value="", inline=False)
    embed.set_footer(text=f"Message ID: {msg.id}  •  {date}")
    return embed

def create_bulk_deletion_embed(messages):
    date = get_normalized_time()

    i = 0
    msgs_shown = 0
    all_messages = ""
    for msg in messages:
        i+=1
        if len(all_messages + f"\n **{msg.author}:** {msg.content}")<=2000:
            all_messages += f"\n **{msg.author}:** {msg.content}"
            msgs_shown+=1

    embed = create_embed_base(f"{i} Messages deleted in #{messages[0].channel}", badColor, all_messages)

    embed.set_footer(text=f"Showing last {msgs_shown} messages  •  {date}")
    return embed

def create_join_embed(user):
    date = get_normalized_time()
    embed = create_embed_base("Member joined", color=goodNeutralColor, description=f"<@{user.id}>")

    embed.set_author(icon_url=user.avatar.url, name=user.name)
    embed.add_field(name=f"User ID: {user.id}", value="", inline=False)
    embed.set_footer(text=f"{date}")
    return embed

def create_ban_embed(user):
    date = get_normalized_time()
    embed = create_embed_base("Member banned", color=badColor, description=f"<@{user.id}>")

    embed.set_author(icon_url=user.avatar.url, name=user.name)
    embed.add_field(name=f"User ID: {user.id}", value="", inline=False)
    embed.set_footer(text=f"{date}")
    return embed

def create_unban_embed(user):
    date = get_normalized_time()
    embed = create_embed_base("Member unbanned", color=goodNeutralColor, description=f"<@{user.id}>")

    embed.add_field(name=f"User ID: {user.id}", value="", inline=False)
    embed.set_author(icon_url=user.avatar.url, name=user.name)
    embed.set_footer(text=date)
    return embed

def create_msg_edited_embed(before, after):
    date = get_normalized_time()
    embed = create_embed_base(f"Message edited in #{before.channel}", color=goodNeutralColor, description=f"**Before: **{before.content}\n**After: **{after.content}")

    embed.set_author(icon_url=before.author.avatar.url, name=before.author.name)
    embed.add_field(name=f"User ID: {before.author.id}", value="", inline=False)
    embed.set_footer(text=f"Message ID: {before.id}  •  {date}")
    return embed

def create_timed_out_embed(after):
    date = get_normalized_time()
    date_after = after.timed_out_until.strftime("%d %B %Y at %H:%M:%S")
    embed = create_embed_base("Member timed out", badColor, description=f"<@{after.id}>")

    embed.add_field(name=f"Timed out until: ", value=date_after, inline=False)

    embed.set_author(icon_url=after.avatar.url, name=after.name)
    embed.add_field(name=f"User ID: {after.id}", value="", inline=False)
    embed.set_footer(text=date)
    return embed

def create_timeout_remove_embed(after):
    date = get_normalized_time()

    embed = create_embed_base("Timeout removed", goodNeutralColor, description=f"<@{after.id}>")

    embed.set_author(icon_url=after.avatar.url, name=after.name)
    embed.add_field(name=f"User ID: {after.id}", value="", inline=False)
    embed.set_footer(text=date)
    return embed

def create_roles_changed_embed(before, after):
    date = get_normalized_time()
    roles_before = ""
    roles_after = ""
    for role in before.roles:
        if role.name != "@everyone":
            roles_before += " <@&" + str(role.id) + ">"
    for role in after.roles:  # after
        if role.name != "@everyone":
            roles_after += " <@&" + str(role.id) + ">"
    if len(after.roles) == 1:
        roles_after += "<no roles>"
    if len(before.roles) == 1:
        roles_before += "<no roles>"

    embed = create_embed_base("Roles updated", goodNeutralColor)
    embed.add_field(name="From: ", value=roles_before, inline=False)
    embed.add_field(name="To: ", value=roles_after, inline=False)

    embed.set_author(icon_url=before.avatar.url, name=before.name)
    embed.add_field(name=f"User ID: {before.id}", value="", inline=False)
    embed.set_footer(text=date)
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