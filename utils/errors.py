from typing import Optional
from discord.ext import commands

class InvalidUserReference(commands.CommandError):
    """Raised when a mention/ID couldn't be resolved to a member or user."""

    def __init__(self, raw: Optional[str] = None):
        self.raw = raw
        super().__init__(f"Could not resolve user reference: {raw!r}")