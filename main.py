import io
import discord
from discord import app_commands
from discord.ext import commands
import os
from datetime import timedelta
import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=",", intents=intents)

saved_channels = {
   "verify_channel_id": None,
   "welcome_channel_id": 1534367256665002044,
   "boost_channel_id": 1534425300098875613,
   "intro_channel_id": None,
   "mod_log_channel_id": 1536425646966706227,
   "approval_channel_id": 1534974589568942221
}

SPECIAL_USER_ID = 000000000000000000
TRIAL_MOD_ROLE_ID = 1536427161202860092

user_warns = {}
warned_messages = set()

# Anti-mass ban tracking
ban_tracker = {}

blacklisted_words = [
   "chink", "nigger", "nigga", "tranny", "faggot", "retard",
   "fag", "coon", "spic", "kike", "retarded", "dyke", "gook", "wetback"
]

class VerifyView(discord.ui.View):
   def __init__(self):
       super().__init__(timeout=None)

   @discord.ui.button(label="verify", style=discord.ButtonStyle.green, custom_id="verify_button")
   async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       role_id = 1534626110309011646
       role = interaction.guild.get_role(role_id)
      
       if role is None:
           await interaction.response.send_message("verification role not found on this server.", ephemeral=True)
           return

       if role in interaction.user.roles:
           await interaction.response.send_message("already verified", ephemeral=True)
       else:
           await interaction.user.add_roles(role)
           await interaction.response.send_message("you have been verified successfully!", ephemeral=True)

class ConfirmWarnView(discord.ui.View):
   def __init__(self, target_user_id: int):
       super().__init__(timeout=None)
       self.target_user_id = target_user_id

   @discord.ui.button(label="yes", style=discord.ButtonStyle.red, custom_id="confirm_warn_yes")
   async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.moderate_members:
           await interaction.response.send_message("you do not have permission to use this button.", ephemeral=True)
           return
      
       guild = interaction.guild
       target_user = guild.get_member(self.target_user_id)
      
       uid = self.target_user_id
       user_warns[uid] = user_warns.get(uid, 0) + 1
       count = user_warns[uid]

       if target_user:
           try:
               await target_user.send(f"you have been warned in **{guild.name}**.\nreason: hate speech / slurs\nwarn count: {count}/3")
           except:
               pass

       if count >= 3 and target_user:
           try:
               await target_user.ban(reason="reached 3 warnings via automod alert")
               user_warns[uid] = 0
               warned_messages.add(interaction.message.id)
               await interaction.response.edit_message(content=f"successfully warned <@{self.target_user_id}> ({count}/3). they reached 3 warnings and have been automatically banned.", view=None)
               return
           except:
               pass

       warned_messages.add(interaction.message.id)
       await interaction.response.edit_message(content=f"successfully warned <@{self.target_user_id}>. current warnings: {count}/3.", view=None)

   @discord.ui.button(label="no", style=discord.ButtonStyle.grey, custom_id="confirm_warn_no")
   async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.moderate_members:
           await interaction.response.send_message("you do not have permission to use this button.", ephemeral=True)
           return
       await interaction.response.edit_message(content="warning cancelled.", view=None)

class ModActionView(discord.ui.View):
   def __init__(self, target_user_id: int):
       super().__init__(timeout=None)
       self.target_user_id = target_user_id

   @discord.ui.button(label="warn user", style=discord.ButtonStyle.red, custom_id="mod_warn_button")
   async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.moderate_members:
           await interaction.response.send_message("you do not have permission to use this button.", ephemeral=True)
           return
      
       if interaction.message.id in warned_messages:
           view = ConfirmWarnView(self.target_user_id)
           await interaction.response.send_message("user has already been warned do u wanna warn again?", view=view, ephemeral=True)
           return

       guild = interaction.guild
       target_user = guild.get_member(self.target_user_id)
      
       uid = self.target_user_id
       user_warns[uid] = user_warns.get(uid, 0) + 1
       count = user_warns[uid]

       if target_user:
           try:
               await target_user.send(f"you have been warned in **{guild.name}**.\nreason: hate speech / slurs\nwarn count: {count}/3")
           except:
               pass

       if count >= 3 and target_user:
           try:
               await target_user.ban(reason="reached 3 warnings via automod alert")
               user_warns[uid] = 0
               warned_messages.add(interaction.message.id)
               await interaction.response.send_message(f"successfully warned <@{self.target_user_id}> ({count}/3). they reached 3 warnings and have been automatically banned.", ephemeral=True)
               return
           except:
               pass

       warned_messages.add(interaction.message.id)
       await interaction.response.send_message(f"successfully warned <@{self.target_user_id}>. current warnings: {count}/3.", ephemeral=True)

