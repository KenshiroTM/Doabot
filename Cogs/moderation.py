# Cogs/moderation.py
import asyncio
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

from utils import EmbedMaker
from utils.checks import check_server_id
from utils.discord_helpers import parse_user_id, resolve_member, resolve_user
from config_helpers.warns import add_warn, get_warns, remove_user_warn_data
from config_helpers.bans import get_last_bans, get_ban_by_position

class Moderation(commands.Cog, name="moderation"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.expose_messages = {}
        self.min_revert_users = 1
        self.max_revert_users = 3
        self.min_purge_msgs = 1
        self.max_purge_msgs = 100

    async def add_to_expose(self, message):
        if message.author.id in self.expose_messages:
            self.expose_messages[message.author.id]["task"].cancel()

        expires_at = datetime.now(timezone.utc) + timedelta(hours=self.bot.expose_delete_hours)

        async def delete_after():
            try:
                time = self.bot.expose_delete_hours * 3600 # making it hours there for sleeping
                await asyncio.sleep(time)
                self.expose_messages.pop(message.author.id, None)
            except asyncio.CancelledError:
                pass

        task = asyncio.create_task(delete_after())
        date = datetime.now(timezone.utc).strftime("%d %B %Y at %H:%M:%S")
        self.expose_messages[message.author.id] = {
            "task": task,
            "content": message.content,
            "date": date,
            "expires_at": expires_at,
        }

    @commands.hybrid_command(name="expose", brief="Display exposed deleted message of a user.",
        help="Displays the most recent deleted message of the specified user if they have any."
    )
    @discord.app_commands.describe(
        member="User to show expose for (mention or ID). Defaults to command user if omitted."
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def expose(self, ctx: commands.Context, member: str = commands.parameter(default=None, description="User to expose (mention or ID). Defaults to self if omitted.")):
        target = await resolve_user(self.bot, member) if member else ctx.author

        exposed = self.expose_messages.get(target.id)
        if exposed is None:
            await ctx.send(f"{target.name} has nothing to be exposed of!")
            return
        embed = EmbedMaker.create_expose_embed(target, exposed["content"], exposed["expires_at"], exposed["date"])
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ban", brief="Ban a user by mention or ID.",
        help="Bans a user from the server using either a mention or a user ID.\n"
             "You can optionally provide a reason. If none is given, 'No reason provided' will be used."
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban_user(self, ctx,
    member: str = commands.parameter(description="User to ban (mention or ID)."),
    *, reason: str = commands.parameter(default="No reason provided", description="Reason for the ban.")):
        target = await resolve_user(self.bot, member)

        try:
            await ctx.guild.fetch_ban(target)
            await ctx.send("User is already banned!")
            return
        except discord.NotFound:
            pass
        await ctx.guild.ban(target, delete_message_days=self.bot.delete_msg_days, reason=reason)
        await ctx.send(f"Successfully banned: **{target.name}**, reason: {reason}")

    @commands.hybrid_command(name="unban", brief="Unban a user by ID.",
        help="Unbans a previously banned user using their Discord ID.\n"
             "You can optionally provide a reason. If none is given, 'No reason provided' will be used."
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban_user(self, ctx, userid: str = commands.parameter(description="ID of the user to unban."),
    *, reason: str = commands.parameter(default="No reason provided", description="Reason for the unban.")):
        target = await resolve_user(self.bot, userid)

        try:
            await ctx.guild.unban(target, reason=reason)
        except discord.NotFound:
            await ctx.send("User is not banned on this server!")
            return

        await ctx.send(f"Successfully unbanned {target.name}, Reason: {reason}")

    @commands.hybrid_command(name="banrev", brief="Revert a recent ban by position (1st, 2nd, or 3rd).",
        help="Unbans a user based on their position in the recent bans list.\n"
             "Position 1 = most recent, 2 = second most recent, 3 = third most recent.\n\n"
             "**Parameters:**\n"
             "`second_arg` (optional): Position in recent bans to revert (1–3). Defaults to 1."
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban_rev(self, ctx, second_arg: int = commands.parameter(default=1, description="Position in recent bans list (1 = most recent, up to 3)")):

        if not (self.min_revert_users <= second_arg <= self.max_revert_users):
            await ctx.send(f"You can only revert up to the last {self.max_revert_users} bans!")
            return

        record = get_ban_by_position(second_arg)  # peek only - don't remove yet
        if record is None:
            await ctx.send("There aren't that many recent bans on record!")
            return

        target = await resolve_user(self.bot, str(record["userid"]))

        await ctx.guild.unban(target)
        # last_bans is updated centrally in the dispatcher cog (on_member_unban)
        await ctx.send(f"Successfully reverted the ban of {target.name}")

    @commands.hybrid_command(name="showbans", brief="Display the 3 most recent bans.",
                       help="Shows the 3 most recently banned users with their usernames and IDs.")
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def show_bans(self, ctx):
        last_bans = get_last_bans()
        if not last_bans:
            await ctx.send("No recent bans on record!")
            return

        lines = [
            f"({position}) username: {user['name']}, userid: {user['userid']}"
            for position, user in enumerate(reversed(last_bans), start=1)
        ]
        await ctx.send("List of recently banned users:\n```\n" + "\n".join(lines) + "\n```")

    @commands.hybrid_command(name="timeout", brief="Mute a user by ID or mention.",
        help="Times out a user for a number of hours.\n\n"
             "**Parameters:**\n"
             "`member`: User mention or ID\n"
             "`amount`: Number of hours to timeout (must be > 0)"
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout_user(self, ctx, member: str = commands.parameter(description="User mention or ID to timeout"), amount: int = commands.parameter(
        default=None, description="Duration of timeout in hours (must be > 0)")):
        if amount is None:
            amount = self.bot.timeout_amount
        if amount <= 0:
            await ctx.send("Timeout amount must be a number bigger than 0!")
            return

        target = await resolve_member(ctx, member)

        if target.timed_out_until is not None:
            await ctx.send("User already timed out!")
            return

        await target.timeout(timedelta(hours=amount))
        await ctx.send(f"Successfully timed out: **{target.name}** for {amount} hours!")

    @commands.hybrid_command(name="untimeout", brief="Un-mute a user by ID or mention.",
        help="Removes timeout from a user.\n\n"
             "**Parameters:**\n"
             "`member`: User mention or ID to remove timeout from"
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def un_timeout_user(self, ctx, member: str = commands.parameter(description="User mention or ID to untimeout")):
        target = await resolve_member(ctx, member)

        await target.timeout(None)
        await ctx.send(f"Successfully removed timeout from: **{target.name}**")

    @commands.hybrid_command(name="warns", brief="Show user's warns.", help="Displays the number of warnings a user has.")
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def user_warns(self, ctx, member: str = commands.parameter(default=None, description="Mention or ID of the user whose warnings you want to view.")):
        target = await resolve_member(ctx, member) if member else ctx.author

        warns = get_warns(target.id)
        if not warns:
            await ctx.send("User has no warns!")
            return

        embed = EmbedMaker.create_warns_embed(target, warns)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="warn", brief="Warn a user.", help="Adds a warning to a user with an optional description explaining the reason.")
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: str = commands.parameter(description="Mention or ID of the user to warn."), *, description: str = commands.parameter(
    default="No description provided.", description="Reason or context for the warning.")):
        target = await resolve_member(ctx, member)

        add_warn(target.id, description)
        await ctx.send(f"User {target.name} was warned, **{description}**")

    @commands.hybrid_command(name="clearwarns", brief="Clear user's warns.", help="Removes all warning records from the specified user.")
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def clear_user_warns(self, ctx, member: str = commands.parameter(description="Mention or ID of the user whose warnings should be cleared.")):
        user_id = parse_user_id(member)

        removed = remove_user_warn_data(user_id)
        target = ctx.guild.get_member(user_id)
        name = target.name if target else str(user_id)

        if removed:
            await ctx.send(f"Cleared warns of: {name}")
        else:
            await ctx.send(f"{name} has no warns to clear!")

    @commands.hybrid_command(name="purge", brief="Delete recent messages.", help="Deletes between 1 and 100 recent messages from the current channel.")
    @check_server_id
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge_messages(self, ctx, amount: int = commands.parameter(description="Number of messages to delete (1-100)")):
        if not (self.min_purge_msgs <= amount <= self.max_purge_msgs):
            await ctx.send(f"Amount must be between {self.min_purge_msgs} and {self.max_purge_msgs}!")
            return
        if ctx.interaction:
            await ctx.defer(ephemeral=False)
        purge_limit = amount + 1
        deleted = await ctx.channel.purge(limit=purge_limit)
        count = len(deleted) - 1
        try:
            msg = await ctx.channel.send(f"Deleted **{count}** messages!")
            await asyncio.sleep(5)
            await msg.delete()
        except discord.NotFound:
            pass

async def setup(bot):
    await bot.add_cog(Moderation(bot))