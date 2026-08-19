# Cogs/config.py
import discord
from discord.ext import commands
from config_helpers import (
    write_config_key,
    toggle_config_key,
    validate_and_write_numeric,
)
from utils.checks import check_server_id

class Config(commands.Cog, name="config"):
    def __init__(self, bot):
        self.bot = bot
        self.min_muteamount = 1
        self.min_delete_msg_days = 0
        self.max_delete_msg_days = 7
        self.min_expose_msg_time = 1
        self.max_expose_msg_time = 24
        self.min_spamtimeout = 3
        self.max_spamtimeout = 20

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="muteamount",
        brief="Set default mute duration in hours.",
        help="Defines the default duration (in hours) for mute command."
    )
    @discord.app_commands.describe(
        amount="Default mute duration in hours (minimum 1)"
    )
    async def muteamount(self, ctx: commands.Context, amount: int):
        """Set the default mute duration in hours (minimum 1)."""
        if amount < self.min_muteamount:
            await ctx.send(f"Amount must be at least {self.min_muteamount} hour(s)!")
            return

        write_config_key("timeout_amount", amount)
        self.bot.timeout_amount = amount
        await ctx.send(f"Mute amount set to **{amount} hour(s)**!")

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="deletemsgdays",
        brief="Set message deletion window for bans.",
        help="Specifies how many days of messages to delete when banning a user (0–7)."
    )
    @discord.app_commands.describe(
        days="Number of days to delete messages (0–7)"
    )
    async def deletemsgdays(self, ctx: commands.Context, days: int = 0):
        """Set how many days of messages to delete when banning a user (0–7)."""
        if not validate_and_write_numeric("delete_msg_days", days, self.min_delete_msg_days, self.max_delete_msg_days):
            await ctx.send("Days must be between 0 and 7!")
            return

        self.bot.delete_msg_days = days
        await ctx.send(f"Messages of banned users are purged starting from **{days} day(s)** before ban!")

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="blacklist",
        brief="Toggle the blacklist system on or off.",
        help="Enables or disables the blacklist feature. When enabled, the bot will scan messages for blacklisted words and take action if needed."
    )
    @discord.app_commands.describe()
    async def blacklist(self, ctx: commands.Context):
        """Toggle the blacklist system on or off."""
        new_state = toggle_config_key("blacklist_on")
        self.bot.blacklist_on = new_state
        await ctx.send(f"Blacklist is now **{'enabled' if new_state else 'disabled'}**")

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="exposedeleteafter",
        brief="Set the duration before exposed messages are deleted.",
        help="Sets the duration (in hours) after which exposed messages will be automatically deleted. Valid range is between 1 and 24 hours."
    )
    @discord.app_commands.describe(
        hours="Value between 1 and 24 hours"
    )
    async def exposedeleteafter(self, ctx: commands.Context, hours: int = 24):
        """Set the duration before exposed messages are deleted (1–24 hours)."""
        if not validate_and_write_numeric("expose_delete_hours", hours, self.min_expose_msg_time, self.max_expose_msg_time):
            await ctx.send("Hours must be between 1 and 24!")
            return

        self.bot.expose_delete_hours = hours
        await ctx.send(f"Exposed messages will be deleted after **{hours} hour(s)**!")

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="linkfixeron",
        brief="Toggle link fixer functionality.",
        help="Enables or disables the link fix feature for the entire server. Run the help command for more info."
    )
    @discord.app_commands.describe()
    async def linkfixeron(self, ctx: commands.Context):
        """Toggle link fixer functionality on or off."""
        new_state = toggle_config_key("linkfixer_on")
        self.bot.linkfixer_on = new_state
        await ctx.send(f"Link fixer is now **{'on' if new_state else 'off'}**")

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="antispamon",
        brief="Toggle anti-spam functionality.",
        help="Enables or disables the anti-spam feature for the entire server."
    )
    @discord.app_commands.describe()
    async def antispamon(self, ctx: commands.Context):
        """Toggle anti-spam functionality on or off."""
        new_state = toggle_config_key("antispam_on")
        self.bot.antispam_on = new_state
        await ctx.send(f"Anti-spam is now **{'on' if new_state else 'off'}**")

    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(
        name="spamtimeout",
        brief="Set anti-spam timeout.",
        help="Sets how long (in seconds) a potential spammer stays in cache before being removed. Default is 4."
    )
    @discord.app_commands.describe(
        seconds="Timeout in seconds (min 3, max 20)"
    )
    async def spamtimeout(self, ctx: commands.Context, seconds: int = None):
        """Set anti-spam timeout (3–20 seconds). Leave as default to see current value."""
        if seconds is None:
            await ctx.send(f"Current spam timeout: **{self.bot.spammer_timeout}s**")
            return

        if not validate_and_write_numeric("spammer_timeout", seconds, self.min_spamtimeout, self.max_spamtimeout):
            await ctx.send("Timeout must be between 3 and 20 seconds!")
            return

        self.bot.spammer_timeout = seconds
        await ctx.send(f"Spam timeout set to **{seconds}s**!")

    @commands.is_owner()
    @commands.hybrid_command(
        name="setserver",
        brief="Restrict bot to this server (owner only).",
        help="Restricts the bot so it can only operate in this server. Use this to prevent bot abuse if hosted publicly."
    )
    @discord.app_commands.describe()
    async def setserver(self, ctx: commands.Context):
        """Restrict bot to this server (owner only)."""
        write_config_key("server_id", ctx.guild.id)
        self.bot.server_id = ctx.guild.id
        await ctx.send(f"Server restricted to **{ctx.guild.name}**!")

async def setup(bot):
    await bot.add_cog(Config(bot))