import discord
from discord.ext import commands
import os

# 1. SETUP INTENTS & PREFIX BOT ONLY
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix=",", intents=intents)

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
    print(f"logged in as {bot.user}".lower())

# Helper function to generate your decorated verification panel with your custom GIF
def get_decorated_verify_embed():
    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    verify here!    𝅄          ۪   ݁   𓈒",
        description="‎\n‎ ㅤ ۪ 𝅄 press the button below to gain access to the rest of the server !",
        color=0x2b2d31
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535053228784357447/41E85482-D59D-4342-ACDB-F323F94F743B.gif?ex=6a765d39&is=6a750bb9&hm=2e10bf1bcf4be571b00387370d5a95e8213dd3045bcc90f054fc3a16210b78d5&")
    return embed

# Helper function to generate your decorated welcome template with your custom GIF
def get_decorated_welcome_embed(target_user):
    embed = discord.Embed(
        description=(
            ".　　 . . 　 ˚　. .　　. 　 ˚　.　　　　 . . 　 ˚　. ⁠\n"
            f", ⟡ ‎﹒ ⟢﹒‎﹒**welc**… {target_user.mention}! ❞ ‎﹒\n"
            "⁠♫・<#1534369682331799552> ⁠⭓<#1534369268748128328> ‎﹒ ❀\n"
            "𝆕  ◟ , enjoy your stay! "
        ),
        color=0x2b2d31
    )
    embed.set_author(name="𓈒    ✿    new arrival!    𝅄", icon_url=target_user.display_avatar.url)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535052679078744084/78700BDC-447A-4AF3-A5C5-508BABB43DEB.gif?ex=6a765cb6&is=6a750b36&hm=fb2d433ba29225b888b70f977c512ffc37605343f28dea328f18a5511034463f&")
    return embed

# 4. AUTOMATED CUTE WELCOME MESSAGE (Triggers when anyone joins)
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel is not None:
        embed = get_decorated_welcome_embed(member)
        await channel.send(embed=embed)

# 5. PREFIX COMMANDS AREA
@bot.command(name="rules")
async def rules_command(ctx):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.HTTPException):
        pass

    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    server rules!    𝅄          ۪   ݁   𓈒",
        description=(
            "‎\n"
            "• **No Slurs:** Please refrain from using racist and homophobic slurs.\n\n"
            "• **Follow Guidelines:** Adhere to Discord's Terms of Service and keep the community safe.\n\n"
            "• **No NSFW or Toxicity:** Strictly no NSFW content, e-dating, or toxic behavior.\n\n"
            "• **Use Common Sense:** Be careful with your words. No telling others to harm themselves.\n\n"
            "• **No Public Drama:** Take arguments to DMs. Ping <@&1534625978884690061> <@&1534626036556365824> if it escalates and won't move to DMs so staff can monitor :))\n\n"
            "• **Privacy & Safety:** Avoid sharing personal information such as home addresses or IP addresses. Doxxing is strictly prohibited.\n\n"
            "• **No Spam or Self-Promotion:** Refrain from spamming and unauthorized advertising. Create a ticket to talk to staff if you want to promote.\n\n"
            "• **Consequences:** Violating any rule may result in a mute, kick, or ban. Appeals and readmissions can be discussed with staff."
        ),
        color=0x2b2d31
    )
    await ctx.send(embed=embed)

@bot.command(name="verify")
async def verify_prefix_command(ctx):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.HTTPException):
        pass

    embed = get_decorated_verify_embed()
    await ctx.send(embed=embed, view=VerifyView())

@bot.command(name="welcome")
async def manual_welcome_test(ctx):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.HTTPException):
        pass

    embed = get_decorated_welcome_embed(ctx.author)
    await ctx.send(embed=embed)

# NEW PREFIX COMMAND FOR SERVER BOOSTERS
@bot.command(name="boost")
async def boost_command(ctx):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.HTTPException):
        pass

    embed = discord.Embed(
        title="‎ ㅤ         𓈒    ✿    thank you for boosting!    𝅄          ۪   ݁   𓈒",
        description=f"‎\n‎ ㅤ ۪ 𝅄 tysm for boosting the server {ctx.author.mention}! we appreciate your support!",
        color=0x2b2d31
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1534974589568942221/1535053258593407048/F78E6667-7B31-4736-8E4D-9337BDAF3FD0.gif?ex=6a765d40&is=6a750bc0&hm=3557e5a996b0f4584c6e00ade1d6fedd1ad9460fe27d8a0f16cea8b6a1157a36&")
    await ctx.send(embed=embed)

# 6. RUN THE BOT SECURELY
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