class StaffApplicationModal(discord.ui.Modal, title="staff application"):
   intro_ans = discord.ui.TextInput(
       label="1. introduce yourself & experience",
       style=discord.TextStyle.paragraph,
       placeholder="name, age, timezone, and past roles...",
       max_length=400
   )
   stand_out_ans = discord.ui.TextInput(
       label="2. what makes you stand out & your skills",
       style=discord.TextStyle.paragraph,
       placeholder="unique qualities, teamwork...",
       max_length=400
   )
   activity_ans = discord.ui.TextInput(
       label="3. how active are you?",
       style=discord.TextStyle.paragraph,
       placeholder="availability and hours per day...",
       max_length=400
   )
   raid_ans = discord.ui.TextInput(
       label="4. raid scenario",
       style=discord.TextStyle.paragraph,
       placeholder="steps to handle a server raid...",
       max_length=400
   )
   argument_ans = discord.ui.TextInput(
       label="5. member argument scenario",
       style=discord.TextStyle.paragraph,
       placeholder="handling drama calmly and fairly...",
       max_length=400
   )

   async def on_submit(self, interaction: discord.Interaction):
       app_channel_id = saved_channels.get("mod_log_channel_id")
       app_channel = interaction.guild.get_channel(app_channel_id) if app_channel_id else interaction.channel

       embed = discord.Embed(
           title="‎ ㅤ         𓈒    ✿    new staff application    𝅄          ۪    ݁    𓈒",
           description=f"𓈒  ✿  **applicant** :: {interaction.user.mention} (`{interaction.user.id}`)\n\n"
                       f"𓈒  ✿  **1. introduction & experience**\n> {self.intro_ans.value}\n\n"
                       f"𓈒  ✿  **2. stands out & skills**\n> {self.stand_out_ans.value}\n\n"
                       f"𓈒  ✿  **3. activity**\n> {self.activity_ans.value}\n\n"
                       f"𓈒  ✿  **4. raid scenario**\n> {self.raid_ans.value}\n\n"
                       f"𓈒  ✿  **5. argument scenario**\n> {self.argument_ans.value}",
           color=0x2b2d31
       )
       embed.set_footer(text=f"applicant_id:{interaction.user.id}")

       view = StaffReviewView(interaction.user.id)
       if app_channel:
           await app_channel.send(embed=embed, view=view)
      
       await interaction.response.send_message("your staff application has been submitted successfully!", ephemeral=True)

class StaffReviewView(discord.ui.View):
   def __init__(self, applicant_id: int):
       super().__init__(timeout=None)
       self.applicant_id = applicant_id

   @discord.ui.button(label="accept", style=discord.ButtonStyle.green, custom_id="staff_accept_btn")
   async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.administrator:
           await interaction.response.send_message("you do not have permission to accept applications.", ephemeral=True)
           return

       guild = interaction.guild
       member = guild.get_member(self.applicant_id)
       role = guild.get_role(TRIAL_MOD_ROLE_ID)

       if role and member:
           try:
               await member.add_roles(role)
           except:
               pass

       if member:
           try:
               await member.send("congratulations! your staff application for the server has been **accepted**. welcome to the team!")
           except:
               pass

       for item in self.children:
           item.disabled = True
       await interaction.response.edit_message(content=f"application accepted by {interaction.user.mention}.", view=self)

   @discord.ui.button(label="deny", style=discord.ButtonStyle.red, custom_id="staff_deny_btn")
   async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.administrator:
           await interaction.response.send_message("you do not have permission to deny applications.", ephemeral=True)
           return

       guild = interaction.guild
       member = guild.get_member(self.applicant_id)

       if member:
           try:
               await member.send("thank you for applying. unfortunately, your staff application has been **denied** at this time.")
           except:
               pass

       for item in self.children:
           item.disabled = True
       await interaction.response.edit_message(content=f"application denied by {interaction.user.mention}.", view=self)

