import re
from typing import Optional

import discord
from discord.ext import commands

from utils.errors import InvalidUserReference


def try_strip_member(raw: Optional[str]) -> Optional[int]:
    """Extract a user ID from a mention (<@123>, <@!123>) or a raw ID string.

    Returns the parsed int, or None if `raw` is missing or not a valid ID.
    Never raises - safe to call with arbitrary user input. resolve_member
    and resolve_user use this internally and raise InvalidUserReference
    themselves when it comes back None.
    """
    if raw is None:
        return None
    stripped = re.sub(r"[<>@!]", "", raw).strip()
    return int(stripped) if stripped.isdigit() else None


def parse_user_id(raw: Optional[str]) -> int:
    """Like try_strip_member, but raises InvalidUserReference instead of
    returning None.

    Use this when you only need a bare ID and don't need to touch Discord
    at all (e.g. clearwarns, which just looks the ID up in local storage
    and should work even for users who already left the guild or whose
    Discord account no longer resolves).
    """
    user_id = try_strip_member(raw)
    if user_id is None:
        raise InvalidUserReference(raw)
    return user_id


async def resolve_member(ctx: commands.Context, raw: Optional[str]) -> discord.Member:
    """Resolve a mention/ID string into a guild Member.

    Raises InvalidUserReference if the string can't be parsed or the user
    isn't currently in the guild. Use this for actions that require the
    target to be a member right now (mute, warn, ...).
    """
    user_id = try_strip_member(raw)
    member = ctx.guild.get_member(user_id) if user_id is not None else None
    if member is None:
        raise InvalidUserReference(raw)
    return member


async def resolve_user(bot: commands.Bot, raw: Optional[str]) -> discord.User:
    """Resolve a mention/ID string into a discord.User via an API fetch.

    Raises InvalidUserReference if the string can't be parsed or no such
    user exists on Discord. Works even if the user already left the guild -
    use this for ban/unban style actions.
    """
    user_id = try_strip_member(raw)
    if user_id is None:
        raise InvalidUserReference(raw)
    try:
        return await bot.fetch_user(user_id)
    except discord.NotFound:
        raise InvalidUserReference(raw)