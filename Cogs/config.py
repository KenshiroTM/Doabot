import discord
from discord.ext import commands
import re

import levelingFiles.levelingScript
from jsonreader import load_cfg, cfg_name, save_cfg
from levelingFiles.levelingScript import leveling_cfg
class Config(commands.Cog, name = "config"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.command(name="prefix",brief="Set the command prefix for the bot.",
    help=("Sets the prefix the bot responds to.\n\n"
         "Usage: `prefix <symbol>`\n"
         "Example: `prefix !`\n\n"
         "Note: The prefix must be exactly 1 character long."))
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def prefix(self, ctx, prefix=commands.parameter(default=None, description="New prefix character (1 character only)")):
        if prefix is not None or len(prefix) != 1:
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
        if amount is not None and int(amount)>=1:
            data = load_cfg(cfg_name)
            data["mute_amount"] = int(amount)
            self.bot.mute_amount = int(amount)
            save_cfg(cfg_name, data)
            await ctx.send(f"Mute amount set to {amount} hours!")
        else:
            await ctx.send("Second argument can't be empty and has to be a number not less than 1!")

    @commands.command(name="deletemsgdays", brief="Set message deletion window for bans.", help="Specifies how many days of messages to delete when banning a user (0–7).")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def delete_msg_days(self, ctx, days=commands.parameter(default=None, description="Number of days to delete messages (0–7)")):
        if days is not None and 0 <= int(days) <= 7:
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

    @commands.command(name="logging", brief="Toggle logging on or off (requires a log channel).", help="Turns the logging system on or off. Requires that a logging channel is already set using the `log_channel` command.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def logging_on(self, ctx):
        if self.bot.get_channel(self.bot.logging_channel) is not None:
            data = load_cfg(cfg_name)
            if data["logging_on"] is True:
                data["logging_on"] = False
                self.bot.logging_on = False
                await ctx.send("Logging is now **off**")
            else:
                data["logging_on"] = True
                self.bot.logging_on = True
                await ctx.send("Logging is now **on**")
            save_cfg(cfg_name, data)
        else:
            await ctx.send("Set a proper logging channel first!")

    @commands.command(name="leveling", brief="Enable or disable the leveling system.", help="Toggles the leveling system. When on, users gain XP and levels from sending messages. You can fine-tune XP settings using `set_xp_gain`, `set_lvl`, etc.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def leveling_on(self, ctx):
        data = load_cfg(leveling_cfg)
        if data["leveling_on"] is True:
            data["leveling_on"] = False
            self.bot.leveling_on = False
            save_cfg(levelingFiles.levelingScript.users_cfg, self.bot.user_levels)
            await ctx.send("Leveling is now **off**")
        else:
            data["leveling_on"] = True
            self.bot.leveling_on = True
            await ctx.send("Leveling is now **on**")
        save_cfg(leveling_cfg, data)

    @commands.command(name="logchannel", brief="Set the logging channel.", help="Sets the channel where log messages (like message deletes, edits, etc.) will be sent.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def log_channel(self, ctx, channel=commands.parameter(description="Channel mention or ID to be used for logging.")):
        channel_id = re.sub("[<>#]", "", channel)
        if int(channel_id):
            data = load_cfg(cfg_name)
            data["logging_channel"] = int(channel_id)
            self.bot.logging_channel = int(channel_id)
            save_cfg(cfg_name, data)
            await ctx.send(f"logging channel set to {channel_id}")

    @commands.command(name="readmsg",brief="Set number of messages for context.", help="Defines how many recent messages the bot reads from the chat history to build context.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def read_msg(self, ctx, msg_amount=commands.parameter(description="Must be 10 or more.")):
        if msg_amount is not None and int(msg_amount)>=10:
            data = load_cfg(cfg_name)
            data["bot_read_msg"] = int(msg_amount)
            self.bot.bot_read_msg = int(msg_amount)
            save_cfg(cfg_name, data)
            await ctx.send(f"Chatbot now reads up to {msg_amount} messages!")
        else:
            await ctx.send("Second argument can't be empty and has to be a number not less than 10!")

    @commands.command(name="maxtokens", brief="Set max AI response length.", help="Defines the maximum response length the AI can generate, measured in tokens.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def max_tokens(self, ctx, max_tokens=commands.parameter(description="Minimum value: 150 tokens. ")):
        if max_tokens is not None and int(max_tokens)>=150:
            data = load_cfg(cfg_name)
            data["bot_max_tokens"] = int(max_tokens)
            self.bot.bot_max_tokens = int(max_tokens)
            save_cfg(cfg_name, data)
            await ctx.send(f"Chatbot tokens set to {max_tokens}!")
        else:
            await ctx.send("Second argument can't be empty and has to be a number not less than 150!")

    @commands.command(name="exposedeleteafter", brief="Set the duration before exposed messages are deleted.",
                      help="Sets the duration (in hours) after which exposed messages will be automatically deleted. Valid range is between 1 and 24 hours.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def expose_message_delete_after(self, ctx, hours=commands.parameter(description="Minimum value: 150 tokens. ")):
        if hours is not None and 24 >= int(hours) >= 1:
            hours_num = int(hours)*3600
            data = load_cfg(cfg_name)
            data["expose_delete_hours"] = int(hours_num)
            self.bot.expose_delete_hours = int(hours_num)
            save_cfg(cfg_name, data)
            hours_num /= 3600
            await ctx.send(f"Exposed messages will be deleted after {hours_num} hour/s")
        else:
            await ctx.send("Second argument can't be empty and has to be a number between 1 and 24!")

    @commands.command(name="chatboton",brief="Toggle AI chatbot functionality.", help="Enables or disables the chatbot feature for the entire server. When enabled, the chatbot will only respond when it is mentioned.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def chatbot_on(self, ctx):
        data = load_cfg(cfg_name)
        if data["chatbot_on"] is True:
            data["chatbot_on"] = False
            self.bot.chatbot_on = False
            save_cfg(cfg_name, data)
            await ctx.send("Chatbot is now **off**")
        else:
            data["chatbot_on"] = True
            self.bot.chatbot_on = True
            await ctx.send("Chatbot is now **on**")
        save_cfg(cfg_name, data)

    @commands.command(name="setserver", brief="Restrict bot to this server (owner only).", help="Restricts the bot so it can only operate in this server. Use this to prevent bot abuse if hosted publicly.")
    @commands.is_owner()
    async def set_server(self, ctx):
        server_id = ctx.guild.id
        data = load_cfg(cfg_name)
        data["server_id"] = int(server_id)
        self.bot.server_id = int(server_id)
        save_cfg(cfg_name, data)
        await ctx.send(f"server set to **{ctx.guild.name}**")