class TrialModApprovalView(discord.ui.View):
   def __init__(self, mod_id: int, action_type: str, target_id: int, reason: str):
       super().__init__(timeout=None)
       self.mod_id = mod_id
       self.action_type = action_type
       self.target_id = target_id
       self.reason = reason

   @discord.ui.button(label="approve", style=discord.ButtonStyle.green, custom_id="trial_approve_btn")
   async def approve_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.administrator:
           await interaction.response.send_message("you do not have permission to approve this action.", ephemeral=True)
           return

       guild = interaction.guild
       target_member = guild.get_member(self.target_id)

       if target_member:
           try:
               if self.action_type == "ban":
                   await target_member.ban(reason=f"approved trial mod action by user id {self.mod_id}: {self.reason}")
               elif self.action_type == "kick":
                   await target_member.kick(reason=f"approved trial mod action by user id {self.mod_id}: {self.reason}")
           except Exception as e:
               await interaction.response.send_message(f"failed to execute action: {e}", ephemeral=True)
               return

       for item in self.children:
           item.disabled = True
       await interaction.response.edit_message(content=f"action approved and executed by {interaction.user.mention}.", view=self)

   @discord.ui.button(label="decline", style=discord.ButtonStyle.red, custom_id="trial_decline_btn")
   async def decline_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.user.guild_permissions.administrator:
           await interaction.response.send_message("you do not have permission to decline this action.", ephemeral=True)
           return

       for item in self.children:
           item.disabled = True
       await interaction.response.edit_message(content=f"action declined by {interaction.user.mention}.", view=self)

class StaffAppView(discord.ui.View):
   def __init__(self):
       super().__init__(timeout=None)

   @discord.ui.button(label="apply for staff", style=discord.ButtonStyle.green, custom_id="apply_staff_button")
   async def apply_button(self, interaction: discord.Interaction, button: discord.ui.Button):
       await interaction.response.send_modal(StaffApplicationModal())

@bot.event
async def on_ready():
   bot.add_view(VerifyView())
   bot.add_view(StaffAppView())
   try:
       await bot.tree.sync()
       print("slash commands synced successfully.")
   except Exception as e:
       print(f"failed to sync slash commands: {e}")
   print(f"logged in as {bot.user}".lower())

@bot.event
async def on_member_join(member):
   if member.id == SPECIAL_USER_ID:
       role_id = 1534626110309011646
       role = member.guild.get_role(role_id)
       if role:
           try:
               await member.add_roles(role)
           except:
               pass

   channel_id = saved_channels["welcome_channel_id"]
   channel = member.guild.get_channel(channel_id) if channel_id else None
   if not channel and channel_id:
       try:
           channel = await member.guild.fetch_channel(channel_id)
       except:
           pass
   if channel:
       if member.id == SPECIAL_USER_ID:
           await channel.send(embed=get_special_welcome_embed(member))
       else:
           await channel.send(embed=get_decorated_welcome_embed(member))

def get_decorated_verify_embed():
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    verify here!    𝅄          ۪    ݁    𓈒",
       description="‎\n‎ ㅤ ۪ 𝅄 press the button below to gain access to the rest of the server !",
       color=0x2b2d31
   )
   embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535053228784357447/41E85482-D59D-4342-ACDB-F323F94F743B.gif?ex=6a765d39&is=6a750bb9&hm=2e10bf1bcf4be571b00387370d5a95e8213dd3045bcc90f054fc3a16210b78d5&")
   return embed

