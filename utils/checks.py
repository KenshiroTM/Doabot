# utils/checks.py
import discord
from discord.ext import commands
from config_helpers.general import read_config_key

@commands.check
async def check_server_id(ctx: commands.Context) -> bool:
    """Ensure commands are run only in the configured server ID."""
    server_id = read_config_key("server_id")
    return ctx.guild.id == server_id