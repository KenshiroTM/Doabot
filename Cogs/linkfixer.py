from discord.ext import commands
from linkfix import linkScript

class Linkfixer(commands.Cog, name = "linkfix"): #put all auto mod stuff here
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if "https://www.instagram.com/reels/" in message.content and self.bot.linkfixer_on is True:
            await message.delete()
            domainType = "ddinstagram" ##TODO: make it get from a database! Check for empty!
            swappedReel = message.content.replace("www.instagram.com", f"www.{domainType}.com")

            await message.channel.send(swappedReel)

    @commands.group(name="lf", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True) #TODO: add descriptions for both help and variables!
    async def lf(self, ctx):
        print("Displays links used")

    @lf.command(name="add")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def linkfixer_add(self, ctx, link_site, fixer_link):
        if linkScript.addSiteLink(link_site, fixer_link) is True:
            await ctx.send("Successfully added a fixer link!")
        else:
            await ctx.send("Site not supported for link fixing!")

    @lf.command(name="rm")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def linkfixer_remove(self, ctx, link_site, fixer_link):
        if linkScript.removeSiteLink(link_site, fixer_link) is True:
            await ctx.send("Successfully removed a fixer link!")
        else:
            await ctx.send("Site not supported for link fixing of link already removed!")

# TODO: add removing and adding fixer links for mods, also swapping options for all users