def get_decorated_welcome_embed(target_user):
   embed = discord.Embed(
       description=(
           ".    . .    ˚ . .  .    ˚ .     . .    ˚ . ⁠\n"
           f", ⟡ ‎﹒ ⟢﹒‎﹒**welc**… {target_user.mention}! ❞ ‎﹒\n"
           "⁠♫・<#1534369682331799552> ⁠⭓<#1534369268748128328> ‎﹒ ❀\n"
           "𝆕    ◟ , enjoy your stay! "
       ),
       color=0x2b2d31
   )
   embed.set_author(name="𓈒    ✿    new arrival!    𝅄", icon_url=target_user.display_avatar.url)
   embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535052679078744084/78700BDC-447A-4AF3-A5C5-508BABB43DEB.gif?ex=6a765cb6&is=6a750b36&hm=fb2d433ba29225b888b70f977c512ffc37605343f28dea328f18a5511034463f&")
   return embed

def get_special_welcome_embed(target_user):
   embed = discord.Embed(
       description="Hello gays I am here you love me yes i am pregnant tommorow",
       color=0x2b2d31
   )
   embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NxExeHU3b2wzc3pjd2tlbHl0anhrOTllcmNsa29nYTM1bHFlb3Fwd2h4NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WNID1qQURzmq1D8zDC/giphy.gif")
   return embed

def get_decorated_boost_embed(target_user):
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    thank you for boosting!    𝅄          ۪    ݁    𓈒",
       description=f"‎\n‎ ㅤ ۪ 𝅄 tysm for boosting the server {target_user.mention}! we appreciate your support!",
       color=0x2b2d31
   )
   embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535053258593407048/F78E6667-7B31-4736-8E4D-9337BDAF3FD0.gif?ex=6a765d40&is=6a750bc0&hm=3557e5a996b0f4584c6e00ade1d6fedd1ad9460fe27d8a0f16cea8b6a1157a36&")
   return embed

def get_decorated_rules_embed():
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    server rules!    𝅄          ۪    ݁    𓈒",
       description=(
           "‎\n"
           "𓈒  ✿  **no slurs**\n"
           "   𝅄 racist, homophobic, or hate-driven language is strictly prohibited.\n\n"
           "𓈒  ✿  **follow guidelines**\n"
           "   𝅄 adhere to discord's terms of service.\n\n"
           "𓈒  ✿  **no nsfw or toxicity**\n"
           "   𝅄 avoid explicit content, e-dating, and public toxicity.\n\n"
           "𓈒  ✿  **no public drama**\n"
           "   𝅄 keep arguments in private messages or ping staff.\n\n"
           "𓈒  ✿  **3 warn system**\n"
           "   𝅄 receiving 3 formal staff warnings results in an automatic ban."
       ),
       color=0x2b2d31
   )
   return embed

def get_decorated_commands_embed():
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    bot commands list    𝅄          ۪    ݁    𓈒",
       description=(
           "‎\n"
           "𓈒  ✿  **general** :: `,rules`, `,verify`, `,staff`, `/membercount`, `/commands`\n"
           "𓈒  ✿  **moderation** :: `,c`, `,lock`, `/warn`, `/ban`, `/mute`"
       ),
       color=0x2b2d31
   )
   return embed

def get_decorated_staff_app_embed():
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    staff applications    𝅄          ۪    ݁    𓈒",
       description=(
           "‎\n"
           "want to help our team grow and keep the community safe? fill out an application below!\n\n"
           "**requirements:**\n"
           "• be active and respectful\n"
           "• provide honest and detailed answers\n\n"
           "‎ ㅤ ۪ 𝅄 click the button below to open the application form !"
       ),
       color=0x2b2d31
   )
   return embed

def get_decorated_automod_embed(target_user, offending_message):
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    automod alert :: slur detected    𝅄          ۪    ݁    𓈒",
       description=(
           f"‎\n"
           f"𓈒  ✿  **offending user** :: {target_user.mention} (`{target_user.id}`)\n"
           f"𓈒  ✿  **channel** :: {offending_message.channel.mention}\n\n"
           f"𓈒  ✿  **message content** ::\n"
           f"> {offending_message.content}\n\n"
           f"‎ ㅤ ۪ 𝅄 should we warn this user for saying this?"
       ),
       color=0x2b2d31
   )
   embed.set_footer(text="automod protection system active")
   return embed

