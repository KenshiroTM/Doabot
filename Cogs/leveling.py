import discord
from discord.ext import commands, tasks

import embedMaker
from jsonreader import save_cfg
from levelingFiles import levelingScript

import re
class Leveling(commands.Cog, name = "leveling"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.recalculating = False
        self.autosave_levels.start()
        self.min_user_level = 0
        self.min_lvl_scaling = 1
        self.min_base_level = 1
        self.min_exp_per_lvl = 1
        self.min_required_lvl = 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.recalculating==True:
            return
        if self.bot.leveling_on is True:
            userid = message.author.id
            if levelingScript.add_exp(userid, self.bot.user_levels) is True:
                user_level = levelingScript.get_user_info(userid, self.bot.user_levels)
                roles = levelingScript.get_level_roles()
                await self.check_level_roles(message, roles, user_level)
                #adding level roles here

    @tasks.loop(seconds=60)
    async def autosave_levels(self):
        if self.bot.leveling_on is True and self.recalculating is False:
            save_cfg(levelingScript.users_cfg, self.bot.user_levels)
            print("autosaving levels...")

    @commands.command(brief="Check your level or another user's level.",
    help=("Displays the current level of you or the mentioned user. "
         "If no user is provided, it defaults to yourself."))
    @commands.cooldown(1,5, commands.BucketType.user) # 1 use per 5 seconds for each user
    async def lvl(self, ctx, member=commands.parameter(default=None, description="Optional. Mention or ID of the user to check.")):
        if not self.recalculating:
            if member is None:
                user_id = ctx.author.id
            else:
                user_id = int(re.sub("[<>@]", "", member))
            try:
                user_level = levelingScript.get_user_info(user_id, self.bot.user_levels)
                member = ctx.guild.get_member(int(user_id))
                exp_per_msg = levelingScript.get_leveling_config()["exp_per_msg"]
                embed = embedMaker.create_lvl_embed(member.name, user_level, member.avatar.url, exp_per_msg)
                await ctx.send(embed = embed)
            except Exception as e:
                print(e)
                await ctx.send("User has no level!")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")

    @commands.command(name="setlvl",brief="Manually set a user's level.", help="Sets the level of a specified user. This disables automatic leveling for them.")
    @commands.has_permissions(manage_roles=True)
    async def set_lvl(self, ctx, member=commands.parameter(description="Mention or ID of the user whose level you want to change."),
                      lvl=commands.parameter(description="The level to set for the user. Must be a number not less than 0.")):
        userid = re.sub("[<>@]", "", member)  # userid
        member = ctx.guild.get_member(int(userid))

        if int(userid) and int(lvl)>=self.min_user_level and self.recalculating==False:
            # setting level and putting it into config
            levelingScript.set_user_level(int(lvl), int(userid), self.bot.user_levels)
            user_level = levelingScript.get_user_info(int(userid), self.bot.user_levels)
            roles = levelingScript.get_level_roles()
            # adding/removing role do someone after adding a level
            await self.check_level_roles(ctx, roles, user_level)

            await ctx.send(f"Set level of **{member.name}** to **{lvl}**")
        elif not int(lvl):
            await ctx.send("Level argument has to be a number not less than 0!")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")
        else:
            await ctx.send("Ping user or provide userid")

    @commands.command(name="setlvlscaling", brief="Set level scaling factor.",
    help="Sets the scaling factor for level progression.\n"
         "Higher values make each level require more EXP.\n"
         "This recalculates all user levels.")
    @commands.has_permissions(manage_roles=True)
    async def set_lvl_scaling(self, ctx, lvl_scaling=commands.parameter(description="A decimal number used as EXP scaling factor (e.g., 1.25). Has to be not less than 1")):
        if float(lvl_scaling)>self.min_lvl_scaling and not self.recalculating:
            self.recalculating = True
            await ctx.send("Changing level formula for existing users, it might take a while...")
            levelingScript.set_level_scaler(float(lvl_scaling), self.bot.user_levels)
            for user in self.bot.user_levels["users"]: # checking all user roles!
                await self.check_level_roles(ctx, levelingScript.get_level_roles(), user)
            self.recalculating = False
            await ctx.send(f"Set level scaler to **{lvl_scaling}**")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")
        else:
            await ctx.send("Level argument scaling has to be a number higher than 1!")

    @commands.command(name="setbaselvlexp", brief="Set base EXP for level 1.",
    help="Sets the base EXP required to reach level 1.\n"
         "This defines the EXP curve starting point and recalculates all levels.")
    @commands.has_permissions(manage_roles=True)
    async def set_base_lvl_exp(self, ctx, base_lvl=commands.parameter(description="Number of EXP points required to reach level 1. Has to be not less than 1")):
        if int(base_lvl)>=self.min_base_level and not self.recalculating:
            self.recalculating = True
            await ctx.send("Changing level formula for existing users, it might take a while...")
            levelingScript.set_base_level_exp(int(base_lvl), self.bot.user_levels)
            for user in self.bot.user_levels["users"]:
                await self.check_level_roles(ctx, levelingScript.get_level_roles(), user)
            self.recalculating = False
            await ctx.send(f"Set base level (level 1) to **{base_lvl}**")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")
        else:
            await ctx.send("Base level has to be a number!")

    @commands.command(name="setxpgain",brief="Set EXP gained per message.",
    help="Sets the flat amount of EXP a user gains per eligible message.\n"
         "Helps control how fast users can level up.")
    @commands.has_permissions(manage_roles=True)
    async def set_xp_gain(self, ctx, xp_per_msg=commands.parameter(description="Flat EXP gained per message (integer). Has to be not less than 1")):
        if int(xp_per_msg)>=self.min_exp_per_lvl and self.recalculating==False:
            levelingScript.set_exp_gained(int(xp_per_msg))
            await ctx.send(f"Set exp gained to **{xp_per_msg}**")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")
        else:
            await ctx.send("Exp per message has to be a number!")

    @commands.group(name="lvlroles", invoke_without_command=True, brief="View configured level-based roles.",
    help="Displays all roles that are awarded at specific user levels.\n"
         "Use subcommands like `add` or `rm` to manage them.")
    async def lvl_roles(self, ctx):
        if not self.recalculating:
            embed = embedMaker.create_level_roles_embed(levelingScript.get_level_roles())
            await ctx.send(embed=embed)
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")

    @lvl_roles.command(name="add", brief="Add a role that is awarded at a level.",
                       help="Adds the mentioned role to the leveling system.\n"
         "When a user reaches the required level, they will be given this role.")
    @commands.has_permissions(manage_roles=True)
    async def lvl_role_add(self, ctx, role=commands.parameter(description="Role to assign (mention or ID)."),
                           required_level=commands.parameter(description="Minimum level required to receive the role (integer). Has to be not less than 1")):
        role_id = re.sub("[<>@&]", "", role)
        if int(role_id) and int(required_level)>=self.min_required_lvl and not self.recalculating:
            if levelingScript.add_level_role(int(required_level), int(role_id)):
                await ctx.send(f"Added {ctx.guild.get_role(int(role_id)).name} to leveling database with required level of {required_level}")
            else:
                await ctx.send(f"Role userid is already in database!")
        elif not int(required_level):
            await ctx.send("Required level has to be a number not less than 1!")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")
        else:
            await ctx.send("Ping role or provide role userid!")

    @lvl_roles.command(name="rm",brief="Remove a role from the leveling system.",
                       help="Removes a level-based role from the system.\n"
         "Users will no longer receive this role based on their level.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def level_role_remove(self, ctx, role=commands.parameter(description="Role to remove (mention or ID).")):
        role_id = re.sub("[<>@&]", "", role)
        if int(role_id) and self.recalculating==False:
            levelingScript.remove_level_role(int(role_id))
            await ctx.send(f"Successfully removed {ctx.guild.get_role(int(role_id)).name} from the database!")
        elif self.recalculating:
            await ctx.send("Currently recalculating user levels, try again later!")
        else:
            await ctx.send("Role userid has to be a number!")

    @staticmethod
    async def check_level_roles(ctx, roles, user):
        try:
            member = await ctx.guild.fetch_member(user["user_id"])
            for role in roles:
                new_role = ctx.guild.get_role(int(role["role_id"]))
                if role["level_required"] <= user["level"]:
                    if new_role not in ctx.author.roles:
                        await member.add_roles(new_role)
                elif role["level_required"] > user["level"]:
                    new_role = ctx.guild.get_role(int(role["role_id"]))
                    if new_role in ctx.author.roles:
                        await member.remove_roles(new_role)
        except Exception as e:
            print(e)
            print("User does not exist or bot has no manage_commands/role permissions!")
