from discord.ext import commands

class Linkfixer(commands.Cog, name = "linkfixer"): #put all auto mod stuff here
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if("https://www.instagram.com/reels/" in message.content): # TODO: add confing for this cog (is enabled) etc.
            await message.delete()
            domainType = "ddinstagram"
            swappedReel = message.content.replace("www.instagram.com", f"www.{domainType}.com")
            await message.channel.send(swappedReel)