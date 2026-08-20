# Cogs/dispatcher.py
import datetime

import discord
from discord.ext import commands
from discord.ext.commands.bot import BotBase

from config_helpers.bans import add_to_last_bans, remove_from_last_bans

class Dispatcher(commands.Cog, name="dispatcher"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        automod_cog = self.bot.get_cog("automod")
        if automod_cog:
            await automod_cog.automod_spam(message)
            await automod_cog.automod_blacklist(message)

        linkfixer_cog = self.bot.get_cog("linkfixer")
        if linkfixer_cog:
            await linkfixer_cog.fix_links(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        moderation_cog = self.bot.get_cog("moderation")
        if moderation_cog:
            await moderation_cog.add_to_expose(message)  # from moderation cog!

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not self.bot.timekick_on:
            return
        if member.bot:
            return
        age_days = (datetime.datetime.now(datetime.timezone.utc) - member.created_at).days # check age of account in days
        if age_days < self.bot.timekick_days:
            await member.kick(reason=f"Account is too young to join this server. Minimum age has to be {self.bot.timekick_days}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        add_to_last_bans(user.name, user.id)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        remove_from_last_bans(user.id)



async def setup(bot):
    await bot.add_cog(Dispatcher(bot))