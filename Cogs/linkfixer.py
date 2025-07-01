from discord.ext import commands
from linkfix import linkScript

class Linkfixer(commands.Cog, name = "linkfix"): #put all auto mod stuff here
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if "https://www.instagram.com/reels/" in message.content and self.bot.linkfixer_on is True: # TODO: add confing for this cog (is enabled) etc.
            await message.delete()
            domainType = "ddinstagram"
            swappedReel = message.content.replace("www.instagram.com", f"www.{domainType}.com")

            await message.channel.send(swappedReel)

# TODO: add removing and adding fixer links for mods, also swapping options for all users