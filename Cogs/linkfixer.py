from discord.ext import commands
import discord

class Linkfixer(commands.Cog, name = "linkfix"): #put all auto mod stuff here
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.bot_instagram_fixer = "instagramez"

    @commands.Cog.listener()
    async def on_message(self, message):
        if "https://www.instagram.com/reels/" in message.content and self.bot.linkfixer_on is True:
            await message.delete()
            domain_type = self.bot_instagram_fixer
            swapped_reel = message.content.replace("www.instagram.com", f"www.{domain_type}.com")
            reply_link = f"[Sent by {message.author}]({swapped_reel})"
            await message.channel.send(reply_link)