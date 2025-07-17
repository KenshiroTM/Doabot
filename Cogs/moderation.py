from datetime import datetime, timezone
import asyncio

from discord.ext import commands
import re

import embedMaker
from warns import warnsScript
from jsonreader import cfg_name, load_cfg, save_cfg

class Moderation(commands.Cog, name = "moderation"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.expose_messages = {}
        self.min_revert_users = 1
        self.max_revert_users = 3
        self.min_purge_msgs = 1
        self.max_purge_msgs = 100

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        if msg.author.id in self.expose_messages:
            self.expose_messages[msg.author.id]["task"].cancel()
        async def delete_after():
            try:
                await asyncio.sleep(self.bot.expose_delete_hours)
                self.expose_messages.pop(msg.author.id)
            except asyncio.CancelledError:
                pass
        task=asyncio.create_task(delete_after())
        date=datetime.now(timezone.utc).strftime("%d %B %Y at %H:%M:%S")
        self.expose_messages[msg.author.id] = {"task": task, "content": msg.content, "date": date}

    @commands.command(name="expose", brief="Track and collect deleted message of an user.",
                  help="Tracks and collects deleted message of a specified user to expose them. Provide a mention or ID of the user to start tracking their deleted message.")
    @commands.has_permissions(ban_members=True)
    async def expose_user(self, ctx, member=commands.parameter(description="User to ban (mention or ID).", default=None)):
        if member is None:
            user_id = ctx.author.id
        else:
            user_id = int(re.sub("[<>@]", "", member))
        member = ctx.guild.get_member(int(user_id))
        if member.id in self.expose_messages:
            exposed_message = self.expose_messages[member.id]["content"]
            delete_hours = self.bot.expose_delete_hours/3600
            date = self.expose_messages[member.id]["date"]
            embed = embedMaker.create_expose_embed(member, exposed_message, delete_hours, date)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.name} has nothing to be exposed of!")

    @commands.command(name="ban", brief="Ban a user by mention or ID.",
    help="Bans a user from the server using either a mention or a user ID.\n"
         "You can optionally provide a reason. If none is given, 'No reason provided' will be used.") #help when `help ban`, brief when `help`
    @commands.has_permissions(ban_members=True)  # * means many words for a reason
    @commands.bot_has_permissions(ban_members=True)
    async def ban_user(self, ctx, member=commands.parameter(description="User to ban (mention or ID)."),
                       *, reason=commands.parameter(default="No reason provided", description="Reason for the ban.")):  # = means it's not necessary to fill and gets "no reason provided" instead
        userid = re.sub("[<>@]", "", member)  # userid
        if int(userid):
            banned_member = await self.bot.fetch_user(int(userid))
            await ctx.guild.ban(banned_member, delete_message_days=self.bot.delete_msg_days)
            await ctx.send(f"Successfully banned: **{banned_member.name}**, reason: {reason}")
        else:
            ctx.send("I can only ban mentions or ids!")

    @commands.command(name="unban", brief="Unban a user by ID.",
    help="Unbans a previously banned user using their Discord ID.\n"
         "You can optionally provide a reason. If none is given, 'No reason provided' will be used.")  # change to hybrid command later on
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban_user(self, ctx, userid=commands.parameter(description="ID of the user to unban."),
                         *, reason=commands.parameter(default="No reason provided", description="Reason for the unban.")):
        if int(userid):
            user = await self.bot.fetch_user(int(userid))
            await ctx.guild.unban(user)
            await ctx.send(f"Successfully unbanned {user.name}, Reason: {reason}")
        else:
            ctx.send("I can only unban user ids!")

    @commands.command(name="banrev", brief="Revert a recent ban by position (1st, 2nd, or 3rd).",
    help="Unbans a user based on their position in the recent bans list.\n"
         "Position 1 = most recent, 2 = second most recent, 3 = third most recent.\n\n"
         "**Parameters:**\n"
         "`second_arg` (optional): Position in recent bans to revert (1–3). Defaults to 1.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban_rev(self, ctx, second_arg=commands.parameter(default=1, description="Position in recent bans list (1 = most recent, up to 3)")):
        data = load_cfg(cfg_name)
        if self.min_revert_users <= second_arg <= self.max_revert_users:
            array_place = len(data["last_bans"]) - second_arg

            userid = data["last_bans"][array_place]["userid"] #userid of user from recent bans config file
            user = await self.bot.fetch_user(int(userid))
            await ctx.guild.unban(user)

            data["last_bans"].pop(array_place)
            save_cfg(cfg_name, data)

            await ctx.send(f"Successfully reverted the ban of {user.name}")
        else:
            await ctx.send("You can unban up to last 3 users")
            
    @commands.command(name="showbans", brief="Display the 3 most recent bans.",
    help="Shows the 3 most recently banned users with their usernames and IDs.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def show_bans(self, ctx):
        data = load_cfg(cfg_name)
        last_bans = data["last_bans"]
        banned_users = "`"
        ctr = len(data["last_bans"])
        for user in last_bans:
            banned_users += "\n("+str(ctr)+") username: "+user["name"]+", userid: "+str(user["userid"])
            ctr -= 1
        await ctx.send("List of recently banned users: "+banned_users+"`")

    @commands.command(name="mute", brief="Mute a user by ID or mention.",
    help="Times out a user for a number of hours.\n\n"
         "**Parameters:**\n"
         "`member`: User mention or ID\n"
         "`amount`: Number of hours to mute (must be > 0)")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def mute_user(self, ctx, member = commands.parameter(description="User mention or ID to timeout"),
                        amount = commands.parameter(default=None, description="Duration of timeout in hours (must be > 0)")):
        userid = re.sub("[<>@]", "", member)  # userid
        if amount is None:
            amount = self.bot.mute_amount
        if not int(amount) and int(amount)>0:
            await ctx.send("Timeout amount must be a number bigger than 0!")
        if int(userid):
            timed_member = ctx.guild.get_member(int(userid))
            if timed_member.timed_out_until is None:
                await timed_member.timeout(datetime.timedelta(hours = amount))
                await ctx.send(f"Successfully timed out: **{timed_member.name}** for {amount} hours!")
            else:
                await ctx.send("User already timed out!")
        else:
            await ctx.send("I can only timeout mentions or ids!")

    @commands.command(name="unmute", brief="Un-mute a user by ID or mention.",
    help="Removes timeout from a user.\n\n"
         "**Parameters:**\n"
         "`member`: User mention or ID to remove timeout from")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def un_mute_user(self, ctx, member = commands.parameter(description="User mention or ID to untimeout")):
        userid = re.sub("[<>@]", "", member)  # userid
        if int(userid):
            timed_member = ctx.guild.get_member(int(userid))
            await timed_member.timeout(None)
            await ctx.send(f"Successfully removed timeout from: **{timed_member.name}**")
        else:
            await ctx.send("I can only remove timeout from mentions or ids!")

    @commands.command(name="warns", brief="Show user's warns.",
    help="Displays the number of warnings a user has.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def user_warns(self, ctx, member=commands.parameter(description="Mention or ID of the user whose warnings you want to view.")):
        if member is None:
            user_id = ctx.author.id
        else:
            user_id = re.sub("[<>@]", "", member)
        if int(user_id):
            user_warns = warnsScript.get_warns(int(user_id))
            if user_warns is not None:
                member = ctx.guild.get_member(int(user_id))
                embed = embedMaker.create_warns_embed(member, user_warns)
                await ctx.send(embed=embed)
            else:
                await ctx.send("User has no warns!")
        else:
            await ctx.send("type warn or warn with mention!")
            
    @commands.command(name="warn", brief="Warn a user.",
    help="Adds a warning to a user with an optional description explaining the reason.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def warn(self, ctx, member=commands.parameter(description="Mention or ID of the user to warn."),
                   description=commands.parameter(description="Reason or context for the warning. Defaults to 'No description provided'.", default="No description provided.")):
        userid = re.sub("[<>@]", "", member)  # userid
        if int(userid):
            warnsScript.add_warn(int(userid), description)
            member = ctx.guild.get_member(int(userid))
            await ctx.send(f"User {member.name} was warned, **{description}**")
        else:
            await ctx.send("I can only warn mentions or ids!")

    @commands.command(name="clearwarns", brief="Clear user's warns.",
    help="Removes all warning records from the specified user.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def clear_user_warns(self, ctx, member=commands.parameter(description="Mention or ID of the user whose warnings should be cleared.")):
        userid = re.sub("[<>@]", "", member)  # userid
        if int(userid):
            warnsScript.remove_user(int(userid))
            member = ctx.guild.get_member(int(userid))
            await ctx.send(f" Cleared warns of: {member.name}")
        else:
            await ctx.send("I can only clearwarn mentions or ids!")

    @commands.command(name="purge", brief="Delete recent messages.", help="Deletes between 1 and 100 recent messages from the current channel.")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge_messages(self, ctx, amount=commands.parameter(description="Number of messages to delete (1-100)")):
        if self.min_purge_msgs <= int(amount) <= self.max_purge_msgs:
            await ctx.channel.purge(limit=int(amount)+1)
            await ctx.send(f"Deleted {amount} messages!", delete_after=3)

    @commands.command(name="sync", brief="Sync slash commands with the bot.", help="Syncs hybrid (slash) commands with the bot. Restricted to bot owner only.")
    @commands.is_owner()  # sync, use only if update slash commands
    async def sync(self, ctx: commands.Context):
        synced = await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} command(s)")