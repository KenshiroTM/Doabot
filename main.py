# main.py
import os
import traceback

from dotenv import load_dotenv
import discord
from discord.ext import commands
from config_helpers import mass_check_json, clean_non_existent_users
from config_helpers.general import read_config_key
from utils.errors import InvalidUserReference

load_dotenv()
mass_check_json()
prefix = read_config_key("prefix")

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        self.server_id = read_config_key("server_id")
        self.delete_msg_days = read_config_key("delete_msg_days")
        self.timeout_amount = read_config_key("timeout_amount")

        self.blacklist_on = read_config_key("blacklist_on")
        self.linkfixer_on = read_config_key("linkfixer_on")
        self.antispam_on = read_config_key("antispam_on")

        self.spammer_timeout = read_config_key("spammer_timeout")
        self.expose_delete_hours = read_config_key("expose_delete_hours")

        super().__init__(command_prefix=prefix, intents=intents, owner_id=383722279089078272)

    async def load_cogs(self):
        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                extension = f"Cogs.{filename[:-3]}"
                try:
                    await self.load_extension(extension)
                    print(f"Loaded extension: {extension}")
                except Exception:
                    print(f"Failed to load extension {extension}:")
                    traceback.print_exc()

    async def setup_hook(self):
        await self.load_cogs()

    async def on_command_error(self, ctx, error):
        print(error)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required arguments!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
        elif isinstance(error, InvalidUserReference):
            await ctx.send("I couldn't find that user, please provide a valid mention or ID!")
        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = ', '.join(error.missing_permissions)
            await ctx.send(f"Bot is missing permissions: **{missing_perms}**")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("You are not an owner to use this command!")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("Mentioned role is not found!")
        elif isinstance(error, commands.CheckFailure):
            server_id = read_config_key("server_id")
            if ctx.guild is None or ctx.guild.id != server_id:
                await ctx.send(
                    "This bot is restricted to a specific server. "
                    "You can only use commands in the configured server."
                )
                return
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            await ctx.send("An error has occurred while executing this command!")

    async def on_ready(self):
        clean_non_existent_users(self)
        activity = discord.Game(name=f"Prefix is {self.command_prefix}")
        await self.change_presence(status=discord.Status.online, activity=activity)
        await self.tree.sync()
        print("Ready!")

if __name__ == '__main__':
    bot = Bot()
    bot.run(os.getenv("TOKEN"))
