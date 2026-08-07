import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix=",", intents=intents)

saved_channels = {
    "verify_channel_id": None,
    "welcome_channel_id": None,
    "boost_channel_id": None,
    "intro_channel_id": None,
    "intro_message_id": None
}

user_warns = {}

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

@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)
    print(f"logged in as {bot.user}".lower())

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
            ".   . .   ˚ . .  .   ˚ .     . .   ˚ . ⁠\n"
            f", ⟡ ‎﹒ ⟢﹒‎﹒**welc**… {target_user.mention}! ❞ ‎﹒\n"
            "⁠♫・<#1534369682331799552> ⁠⭓<#1534369268748128328> ‎﹒ ❀\n"
            "𝆕  ◟ , enjoy your stay! "
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
            "   𝅄 receiving 3 formal staff warnings results in an automatic kick from the server.\n\n"
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

@bot.event
async def on_member_join(member):
    channel_id = saved_channels["welcome_channel_id"]
    channel = member.guild.get_channel(channel_id) if channel_id else discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(embed=get_decorated_welcome_embed(member))

@bot.event
async def on_message(message):
    if message.author.bot:
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

    if saved_channels["intro_channel_id"] and message.channel.id == saved_channels["intro_channel_id"]:
        try:
            old_msg_id = saved_channels["intro_message_id"]
            if old_msg_id:
                try:
                    old_msg = await message.channel.fetch_message(old_msg_id)
                    await old_msg.delete()
                except:
                    pass
            
            new_msg = await message.channel.send(content=intro_copy_text, embed=get_decorated_intro_embed())
            saved_channels["intro_message_id"] = new_msg.id
        except:
            pass

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

@bot.command(name="welcome")
async def welcome_setup_command(ctx):
    try: await ctx.message.delete()
    except: pass
    saved_channels["welcome_channel_id"] = ctx.channel.id
    await ctx.send(embed=get_decorated_welcome_embed(ctx.author))

@bot.command(name="boost")
async def boost_setup_command(ctx):
    try: await ctx.message.delete()
    except: pass
    saved_channels["boost_channel_id"] = ctx.channel.id
    await ctx.send(embed=get_decorated_boost_embed(ctx.author))

@bot.command(name="intro")
async def intro_setup_command(ctx):
    try: 
        await ctx.message.delete()
    except: 
        pass
    
    saved_channels["intro_channel_id"] = ctx.channel.id
    
    if saved_channels["intro_message_id"]:
        try:
            old_msg = await ctx.channel.fetch_message(saved_channels["intro_message_id"])
            await old_msg.delete()
        except:
            pass

    msg = await ctx.send(content=intro_copy_text, embed=get_decorated_intro_embed())
    saved_channels["intro_message_id"] = msg.id

@bot.command(name="gif")
async def gif_command(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    target_message = None

    if ctx.message.reference and ctx.message.reference.message_id:
        try:
            target_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except:
            pass

    if not target_message:
        async for msg in ctx.channel.history(limit=10):
            if msg.id != ctx.message.id and (msg.attachments or msg.embeds):
                target_message = msg
                break

    if not target_message:
        await ctx.send("no recent photo or video found to turn into a gif.", delete_after=5)
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
        await ctx.send("the target message does not contain a valid file.", delete_after=5)
        return

    if file_url.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm")):
        await ctx.send(f"converted to gif:\n{file_url}")
    else:
        await ctx.send(f"found the file, here is the link:\n{file_url}")

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
    
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("channel has been locked.", delete_after=5)

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
    ban_reason = f"banned by {interaction.user}"
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
            await user.kick(reason="reached 3 warnings")
            await interaction.response.send_message(f"warned {user.mention} ({count}/3). they reached 3 warnings and have been automatically kicked.", ephemeral=True)
            user_warns[uid] = 0
            return
        except Exception as e:
            pass

    await interaction.response.send_message(f"warned {user.mention}. current warnings: {count}/3.", ephemeral=True)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
