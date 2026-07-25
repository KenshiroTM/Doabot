import discord
from discord.ext import commands
from jsonreader import load_cfg, cfg_name, save_cfg
class Config(commands.Cog, name = "config"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.min_muteamount = 1
        self.min_delete_msg_days = 0
        self.max_delete_msg_days = 7
        self.min_read_msg_amount = 10
        self.max_expose_msg_time = 24
        self.min_expose_msg_time = 1

    @commands.command(name="prefix",brief="Set the command prefix for the bot.",
    help=("Sets the prefix the bot responds to.\n\n"
         "Usage: `prefix <symbol>`\n"
         "Example: `prefix !`\n\n"
         "Note: The prefix must be exactly 1 character long."))
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def prefix(self, ctx, prefix=commands.parameter(default=None, description="New prefix character (1 character only)")):
        if prefix is not None and len(prefix) == 1:
            data = load_cfg(cfg_name)
            data["prefix"] = str(prefix)
            self.bot.command_prefix = prefix
            save_cfg(cfg_name, data)
            await ctx.send(f"Prefix is now set to **{prefix}**")
            activity = discord.Game(name=f"Prefix is {self.bot.command_prefix}")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
        else:
            await ctx.send("Second argument can't be empty or more than one character!")

    @commands.command(name="muteamount", brief="Set default mute duration in hours.", help="Defines the default duration (in hours) for mute command.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def mute_amount(self, ctx, amount=commands.parameter(default=None, description="Default mute duration in hours. Minimum 1")):
        try:
            if amount is not None and int(amount)>=self.min_muteamount:
                data = load_cfg(cfg_name)
                data["mute_amount"] = int(amount)
                self.bot.mute_amount = int(amount)
                save_cfg(cfg_name, data)
                await ctx.send(f"Mute amount set to {amount} hours!")
            else:
                await ctx.send("Second argument can't be empty and has to be a number not less than 1!")
        except TypeError:
            await ctx.send("Enter a valid number!")

    @commands.command(name="deletemsgdays", brief="Set message deletion window for bans.", help="Specifies how many days of messages to delete when banning a user (0–7).")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def delete_msg_days(self, ctx, days=commands.parameter(default=None, description="Number of days to delete messages (0–7)")):
        if days is not None and self.min_delete_msg_days <= int(days) <= self.max_delete_msg_days:
            data = load_cfg(cfg_name)
            data["delete_msg_days"] = int(days)
            self.bot.delete_msg_days = int(days)
            save_cfg(cfg_name, data)
            await ctx.send(f"Messages of banned users are purged starting from {days} days before ban!")
        else:
            await ctx.send("Second argument can't be empty and has to be a number!")

    @commands.command(name="blacklist", brief="Toggle the blacklist system on or off.", help="Enables or disables the blacklist feature. When enabled, the bot will scan messages for blacklisted words and take action if needed.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def blacklist_on(self, ctx):
        data = load_cfg(cfg_name)
        if data["blacklist_on"] is True:
            data["blacklist_on"] = False
            self.bot.blacklist_on = False
            await ctx.send("Blacklist is now **disabled**")
        else:
            data["blacklist_on"] = True
            self.bot.blacklist_on = True
            await ctx.send("Blacklist is now **enabled**")
        save_cfg(cfg_name, data)

    @commands.command(name="exposedeleteafter", brief="Set the duration before exposed messages are deleted.",
                      help="Sets the duration (in hours) after which exposed messages will be automatically deleted. Valid range is between 1 and 24 hours.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def expose_message_delete_after(self, ctx, hours=commands.parameter(description="Value between 24 and 1")):
        if hours is not None and self.max_expose_msg_time >= int(hours) >= self.min_expose_msg_time:
            hours_num = int(hours)*3600
            data = load_cfg(cfg_name)
            data["expose_delete_hours"] = int(hours_num)
            self.bot.expose_delete_hours = int(hours_num)
            save_cfg(cfg_name, data)
            hours_num /= 3600
            await ctx.send(f"Exposed messages will be deleted after {hours_num} hour(s)")
        else:
            await ctx.send("Second argument can't be empty and has to be a number between 1 and 24!")

    @commands.command(name="linkfixeron", brief="Toggle link fixer functionality.",
                      help="Enables or disables the link fix feature for the entire server. Run the help command for more info.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def linkfixer_on(self, ctx):
        data = load_cfg(cfg_name)
        if data["linkfixer_on"] is True:
            data["linkfixer_on"] = False
            self.bot.linkfixer_on= False
            save_cfg(cfg_name, data)
            await ctx.send("Link fixer is now **off**")
        else:
            data["linkfixer_on"] = True
            self.bot.linkfixer_on = True
            await ctx.send("Link fixer is now **on**")
        save_cfg(cfg_name, data)

    @commands.command(name="antispamon", brief="Toggle anti-spam functionality.",
                      help="Enables or disables the anti-spam feature for the entire server.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def antispam_on(self, ctx):
        data = load_cfg(cfg_name)
        if data.get("antispam_on", False) is True:
            data["antispam_on"] = False
            self.bot.antispam_on = False
            await ctx.send("Anti-spam is now **off**")
        else:
            data["antispam_on"] = True
            self.bot.antispam_on = True
            await ctx.send("Anti-spam is now **on**")
        save_cfg(cfg_name, data)

    @commands.command(name="spamtimeout", brief="Set anti-spam timeout.",
                      help="Sets how long (in seconds) a potential spammer stays in cache before being removed. Default is 4.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def spam_timeout(self, ctx,
                           seconds: int = commands.parameter(description="Timeout in seconds (min 3, max 20).",
                                                             default=None)):
        if seconds is None:
            await ctx.send(f"Current spam timeout: **{self.spammer_timeout}s**")
            return

        if seconds < 3 or seconds > 20:
            await ctx.send("Timeout must be between **3** and **20** seconds!")
            return

        data = load_cfg(cfg_name)
        data["spammer_timeout"] = seconds
        self.bot.spammer_timeout = seconds
        save_cfg(cfg_name, data)
        await ctx.send(f"Spam timeout set to **{seconds}s**")

    @commands.command(name="setserver", brief="Restrict bot to this server (owner only).", help="Restricts the bot so it can only operate in this server. Use this to prevent bot abuse if hosted publicly.")
    @commands.is_owner()
    async def set_server(self, ctx):
        server_id = ctx.guild.id
        data = load_cfg(cfg_name)
        data["server_id"] = int(server_id)
        self.bot.server_id = int(server_id)
        save_cfg(cfg_name, data)
        await ctx.send(f"server set to **{ctx.guild.name}**")