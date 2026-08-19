import discord


class EmbedMaker:
    """Utility class for creating Discord embeds."""

    @staticmethod
    def create_expose_embed(member, content, expires_at, date):
        embed = discord.Embed(
            title="Message Exposed",
            description=f"**{member.mention}**\n{content}",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Expires In",
            value=f"<t:{int(expires_at.timestamp())}:R>",
            inline=False
        )
        embed.set_footer(
            text=f"Deleted on: {date}",
            icon_url=member.display_avatar.url
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        return embed

    @staticmethod
    def create_warns_embed(member, warns):
        embed = discord.Embed(
            title=f"Warns for {member.name}",
            description=f"**{member.mention}** has **{len(warns)}** warn(s).",
            color=discord.Color.orange()
        )
        for index, warn in enumerate(warns, start=1):
            embed.add_field(
                name=f"Warn #{index}",
                value=warn,  # warn to string, nie dict
                inline=False
            )
        embed.set_thumbnail(url=member.display_avatar.url)
        return embed

    @staticmethod
    def create_blacklist_word_show_embed(words_dict):
        embed = discord.Embed(
            title="Blacklisted Words",
            description="Here are all currently blacklisted words.",
            color=discord.Color.dark_red()
        )

        sensitive = words_dict.get("sensitive", [])
        insensitive = words_dict.get("insensitive", [])

        if not sensitive and not insensitive:
            embed.add_field(
                name="No words",
                value="The blacklist is currently empty.",
                inline=False
            )
        else:
            # --- Sensitive ---
            if sensitive:
                chunk_size = 20
                for i in range(0, len(sensitive), chunk_size):
                    chunk = sensitive[i:i + chunk_size]
                    field_name = f"Sensitive {i + 1}–{min(i + chunk_size, len(sensitive))}"
                    field_value = "\n".join(f"• `{word}`" for word in chunk)
                    embed.add_field(name=field_name, value=field_value, inline=False)
            else:
                embed.add_field(name="Sensitive", value="*None*", inline=False)

            # --- Insensitive ---
            if insensitive:
                chunk_size = 20
                for i in range(0, len(insensitive), chunk_size):
                    chunk = insensitive[i:i + chunk_size]
                    field_name = f"Insensitive {i + 1}–{min(i + chunk_size, len(insensitive))}"
                    field_value = "\n".join(f"• `{word}`" for word in chunk)
                    embed.add_field(name=field_name, value=field_value, inline=False)
            else:
                embed.add_field(name="Insensitive", value="*None*", inline=False)

        embed.set_footer(text=f"Total words: {len(sensitive) + len(insensitive)}")
        return embed

    @staticmethod
    def create_scam_links_show_embed(links):
        embed = discord.Embed(
            title="Blacklisted Link Rules",
            description="Here are all currently configured scam link rules.",
            color=discord.Color.dark_orange()
        )

        if not links:
            embed.add_field(
                name="No rules",
                value="No link rules are currently configured.",
                inline=False
            )
        else:
            for index, link in enumerate(links, start=1):
                name = link.get("name", "Unnamed")
                threshold = link.get("threshold", "N/A")
                keywords = link.get("keywords", [])
                keywords_str = ", ".join(f"`{kw}`" for kw in keywords) if keywords else "`none`"

                embed.add_field(
                    name=f"Link Rule #{index}: {name}",
                    value=(
                        f"**Threshold:** `{threshold}`\n"
                        f"**Keywords:** {keywords_str}"
                    ),
                    inline=False
                )

        embed.set_footer(text=f"Total rules: {len(links)}")
        return embed