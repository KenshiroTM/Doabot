from discord.ext import commands
import discord

from jsonreader import save_cfg, load_cfg, cfg_name


class Linkfixer(commands.Cog, name = "linkfix"): #put all auto mod stuff here
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.bot_instagram_fixer = ["instagramez", "ddinstagram", "kkinstagram"]
        self.bot_instagram_link = "https://www.instagram.com"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot_instagram_link in message.content and self.bot.linkfixer_on is True:
            print(self.bot.instagram_fixer_idx)
            await message.delete()
            link = self.bot_instagram_fixer[self.bot.instagram_fixer_idx]
            swapped_reel = message.content.replace("www.instagram.com", f"www.{link}.com")
            reply_link = f"**Sent by {message.author}**\n{swapped_reel} \nEmbed does not work? Use `{self.bot.command_prefix}swap` to change embed link (3 second cooldown per use)"
            await message.channel.send(reply_link)

    @commands.command()
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.default)
    async def swap(self, ctx):
        await ctx.message.delete()
        previous_link = self.bot_instagram_fixer[self.bot.instagram_fixer_idx] #previous link

        if self.bot.instagram_fixer_idx==len(self.bot_instagram_fixer)-1: # move through indexes
            self.bot.instagram_fixer_idx=0
        else:
            self.bot.instagram_fixer_idx += 1
        current_link = self.bot_instagram_fixer[self.bot.instagram_fixer_idx]

        async for msg in ctx.channel.history(limit=20):
            if msg.author == self.bot.user and previous_link in msg.content:
                await msg.delete()
                content = msg.content.replace(f"www.{previous_link}.com", f"www.{current_link}.com")
                await msg.channel.send(content)
                data = load_cfg(cfg_name) # saving cfg
                data["instagram_fixer_idx"] = self.bot.instagram_fixer_idx
                save_cfg(cfg_name,data)
                return