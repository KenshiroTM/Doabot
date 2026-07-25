import os

from discord.ext.commands import BotMissingPermissions
from dotenv import load_dotenv
import discord
from discord.ext import commands

import jsonChecker
import warns.warnsScript
# imports above ^^^^

# custom function imports

#cogs for function classification
from Cogs.automod import Automod
from Cogs.moderation import Moderation
from Cogs.linkfixer import Linkfixer
from Cogs.config import Config
from jsonreader import load_cfg, cfg_name
load_dotenv() # token in a variable

jsonChecker.mass_check_json()
prefix = load_cfg(cfg_name)["prefix"]

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True # for guild member fetching
        intents.message_content = True # for message content
        super().__init__(command_prefix=prefix, intents = intents, owner_id=383722279089078272,)

        self.mute_amount = load_cfg(cfg_name)["mute_amount"]
        self.delete_msg_days = load_cfg(cfg_name)["delete_msg_days"]
        self.server_id = load_cfg(cfg_name)["server_id"]
        self.expose_delete_hours = load_cfg(cfg_name)["expose_delete_hours"]

        self.blacklist_on = load_cfg(cfg_name)["blacklist_on"]

        self.linkfixer_on = load_cfg(cfg_name)["linkfixer_on"]
        self.instagram_fixer_idx = load_cfg(cfg_name)["instagram_fixer_idx"]

        self.antispam_on = load_cfg(cfg_name)["antispam_on"]
        self.spammer_timeout = load_cfg(cfg_name)["spammer_timeout"]

    # on command errors
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required arguments!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = ', '.join(error.missing_permissions)
            await ctx.send(f"Bot is missing permissions: **{missing_perms}**")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("You are not an owner to use this command!")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("Mentioned role is not found!")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Command is on cooldown!")
            return
        elif isinstance(error, commands.CommandNotFound): # do not type anything back
            return
        else:
            await ctx.send("An error has occurred while executing this command!")

    async def on_ready(self):
        await self.add_cog(Automod(self))
        await self.add_cog(Moderation(self))
        await self.add_cog(Linkfixer(self)) # adding cogs in the script
        await self.add_cog(Config(self))

        for guild in bot.guilds: # this code checks and cleans up any user that left the server on startup
            if bot.server_id == guild.id:
                #cleaning users
                warn_data = load_cfg(warns.warnsScript.warns_name)
                for warn_user in warn_data["users"]:
                    if not bot.get_user(warn_user["user_id"]):
                        warns.warnsScript.remove_user(warn_user["user_id"])
                print("clearing non existent users...")
        #checks for users

        activity = discord.Game(name=f"Prefix is {self.command_prefix}")

        await bot.change_presence(status=discord.Status.online, activity=activity)
        print("Ready!")

    #put config change somewhere here
    async def on_message(self, message):
        #if a bot then ignore
        if message.author.bot:
            return
        if self.server_id != message.guild.id and message.author.id != bot.owner_id: # further security measurement in case someone tries to invite my bot
            print("Server not configured to operate commands, ask owner to use set server command")
            return
        await self.process_commands(message)

if __name__ == '__main__':
    bot = Bot()
    bot.run(os.getenv("TOKEN"))