@bot.event
async def on_message(message):
   if message.author.bot:
       return

   content_lower = message.content.lower()
   if any(word in content_lower for word in blacklisted_words):
       try:
           await message.delete()
       except:
           pass

       log_channel_id = saved_channels["mod_log_channel_id"]
       log_channel = message.guild.get_channel(log_channel_id) if log_channel_id else None

       if log_channel:
           view = ModActionView(message.author.id)
           await log_channel.send(
               embed=get_decorated_automod_embed(message.author, message),
               view=view
           )
       return

   if message.type in (discord.MessageType.premium_guild_subscription,
                       discord.MessageType.premium_guild_tier_1,
                       discord.MessageType.premium_guild_tier_2,
                       discord.MessageType.premium_guild_tier_3):
       try:
           await message.delete()
       except (discord.Forbidden, discord.HTTPException):
           pass

       channel_id = saved_channels["boost_channel_id"]
       channel = message.guild.get_channel(channel_id) if channel_id else None
       if not channel and channel_id:
           try:
               channel = await message.guild.fetch_channel(channel_id)
           except:
               pass
       if not channel:
           channel = message.channel
      
       if channel:
           await channel.send(embed=get_decorated_boost_embed(message.author))

   await bot.process_commands(message)

@bot.command(name="rules")
async def rules_command(ctx):
   try:
       await ctx.message.delete()
   except:
       pass
   await ctx.send(embed=get_decorated_rules_embed())

@bot.command(name="verify")
async def verify_prefix_command(ctx):
   try: await ctx.message.delete()
   except: pass
   saved_channels["verify_channel_id"] = ctx.channel.id
   await ctx.send(embed=get_decorated_verify_embed(), view=VerifyView())

@bot.command(name="staff")
@commands.has_permissions(administrator=True)
async def staff_panel_command(ctx):
   try:
       await ctx.message.delete()
   except:
       pass
   await ctx.send(embed=get_decorated_staff_app_embed(), view=StaffAppView())

@bot.command(name="welcome")
@commands.has_permissions(manage_guild=True)
async def manual_welcome(ctx, member: discord.Member):
   try:
       await ctx.message.delete()
   except:
       pass
  
   channel_id = saved_channels["welcome_channel_id"]
   channel = ctx.guild.get_channel(channel_id) if channel_id else ctx.channel
   if not channel and channel_id:
       try:
           channel = await ctx.guild.fetch_channel(channel_id)
       except:
           channel = ctx.channel

   if member.id == SPECIAL_USER_ID:
       await channel.send(embed=get_special_welcome_embed(member))
   else:
       await channel.send(embed=get_decorated_welcome_embed(member))

@bot.command(name="boost")
@commands.has_permissions(manage_guild=True)
async def manual_boost(ctx, member: discord.Member):
   try:
       await ctx.message.delete()
   except:
       pass
  
   channel_id = saved_channels["boost_channel_id"]
   channel = ctx.guild.get_channel(channel_id) if channel_id else ctx.channel
   if not channel and channel_id:
       try:
           channel = await ctx.guild.fetch_channel(channel_id)
       except:
           channel = ctx.channel

   await channel.send(embed=get_decorated_boost_embed(member))

@bot.command(name="c")
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int = None):
   try:
       await ctx.message.delete()
   except:
       pass
  
   if amount is None:
       await ctx.channel.purge(limit=None)
   else:
       await ctx.channel.purge(limit=amount)

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx):
   try:
       await ctx.message.delete()
   except:
       pass
  
   role_id = 1534626110309011646
   role = ctx.guild.get_role(role_id)
  
   if role is None:
       await ctx.send("lock role not found on this server.", delete_after=5)
       return

   overwrite = ctx.channel.overwrites_for(role)
   overwrite.send_messages = False
   await ctx.channel.set_permissions(role, overwrite=overwrite)
   await ctx.send("channel has been locked for that role.", delete_after=5)

@bot.command(name="cmds")
async def cmds_prefix_command(ctx):
   try:
       await ctx.message.delete()
   except:
       pass
   await ctx.send(embed=get_decorated_commands_embed())

@bot.tree.command(name="commands", description="show all bot commands")
async def commands_slash(interaction: discord.Interaction):
   await interaction.response.send_message(embed=get_decorated_commands_embed(), ephemeral=True)

