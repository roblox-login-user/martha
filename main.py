import discord
from discord.ext import commands
import os

# 1. SETUP INTENTS & PREFIX BOT ONLY
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required to detect when new users join the server

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

# Helper function to generate your decorated verification panel
def get_decorated_verify_embed():
    return discord.Embed(
        title="‎ ㅤ         𓈒    ✿    verify here!    𝅄          ۪   ݁   𓈒",
        description="‎\n‎ ㅤ ۪ 𝅄 press the button below to gain access to the rest of the server !",
        color=0x2b2d31
    )

# 4. AUTOMATED CUTE WELCOME MESSAGE (Triggers when anyone joins)
@bot.event
async def on_member_join(member):
    # Find the welcome channel automatically in your server
    # You can name your system channel 'welcome' or 'joins'
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    
    if channel is not None:
        embed = discord.Embed(
            description=(
                ".　　 . . 　 ˚　. .　　. 　 ˚　.　　　　 . . 　 ˚　. ⁠\n"
                f", ⟡ ‎﹒ ⟢﹒‎﹒welc… {member.mention}! ❞ ‎﹒\n"
                "⁠♫・<#1534369682331799552> ⁠⭓<#1534369268748128328> ‎﹒ ❀\n"
                "𝆕  ◟ , enjoy your stay! "
            ),
            color=0x2b2d31
        )
        # Adds a cute sparkle decoration pattern to the side
        embed.set_author(name="𓈒    ✿    new arrival!    𝅄", icon_url=member.display_avatar.url)
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

# Manually test the welcome template layout inside a channel
@bot.command(name="welcome")
async def manual_welcome_test(ctx):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.HTTPException):
        pass

    embed = discord.Embed(
        description=(
            ".　　 . . 　 ˚　. .　　. 　 ˚　.　　　　 . . 　 ˚　. ⁠\n"
            f", ⟡ ‎﹒ ⟢﹒‎﹒welc… {ctx.author.mention}! ❞ ‎﹒\n"
            "⁠♫・<#1534369682331799552> ⁠⭓<#1534369268748128328> ‎﹒ ❀\n"
            "𝆕  ◟ , enjoy your stay! "
        ),
        color=0x2b2d31
    )
    embed.set_author(name="𓈒    ✿    welcome test!    𝅄", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# 6. RUN THE BOT SECURELY
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
