from discord.ext import commands

import embedMaker
from blacklist import blacklistScript


class Automod(commands.Cog, name = "automod"): #put all auto mod stuff here
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        # if a bot then ignore
        if message.author.bot:
            return
        if self.bot.blacklist_on: #checks if blacklist is on
            if not message.author.guild_permissions.ban_members: #check if it has ban members permissions, if it does then don't do anything
                blacklisted_msg = blacklistScript.check_blacklist(message.content) # get word from blacklist, if no word found then return "None"
                if blacklisted_msg is not None: #if a word is found then do this:
                    embed = embedMaker.create_blacklisted_word_embed(message, blacklisted_msg)
                    await message.delete()
                    await message.author.ban(reason=f"Banned for using a blacklisted word {blacklisted_msg}", delete_message_days=self.bot.delete_msg_days)
                    channel = self.bot.get_channel(self.bot.logging_channel)
                    await channel.send(embed = embed)
                    return
                scam_link_msg = blacklistScript.check_scam_links(message.content)
                if scam_link_msg is not None:
                    embed = embedMaker.create_scam_link_embed(message, scam_link_msg)
                    await message.delete()
                    await message.author.ban(reason=f"Suspected for scam link", delete_message_days=self.bot.delete_msg_days)
                    channel = self.bot.get_channel(self.bot.logging_channel)
                    await channel.send(embed = embed)
                    return

    # function for blacklist syntax
    @commands.group(name="bl", invoke_without_command=True, brief="Blacklist management (view, add, remove).", help="Shows the current list of blacklisted words. Use `bl add` to add words and `bl rm` to remove them.")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def blacklist(self, ctx):
        embed = embedMaker.create_blacklist_word_show_embed(blacklistScript.get_blacklisted_words())
        await ctx.send(embed=embed)

    @blacklist.command(name="add", help=(
            "Adds a word to the blacklist.\n"
            "Usage: `bl add <s/i> <word>`\n"
            "<s/i> = Specify whether the word should be case-sensitive or case-insensitive.\n"
            "`s` for sensitive (the word triggers a ban if it appears **anywhere** in a message).\n"
            "`i` for insensitive (the word triggers a ban only if it appears **isolated**, such as a word by itself).\n"
            "Example: `bl add s spam word` will ban users if `spam word` appears anywhere in a message.\n"
            "Example: `bl add i spam word` will only ban users if `spam word` appears as a standalone word."))
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def add_to_blacklist(self, ctx,
                               case: str = commands.parameter(description="Specify the case sensitivity: `s` for sensitive, `i` for insensitive."),
                               *,
                               word: str = commands.parameter(description="The word to add to the blacklist.")
                               ):
        if case not in ["s", "i"]:
            await ctx.send("Specify case for sensitive or insensitive `s/i`")
            return

        if word is None:
            await ctx.send("Please put a word you want to add!")
            return

        if not blacklistScript.add_blacklisted_word(word, case):
            await ctx.send("Word already in database!")
            return
        else:
            await ctx.send("Word added to database!")

    @blacklist.command(name="rm", help=(
            "Removes a word from the blacklist.\n"
            "Usage: `bl rm <s/i> <word>`\n"
            "<s/i> = Specify case-sensitive or case-insensitive for removal.\n"
            "`s` for sensitive (removes the word from sensitive matches).\n"
            "`i` for insensitive (removes the word from isolated matches only).\n"
            "Example: `bl rm i spam word` will remove `spam word` from the insensitive matches."))
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def remove_from_blacklist(self, ctx,
                                    case: str = commands.parameter(description="Specify the case sensitivity: `s` for sensitive, `i` for insensitive."),
                                    *,
                                    word: str = commands.parameter(description="The word to remove from the blacklist.")
                                    ):
        if case not in ["s", "i"]:
            await ctx.send("Specify case for sensitive or insensitive `s/i`")
            return

        if word is None:
            await ctx.send("Please put a word you want to add!")
            return

        if not blacklistScript.remove_blacklisted_word(word, case) and case is not None:
            await ctx.send("Word not found in database!")
        else:
            await ctx.send("Removed from database!")

    @commands.group(name = "link",brief="Anti-spam link blacklist system. Type help for more info" , invoke_without_command=True, help=("Manages the anti-spam link blacklist system.\n\n"
         "Use subcommands to add or remove spam link entries.\n"
         "Each link rule has:\n"
         "- A `name`: unique identifier for the link rule.\n"
         "- A `threshold`: how many keyword matches are needed before banning.\n"
         "- A list of `keywords`: words checked against each message.\n\n"
         "Use `link add` to create a new rule.\n"
         "Use `link rm` to remove a rule by name.\n"
         "Using just `link` will show all configured link rules."))
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def link(self, ctx):
        embed = embedMaker.create_scam_links_show_embed(blacklistScript.get_blacklisted_links())
        await ctx.send(embed = embed)

    @link.command(name="add", help=("Adds a new spam link rule to the blacklist.\n\n"
         "Arguments:\n"
         "- `name`: unique name for the rule.\n"
         "- `threshold`: number of keyword matches needed to trigger a ban.\n"
         "- `keywords`: space-separated list of keywords to detect in messages."))
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def add_to_links(self, ctx, name=commands.parameter(description="Name for the link rule (must be unique).", default=None),
                           threshold=commands.parameter(description="Number of keyword matches needed to trigger ban. Not less than 2", default=None),
                           *, keywords=commands.parameter(description="Space-separated list of keywords to match in messages.", default=None)):
        if name is None or threshold is None or keywords is None:
            return await ctx.send("All arguments have to be filled!")
        if int(threshold)>=2:
            link = {
                "name": name,
                "threshold": int(threshold),
                "keywords": keywords.split()
            }
            if blacklistScript.add_blacklisted_link(link) is True:
                await ctx.send("Successfully added a link!")
            else:
                await ctx.send("Name already in database!")
        else:
            await ctx.send("Threshold must be a number not less than 2!")

    @link.command(name="rm", help="Removes an existing spam link rule by its name.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def remove_from_links(self, ctx, name=commands.parameter(description="Name of the link rule to remove.", default=None)):
        if name is None:
            await ctx.send("Missing required arguments!")
        else:
            if blacklistScript.remove_blacklisted_link(name) is False:
                await ctx.send("Link rule not found!")
            else:
                await ctx.send("Successfully removed the link rule!")