@bot.tree.command(name="cmds", description="show all bot commands")
async def cmds_slash_alt(interaction: discord.Interaction):
   await interaction.response.send_message(embed=get_decorated_commands_embed(), ephemeral=True)

@bot.tree.command(name="staff", description="send the staff application panel")
async def staff_slash(interaction: discord.Interaction):
   if not interaction.user.guild_permissions.administrator:
       await interaction.response.send_message("you do not have permission to use this command.", ephemeral=True)
       return
   await interaction.response.send_message(embed=get_decorated_staff_app_embed(), view=StaffAppView(), ephemeral=True)

@bot.tree.command(name="membercount", description="show total members, humans, and bots")
async def membercount_slash(interaction: discord.Interaction):
   guild = interaction.guild
   total = guild.member_count
   humans = sum(1 for m in guild.members if not m.bot)
   bots = sum(1 for m in guild.members if m.bot)
   
   embed = discord.Embed(
       title="‎ ㅤ         𓈒    ✿    server member count    𝅄          ۪    ݁    𓈒",
       description=f"𓈒  ✿  **total members** :: `{total}`\n𓈒  ✿  **humans** :: `{humans}`\n𓈒  ✿  **bots** :: `{bots}`",
       color=0x2b2d31
   )
   await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="warn", description="warn a user")
@app_commands.describe(member="user to warn", reason="reason for warn")
async def warn_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "no reason provided"):
   trial_role = interaction.guild.get_role(TRIAL_MOD_ROLE_ID)
   is_trial_mod = trial_role in interaction.user.roles if trial_role else False

   if is_trial_mod and not interaction.user.guild_permissions.administrator:
       approval_channel = interaction.guild.get_channel(saved_channels["approval_channel_id"])
       if approval_channel:
           embed = discord.Embed(
               title="trial mod action approval required",
               description=f"**trial mod:** {interaction.user.mention}\n**action:** warn\n**target:** {member.mention}\n**reason:** {reason}",
               color=0xffaa00
           )
           await approval_channel.send(embed=embed)
       await interaction.response.send_message("your action requires admin approval and has been sent to the approval channel.", ephemeral=True)
       return

   if not interaction.user.guild_permissions.moderate_members:
       await interaction.response.send_message("you do not have permission to warn members.", ephemeral=True)
       return
       
   uid = member.id
   user_warns[uid] = user_warns.get(uid, 0) + 1
   count = user_warns[uid]
   
   try:
       await member.send(f"you have been warned in **{interaction.guild.name}**.\nreason: {reason}\nwarn count: {count}/3")
   except:
       pass
       
   if count >= 3:
       try:
           await member.ban(reason="reached 3 warnings")
           user_warns[uid] = 0
           await interaction.response.send_message(f"warned {member.mention} ({count}/3). they reached 3 warnings and were automatically banned.", ephemeral=True)
           return
       except Exception as e:
           await interaction.response.send_message(f"warned {member.mention} ({count}/3) but failed to ban: {e}", ephemeral=True)
           return
           
   await interaction.response.send_message(f"successfully warned {member.mention}. current warnings: {count}/3.", ephemeral=True)

@bot.tree.command(name="mute", description="mute a user for a specified duration")
@app_commands.describe(member="user to mute", time_str="duration (e.g. 10m, 1h, 1d)", reason="reason for mute")
async def mute_slash(interaction: discord.Interaction, member: discord.Member, time_str: str, reason: str = "no reason provided"):
   trial_role = interaction.guild.get_role(TRIAL_MOD_ROLE_ID)
   is_trial_mod = trial_role in interaction.user.roles if trial_role else False

   if is_trial_mod and not interaction.user.guild_permissions.administrator:
       await interaction.response.send_message("trial mods cannot use mute without direct admin approval.", ephemeral=True)
       return

   if not interaction.user.guild_permissions.moderate_members:
       await interaction.response.send_message("you do not have permission to mute members.", ephemeral=True)
       return

   seconds = 0
   unit = time_str[-1].lower()
   val = time_str[:-1]

   if not val.isdigit():
       await interaction.response.send_message("invalid time format. use something like `10m`, `1h`, or `1d`.", ephemeral=True)
       return

   amount = int(val)
   if unit == 's':
       seconds = amount
   elif unit == 'm':
       seconds = amount * 60
   elif unit == 'h':
       seconds = amount * 3600
   elif unit == 'd':
       seconds = amount * 86400
   else:
       await interaction.response.send_message("invalid time unit. use `s`, `m`, `h`, or `d`.", ephemeral=True)
       return

   duration = timedelta(seconds=seconds)
   try:
       await member.timeout(duration, reason=reason)
       await interaction.response.send_message(f"successfully muted {member.mention} for {time_str}.", ephemeral=True)
   except Exception as e:
       await interaction.response.send_message(f"failed to mute user: {e}", ephemeral=True)

