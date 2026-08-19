# cogs/linkfixer.py
from discord.ext import commands
from config_helpers.linkfixer import (
    load_linkfixers,
    add_fixer,
    remove_fixer,
    increment_index,
    check_and_replace_links,
)
from utils import check_server_id


class Linkfixer(commands.Cog, name="linkfixer"):
    def __init__(self, bot):
        self.bot = bot
        self.linkfixer_links = load_linkfixers()
        self.hint = "\nEmbed does not work? Respond directly to this message and use ^swap command (3 second cooldown, support slash commands)"

    async def fix_links(self, message):
        if message.author.bot or not self.bot.linkfixer_on:
            return

        modified_msg, was_modified, can_swap = check_and_replace_links(
            message.content, self.linkfixer_links
        )

        if was_modified:
            await message.delete()
            response = f"**Sent by {message.author}**\n{modified_msg}"
            if can_swap:
                response += self.hint
            await message.channel.send(response)

    @commands.hybrid_group(
        name="linkfix",
        brief="Link fixer management.",
        help="Manages link replacement rules. Use subcommands: show, add, rm.",
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def linkfix(self, ctx):
        await ctx.send("Use `linkfix show`, `linkfix add`, or `linkfix rm`.")

    @linkfix.command(
        name="show",
        help="Displays all active link fixer rules with their current index.",
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def show_fixers(self, ctx):
        fixers = load_linkfixers()["fixers"]
        if not fixers:
            await ctx.send("No fixers configured.")
            return
        msg = "**Active Link Fixers:**\n"
        for f in fixers:
            msg += f"- `{f['name']}` -> {', '.join(f['link'])} (index: {f['index']})\n"
        await ctx.send(msg)

    @linkfix.command(
        name="add",
        help="Adds a new link fixer rule. Provide domain name and space-separated replacement links.",
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def add_fixer(self, ctx, name: str = commands.parameter(description="Name of the domain."), *,
    links: str = commands.parameter(description="Space-separated replacement links."),):

        links_list = [l.strip() for l in links.split() if l.strip()]
        if not links_list:
            await ctx.send("Please provide at least one link!")
            return
        success, msg = add_fixer(name, links_list)
        if success:
            self.linkfixer_links = load_linkfixers()
        await ctx.send(msg)

    @linkfix.command(
        name="rm",
        help="Removes a link fixer rule by its exact name.",
    )
    @check_server_id
    @commands.has_permissions(ban_members=True)
    async def remove_fixer(self, ctx, *, name: str = commands.parameter(description="Name of the fixer to remove."),):
        success = remove_fixer(name)
        if success:
            self.linkfixer_links = load_linkfixers()
            await ctx.send(f"Removed fixer '{name}'.")
        else:
            await ctx.send(f"Fixer '{name}' not found.")

    @commands.hybrid_command(
        name="swap",
        brief="Swaps to next replacement link.",
        help="Cycles through available replacement links for the last bot message in history.",
    )
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.default)
    async def swap(self, ctx):
        if ctx.interaction:
            await ctx.defer(ephemeral=False)

        active_links = {f["link"][f["index"]]: f["name"] for f in self.linkfixer_links["fixers"] if f["link"]}
        if not active_links:
            await ctx.send("No active fixers.", delete_after=3)
            return # check if there are any active links (there should be)

        target_msg = found_link = None
        async for msg in ctx.channel.history(limit=15):
            if msg.author != self.bot.user: continue
            for link in active_links:
                if link in msg.content:
                    target_msg, found_link = msg, link
                    break
            if target_msg: break # check if there is a target link in the message, if you find bot author AND catch the link, go return

        if not target_msg:
            await ctx.send("No replaceable link found.", delete_after=3) # if not just say it
            return

        try:
            await ctx.message.delete()
        except Exception:
            pass

        clean_content = target_msg.content.replace(self.hint, "")
        fixer_name = active_links[found_link] # remove hint and identify the fixer name

        # get whole object by name
        target_fixer = next((f for f in self.linkfixer_links["fixers"] if f["name"] == fixer_name), None)
        if not target_fixer: return

        new_idx = increment_index(fixer_name) # it auto updates json too
        new_link = target_fixer["link"][new_idx]

        response = clean_content.replace(found_link, new_link, 1) # replace current found link with new link from iterated stuff
        if len(target_fixer["link"]) > 1: response += self.hint # add hint if needed

        self.linkfixer_links = load_linkfixers()
        await target_msg.delete()
        await ctx.channel.send(response)

async def setup(bot):
    await bot.add_cog(Linkfixer(bot))