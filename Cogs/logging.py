from discord.ext import commands

import embedMaker
import levelingFiles.levelingScript
import warns.warnsScript

from jsonreader import add_to_last_bans, remove_from_last_bans, save_cfg, load_cfg, cfg_name


class Logging(commands.Cog, name="logging"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    #message delete listener
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        if self.bot.logging_on is True:
            embed = embedMaker.create_deletion_embed(msg)
            channel = self.bot.get_channel(self.bot.logging_channel)
            await channel.send(embed=embed)
    #purge listener
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if self.bot.logging_on is True:

            embed = embedMaker.create_bulk_deletion_embed(messages)
            channel = self.bot.get_channel(self.bot.logging_channel)
            await channel.send(embed=embed)

    #message edit listener
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if self.bot.logging_on is True:
            channel = self.bot.get_channel(self.bot.logging_channel)
            embed = embedMaker.create_msg_edited_embed(before, after)
            await channel.send(embed=embed)
    #join listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        if self.bot.logging_on is True:
            channel = self.bot.get_channel(self.bot.logging_channel)
            embed = embedMaker.create_join_embed(member)
            await channel.send(embed=embed)
    #rolechange listener
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot:
            return
        if self.bot.logging_on is True:
            channel = self.bot.get_channel(self.bot.logging_channel)
            if after.roles != before.roles:
                embed = embedMaker.create_roles_changed_embed(before, after)
                await channel.send(embed=embed)
            # on timeout
            elif after.timed_out_until != before.timed_out_until:
                if after.timed_out_until is not None:
                    embed = embedMaker.create_timed_out_embed(after)
                    await channel.send(embed=embed)
                elif after.timed_out_until is None:
                    embed = embedMaker.create_timeout_remove_embed(after)
                    await channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member): #works
        print(guild)
        if member.bot:
            return
        if self.bot.logging_on is True:
            channel = self.bot.get_channel(self.bot.logging_channel)

            embed = embedMaker.create_ban_embed(member)
            await channel.send(embed=embed)
        add_to_last_bans(member.name, member.id)

        levelingFiles.levelingScript.remove_user(member.id, self.bot.user_levels) #user removal when banned
        warns.warnsScript.remove_user(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return
        levelingFiles.levelingScript.remove_user(member.id, self.bot.user_levels) # also when leaves
        warns.warnsScript.remove_user(member.id)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        print(guild)
        if member.bot:
            return
        if self.bot.logging_on is True:
            channel = self.bot.get_channel(self.bot.logging_channel)

            embed = embedMaker.create_unban_embed(member)
            await channel.send(embed=embed)
        remove_from_last_bans(member.id)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        # Check if the deleted channel is the logging channel
        if channel.id == self.bot.logging_channel:
            print(f"Logging channel {channel.name} has been deleted.")
            data = load_cfg(cfg_name)
            data["logging_on"] = False
            self.bot.logging_on = False
            save_cfg(cfg_name, data)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        levelingFiles.levelingScript.remove_level_role(role.id) # on role removal manually