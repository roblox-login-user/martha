import discord
from discord.ext import commands
import os

# 1. SETUP INTENTS & BOT PREFIX
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix=",", intents=intents)

saved_channels = {
    "verify_channel_id": None,
    "welcome_channel_id": None,
    "boost_channel_id": None
}

# 2. INTERACTIVE BUTTON INTERFACE
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

# 3. STARTUP LOGS
@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    print(f"logged in as {bot.user}".lower())

# Helper structures for your aesthetic templates
def get_decorated_verify_embed():
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    verify here!    𝅄          ۪   ݁   𓈒",
        description="‎\n‎ ㅤ ۪ 𝅄 press the button below to gain access to the rest of the server !",
        color=0x2b2d31
    )
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
    return embed

def get_decorated_boost_embed(target_user):
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    thank you for boosting!    𝅄          ۪   ݁   𓈒",
        description=f"‎\n‎ ㅤ ۪ 𝅄 tysm for boosting the server {target_user.mention}! we appreciate your support!",
        color=0x2b2d31
    )
    return embed

# 4. AUTOMATED EVENTS (Welcome & Boost Detect)
@bot.event
async def on_member_join(member):
    channel_id = saved_channels["welcome_channel_id"]
    channel = member.guild.get_channel(channel_id) if channel_id else discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(embed=get_decorated_welcome_embed(member))

@bot.event
async def on_message(message):
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

# 5. PREFIX COMMANDS AREA
@bot.command(name="rules")
async def rules_command(ctx):
    try: 
        await ctx.message.delete()
    except: 
        pass

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
            "𓈒  ✿  **consequences**\n"
            "   𝅄 infractions result in account mutes, kicks, or server bans. you may coordinate with staff privately regarding appeal requests."
        ),
        color=0x2b2d31
    )
    await ctx.send(embed=embed)

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

# 6. RUN THE BOT SECURELY
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
