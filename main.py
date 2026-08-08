import discord
from discord import app_commands
from discord.ext import commands
import os

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
    "mod_log_channel_id": 1534974589568942221
}

user_warns = {}

blacklisted_words = [
    "chink", "nigger", "nigga", "tranny", "faggot", "retard",
    "fag", "coon", "spic", "kike", "retarded", "dyke", "gook", "wetback"
]

intro_copy_text = (
    "```text\n"
    "‎ ㅤ         𓈒    ✿    introduction template    𝅄          ۪   ݁   𓈒\n"
    "‎\n"
    "𓈒  ✿  **name** :: \n\n"
    "𓈒  ✿  **age / pronouns** :: \n\n"
    "𓈒  ✿  **hobbies** :: \n\n"
    "𓈒  ✿  **favorite thing** :: \n\n"
    "𓈒  ✿  **extra** :: \n"
    "```"
)

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

class ModActionView(discord.ui.View):
    def __init__(self, target_user_id: int):
        super().__init__(timeout=None)
        self.target_user_id = target_user_id

    @discord.ui.button(label="warn user", style=discord.ButtonStyle.red, custom_id="mod_warn_button")
    async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
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
                await interaction.response.send_message(f"successfully warned <@{self.target_user_id}> ({count}/3). they reached 3 warnings and have been automatically banned.", ephemeral=True)
                return
            except:
                pass

        await interaction.response.send_message(f"successfully warned <@{self.target_user_id}>. current warnings: {count}/3.", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    try:
        await bot.tree.sync()
        print("slash commands synced successfully.")
    except Exception as e:
        print(f"failed to sync slash commands: {e}")
    print(f"logged in as {bot.user}".lower())

@bot.event
async def on_member_join(member):
    channel_id = saved_channels["welcome_channel_id"]
    channel = member.guild.get_channel(channel_id) if channel_id else discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(embed=get_decorated_welcome_embed(member))

def get_decorated_verify_embed():
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    verify here!    𝅄          ۪   ݁   𓈒",
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

def get_decorated_boost_embed(target_user):
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    thank you for boosting!    𝅄          ۪   ݁   𓈒",
        description=f"‎\n‎ ㅤ ۪ 𝅄 tysm for boosting the server {target_user.mention}! we appreciate your support!",
        color=0x2b2d31
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535053258593407048/F78E6667-7B31-4736-8E4D-9337BDAF3FD0.gif?ex=6a765d40&is=6a750bc0&hm=3557e5a996b0f4584c6e00ade1d6fedd1ad9460fe27d8a0f16cea8b6a1157a36&")
    return embed

def get_decorated_rules_embed():
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    server rules!    𝅄          ۪   ݁   𓈒",
        description=(
            "‎\n"
            "𓈒  ✿  **no slurs**\n"
            "   𝅄 please keep our chat safe and kind. racist, homophobic, or hate-driven language is strictly prohibited.\n\n"
            "𓈒  ✿  **follow guidelines**\n"
            "   𝅄 please adhere to discord's formal terms of service to safeguard our community atmosphere.\n\n"
            "𓈒  ✿  **no nsfw or toxicity**\n"
            "   𝅄 avoid any explicit content, e-dating behaviors, or general toxicity inside public text areas.\n\n"
            "𓈒  ✿  **use common sense**\n"
            "   𝅄 think before you speak. malicious language, severe harassment, or encouraging self-harm is not tolerated.\n\n"
            "𓈒  ✿  **no public drama**\n"
            "   𝅄 keep interpersonal arguments or disagreements strictly inside private message chats. if an issue escalates or requires dynamic moderation, please immediately alert <@&1534625978884690061> or <@&1534626036556365824> so our staff team can assess the room.\n\n"
            "𓈒  ✿  **privacy & safety**\n"
            "   𝅄 never share sensitive real-world info like IP or home addresses. malicious doxxing triggers an unappealable ban.\n\n"
            "𓈒  ✿  **no spam or promotion**\n"
            "   𝅄 do not spam text walls or link advertisements without permissions. please open a staff ticket if you wish to apply for promotional privileges.\n\n"
            "𓈒  ✿  **3 warn system**\n"
            "   𝅄 receiving 3 formal staff warnings results in an automatic ban from the server.\n\n"
            "𓈒  ✿  **consequences**\n"
            "   𝅄 infractions result in account mutes, kicks, or server bans. you may coordinate with staff privately regarding appeal requests."
        ),
        color=0x2b2d31
    )
    return embed