@bot.tree.command(name="ban", description="ban a user from the server with anti-mass ban protection")
@app_commands.describe(member="user to ban", reason="reason for ban")
async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "no reason provided"):
   trial_role = interaction.guild.get_role(TRIAL_MOD_ROLE_ID)
   is_trial_mod = trial_role in interaction.user.roles if trial_role else False

   if is_trial_mod and not interaction.user.guild_permissions.administrator:
       approval_channel = interaction.guild.get_channel(saved_channels["approval_channel_id"])
       if approval_channel:
           embed = discord.Embed(
               title="trial mod action approval required",
               description=f"**trial mod:** {interaction.user.mention}\n**action:** ban\n**target:** {member.mention}\n**reason:** {reason}",
               color=0xffaa00
           )
           view = TrialModApprovalView(interaction.user.id, "ban", member.id, reason)
           await approval_channel.send(embed=embed, view=view)
       await interaction.response.send_message("your ban request has been sent to staff approval.", ephemeral=True)
       return

   if not interaction.user.guild_permissions.ban_members:
       await interaction.response.send_message("you do not have permission to ban members.", ephemeral=True)
       return

   # Anti-mass ban check
   user_id = interaction.user.id
   current_time = time.time()
   if user_id not in ban_tracker:
       ban_tracker[user_id] = []
   
   ban_tracker[user_id].append(current_time)
   ban_tracker[user_id] = [t for t in ban_tracker[user_id] if current_time - t < 10]

   if len(ban_tracker[user_id]) >= 3:
       approval_channel = interaction.guild.get_channel(saved_channels["approval_channel_id"])
       if approval_channel:
           await approval_channel.send(f"⚠️ **SECURITY ALERT:** Moderator {interaction.user.mention} is mass-banning users! Action has been intercepted.")
       try:
           await interaction.user.remove_roles(*(interaction.user.roles[1:]))
           await interaction.response.send_message("mass banning detected. your roles have been stripped.", ephemeral=True)
       except:
           await interaction.response.send_message("mass banning detected, but failed to strip roles.", ephemeral=True)
       return

   try:
       await member.ban(reason=reason)
       await interaction.response.send_message(f"successfully banned {member.mention}.", ephemeral=True)
   except Exception as e:
       await interaction.response.send_message(f"failed to ban user: {e}", ephemeral=True)

@bot.tree.command(name="echo", description="send an echoed message")
@app_commands.describe(message="text to send", channel="channel to send message in")
async def echo_slash(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
   if not interaction.user.guild_permissions.manage_messages:
       await interaction.response.send_message("you do not have permission to use echo.", ephemeral=True)
       return
   target = channel or interaction.channel
   await target.send(message)
   await interaction.response.send_message(f"sent message to {target.mention}", ephemeral=True)

@bot.tree.command(name="dm", description="direct message a user through the bot")
@app_commands.describe(member="user to DM", text="message text")
async def dm_slash(interaction: discord.Interaction, member: discord.Member, text: str):
   if not interaction.user.guild_permissions.administrator:
       await interaction.response.send_message("you do not have permission to DM users.", ephemeral=True)
       return
   try:
       await member.send(text)
       await interaction.response.send_message(f"successfully sent DM to {member.mention}.", ephemeral=True)
   except Exception as e:
       await interaction.response.send_message(f"failed to DM user: {e}", ephemeral=True)

bot.run(os.getenv("TOKEN"))
