import asyncio
from discord.ext import commands

from config_helpers import check_blacklist, check_scam_links, get_blacklisted_words, add_blacklisted_word, \
    remove_blacklisted_word
from config_helpers.blacklist import get_blacklisted_links, add_blacklisted_link, remove_blacklisted_link
from utils import check_server_id, EmbedMaker


class Automod(commands.Cog, name="automod"):
    def __init__(self, bot):
        self.bot = bot
        self.keyword_match_threshold = 2
        self.potential_spammers = []
        self.blacklisted_words = get_blacklisted_words()
        self.blacklisted_links = get_blacklisted_links()

    async def quick_delete(self, new_spammer):
        try:
            await asyncio.sleep(self.bot.spammer_timeout)
        except asyncio.CancelledError:
            return

        try:
            self.potential_spammers.remove(new_spammer)
        except ValueError:
            pass

    async def automod_spam(self, message):
        if not self.bot.blacklist_on:
            return
        if message.author.guild_permissions.ban_members:
            return

        has_image = any(
            att.content_type and att.content_type.startswith("image/")
            for att in message.attachments
        )
        has_text_spam = any(
            marker in message.content for marker in ["https://", "http://", "@everyone", "@here"]
        )

        if not (has_text_spam or has_image):
            return

        content_key = message.content
        if not content_key and message.attachments:
            content_key = message.attachments[0].filename

        new_spammer = {
            "userid": message.author.id,
            "content": content_key,
            "channel_id": message.channel.id,
        }
        for spammer in self.potential_spammers:
            if spammer["userid"] == new_spammer["userid"]:
                if spammer["channel_id"] != new_spammer["channel_id"] and spammer["content"] == new_spammer["content"]:
                    await message.delete()
                    await message.author.ban(
                        reason=f"Banned for suspected spam!",
                        delete_message_days=self.bot.delete_msg_days
                    )
                    self.potential_spammers[:] = [
                        x for x in self.potential_spammers if x["userid"] != message.author.id
                    ]
                    return
                return

        self.potential_spammers.append(new_spammer)
        asyncio.create_task(self.quick_delete(new_spammer))

    async def automod_blacklist(self, message):
        if not self.bot.blacklist_on:
            return
        if message.author.guild_permissions.ban_members:
            return
        # check blacklisted words
        blacklisted_msg = check_blacklist(message.content, self.blacklisted_words)
        if blacklisted_msg is not None:
            print(blacklisted_msg)
            await message.delete()
            await message.author.ban(
                reason=f"Banned for using a blacklisted word {blacklisted_msg}",
                delete_message_days=self.bot.delete_msg_days
            )
            return
        # Check scam links
        scam_link_msg = check_scam_links(message.content, self.blacklisted_links)
        if scam_link_msg is not None:
            await message.delete()
            await message.author.ban(
                reason="Suspected for scam link",
                delete_message_days=self.bot.delete_msg_days
            )
            return

    @commands.hybrid_group(
        name="bl",
        brief="Blacklist management.",
        help="Manages blacklisted words."
    )
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def blacklist(self, ctx):
        await ctx.send("Use `bl show`, `bl add`, or `bl rm`.")

    @blacklist.command(name="show", help="Shows all blacklisted words.")
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def show_blacklist(self, ctx):
        words = get_blacklisted_words()
        embed = EmbedMaker.create_blacklist_word_show_embed(words)
        await ctx.send(embed=embed)

    @blacklist.command(name="add", help="Adds a word to the blacklist.")
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def add_to_blacklist(self, ctx, case: str = commands.parameter(description="Case sensitivity: s (sensitive) or i (insensitive)"),
    *, word: str = commands.parameter(description="The word to add.")):

        case = case.lower().strip()
        if case not in ("s", "i"):
            await ctx.send("Specify case for sensitive or insensitive: `s` or `i`")
            return
        word = word.strip()
        if not word:
            await ctx.send("Please put a word you want to add!")
            return
        if not add_blacklisted_word(word, case):
            await ctx.send("Word already in database!")
        else:
            self.blacklisted_words = get_blacklisted_words()
            await ctx.send("Word added to database!")

    @blacklist.command(name="rm", help="Removes a word from the blacklist.")
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def remove_from_blacklist(self, ctx, case: str = commands.parameter(description="Case sensitivity: s (sensitive) or i (insensitive)"),
    *, word: str = commands.parameter(description="The word to remove.")):

        case = case.lower().strip()
        if case not in ("s", "i"):
            await ctx.send("Specify case for sensitive or insensitive: `s` or `i`")
            return
        word = word.strip()
        if not word:
            await ctx.send("Please put a word you want to remove!")
            return
        if not remove_blacklisted_word(word, case):
            await ctx.send("Word not found in database!")
        else:
            self.blacklisted_words = get_blacklisted_words()
            await ctx.send("Removed from database!")

    @commands.hybrid_group(
        name="link",
        brief="Anti-spam link blacklist system.",
        help="Manages spam link detection rules."
    )
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def link(self, ctx):
        await ctx.send("Use `link show`, `link add`, or `link rm`.")

    @link.command(name="show", help="Shows all blacklisted link rules.")
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def show_links(self, ctx):
        links = get_blacklisted_links()
        embed = EmbedMaker.create_scam_links_show_embed(links)
        await ctx.send(embed=embed)

    @link.command(name="add", help="Adds a new spam link rule.")
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def add_to_links(self, ctx, name: str = commands.parameter(description="Name of the rule."),
    threshold: int = commands.parameter(description="Keyword match threshold (min 2)."), *, keywords: str = commands.parameter(description="Space-separated keywords.")):
        keyword_list = [kw.strip() for kw in keywords.split() if kw.strip()]
        if threshold < self.keyword_match_threshold:
            await ctx.send("Threshold must be a number not less than 2!")
            return
        if not keyword_list:
            await ctx.send("Please provide at least one keyword!")
            return
        if add_blacklisted_link({"name": name, "threshold": threshold, "keywords": keyword_list}):
            self.blacklisted_links = get_blacklisted_links()
            await ctx.send("Successfully added a link rule!")
        else:
            await ctx.send("Name already in database!")

    @link.command(name="rm", help="Removes a spam link rule by name.")
    @check_server_id
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def remove_from_links(self, ctx, *, name: str = commands.parameter(description="Name of the link rule to remove.")):
        if not remove_blacklisted_link(name):
            await ctx.send("Link rule not found!")
        else:
            self.blacklisted_links = get_blacklisted_links()
            await ctx.send("Successfully removed the link rule!")

async def setup(bot):
    await bot.add_cog(Automod(bot))