def get_decorated_intro_embed():
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    introduction template    𝅄          ۪   ݁   𓈒",
        description="use the copy button on the text above to easily copy the template on mobile!",
        color=0x2b2d31
    )
    return embed

def get_decorated_commands_embed():
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    bot commands list    𝅄          ۪   ݁   𓈒",
        description=(
            "‎\n"
            "𓈒  ✿  **general commands**\n"
            "   𝅄 `,ping` or `/ping` :: check bot latency\n"
            "   𝅄 `,rules` or `/rules` :: display server rules embed\n"
            "   𝅄 `,verify` or `/verify` :: send verification panel button\n"
            "   𝅄 `,intro` or `/intro` :: send introduction copy template\n"
            "   𝅄 `,gif` or `/gif` :: convert latest file/video in chat to a gif link\n"
            "   𝅄 `/membercount` :: show total members, humans, and bots\n\n"
            "𓈒  ✿  **moderation commands**\n"
            "   𝅄 `,c [amount]` or `/c` :: clear messages in channel\n"
            "   𝅄 `,lock` or `/lock` :: lock current channel for verified role\n"
            "   𝅄 `/warn [user] [reason]` :: warn a user (auto-bans at 3 warns)\n"
            "   𝅄 `/ban [user] [time] [reason]` :: ban a user from the server\n\n"
            "𓈒  ✿  **utility commands**\n"
            "   𝅄 `/echo [message] [channel]` :: send an echoed message\n"
            "   𝅄 `/dm [user] [text]` :: direct message a user through the bot\n"
            "   𝅄 `/status [type]` :: change bot online status or stream"
        ),
        color=0x2b2d31
    )
    return embed

def get_decorated_automod_embed(target_user, offending_message):
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    automod alert :: slur detected    𝅄          ۪   ݁   𓈒",
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
        channel = message.guild.get_channel(channel_id) if channel_id else message.channel
        
        if channel:
            await channel.send(embed=get_decorated_boost_embed(message.author))

    await bot.process_commands(message)

