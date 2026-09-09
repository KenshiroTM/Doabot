from discord.ext import commands
from utils import check_server_id
from utils.image_editing import speechify
import io
import discord
import aiohttp

class Misc(commands.Cog, name="misc"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="speechify",
        brief="Adds a speech bubble to an image and returns it as a GIF",
        description="Takes an image URL, adds a speech bubble (1-2) with specified coverage ratio and returns as GIF.",
    )
    @check_server_id
    async def speechify(self, ctx: commands.Context, image_url: str, bubble_number: int = 1, bubble_height_ratio: float = 0.25):
        if bubble_number < 1 or bubble_number > 2:
            await ctx.reply("Bubble number must be between 1 and 2.")
            return
        if bubble_height_ratio < 0.1 or bubble_height_ratio > 0.5:
            await ctx.reply("Bubble ratio has to be between 0.1 or 0.5!")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    image_data = await resp.read()

            result = await speechify(image_data, bubble_number, bubble_height_ratio)
            file = discord.File(result, filename="speechified.gif")
            await ctx.reply(file=file)
        except Exception as e:
            await ctx.reply("Please enter a valid image URL (copy image link option).")

async def setup(bot):
    await bot.add_cog(Misc(bot))