@bot.command(name="ping")
async def ping_command(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    latency = round(bot.latency * 1000)
    await ctx.send(f"pong! {latency}ms")

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

@bot.command(name="intro")
async def intro_setup_command(ctx):
    try: 
        await ctx.message.delete()
    except: 
        pass
    
    await ctx.send(content=intro_copy_text, embed=get_decorated_intro_embed())

@bot.command(name="gif")
async def gif_command(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    target_message = None
    async for msg in ctx.channel.history(limit=15):
        if msg.id != ctx.message.id and (msg.attachments or msg.embeds):
            target_message = msg
            break

    if not target_message:
        await ctx.send("no recent file or video found in this channel to convert.", delete_after=5)
        return

    file_url = None
    if target_message.attachments:
        file_url = target_message.attachments[0].url
    elif target_message.embeds:
        for embed in target_message.embeds:
            if embed.image and embed.image.url:
                file_url = embed.image.url
                break
            elif embed.thumbnail and embed.thumbnail.url:
                file_url = embed.thumbnail.url
                break

    if not file_url:
        await ctx.send("the latest message does not contain a valid file.", delete_after=5)
        return

    await ctx.send(f"converted to gif:\n{file_url}")

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
async def cmds_slash(interaction: discord.Interaction):
    await interaction.response.send_message(embed=get_decorated_commands_embed(), ephemeral=True)

@bot.tree.command(name="status", description="change the bot's online status")
@app_commands.describe(type="online, idle, dnd, invisible, or streaming")
@app_commands.choices(type=[
    app_commands.Choice(name="online", value="online"),
    app_commands.Choice(name="idle", value="idle"),
    app_commands.Choice(name="dnd", value="dnd"),
    app_commands.Choice(name="invisible", value="invisible"),
    app_commands.Choice(name="streaming", value="streaming")
])
async def status(interaction: discord.Interaction, type: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("you do not have permission to use this command.", ephemeral=True)
        return

    status_types = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
        "invisible": discord.Status.invisible,
        "streaming": discord.Status.online
    }

    if type == "streaming":
        activity = discord.Streaming(name="custom stream", url="https://www.twitch.tv/discord")
        await bot.change_presence(status=discord.Status.online, activity=activity)
    else:
        await bot.change_presence(status=status_types.get(type, discord.Status.online), activity=None)

    await interaction.response.send_message(f"successfully changed bot status to **{type}**.", ephemeral=True)

@bot.tree.command(name="membercount", description="show the total members and bots in the server")
async def membercount(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    await guild.chunk(cache=True)
    
    total_members = guild.member_count
    humans = sum(not m.bot for m in guild.members)
    bots = sum(m.bot for m in guild.members)

    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    member count    𝅄          ۪   ݁   𓈒",
        description=(
            f"𓈒  ✿  **total members** :: {total_members}\n"
            f"𓈒  ✿  **humans** :: {humans}\n"
            f"𓈒  ✿  **bots** :: {bots}"
        ),
        color=0x2b2d31
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="echo", description="echo a message to a channel")
@app_commands.describe(message="the message to echo", channel="the channel to send it in")
async def echo(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
    target_channel = channel or interaction.channel
    await target_channel.send(message)
    await interaction.response.send_message("message sent!", ephemeral=True)

@bot.tree.command(name="ban", description="ban a user from the server")
@app_commands.describe(user="the user to ban", time="optional duration", reason="reason for ban")
async def ban(interaction: discord.Interaction, user: discord.Member, time: str = None, reason: str = None):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("you do not have permission to use this command.", ephemeral=True)
        return
    ban_reason = f"banned by the staff team"
    if time:
        ban_reason += f" | duration: {time}"
    if reason:
        ban_reason += f" | reason: {reason}"
    
    try:
        await user.ban(reason=ban_reason)
        await interaction.response.send_message(f"successfully banned {user.mention}.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"failed to ban user: {e}", ephemeral=True)

@bot.tree.command(name="warn", description="warn a user")
@app_commands.describe(user="the user to warn", reason="reason for the warning")
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "no reason provided"):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("you do not have permission to use this command.", ephemeral=True)
        return
    
    uid = user.id
    user_warns[uid] = user_warns.get(uid, 0) + 1
    count = user_warns[uid]

    try:
        await user.send(f"you have been warned in **{interaction.guild.name}**.\nreason: {reason}\nwarn count: {count}/3")
    except:
        pass

    if count >= 3:
        try:
            await user.ban(reason="reached 3 warnings")
            await interaction.response.send_message(f"warned {user.mention} ({count}/3). they reached 3 warnings and have been automatically banned.", ephemeral=True)
            user_warns[uid] = 0
            return
        except Exception as e:
            pass

    await interaction.response.send_message(f"warned {user.mention}. current warnings: {count}/3.", ephemeral=True)

@bot.tree.command(name="dm", description="send a direct message to a user through the bot")
@app_commands.describe(user="the user to direct message", text="the message to send")
async def dm(interaction: discord.Interaction, user: discord.Member, text: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("you do not have permission to use this command.", ephemeral=True)
        return

    try:
        await user.send(text)
        await interaction.response.send_message(f"successfully sent a direct message to {user.mention}.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"failed to send direct message to {user.mention}. they might have dms closed.", ephemeral=True)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
