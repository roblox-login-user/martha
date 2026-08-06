import discord
from discord.ext import commands
import os

# 1. SETUP BOTH COMMAND TYPES IN ONE AREA
intents = discord.Intents.default()
intents.message_content = True

# We use commands.Bot so we can mix prefix commands and slash commands easily
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

# 3. STARTUP LOGS & SYNCING
@bot.event
async def on_ready():
    print(f"logged in as {bot.user}".lower())
    try:
        # This registers your slash commands to Discord's servers automatically
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"failed to sync commands: {e}")

# 4. PREFIX COMMANDS AREA (Like your ,rules command)
@bot.command(name="rules")
async def rules_command(ctx):
    # Safely delete the user's trigger message (e.g. delete the ",rules" text)
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.HTTPException):
        pass

    embed = discord.Embed(
        title="RULES",
        description=(
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

# 5. SLASH COMMANDS AREA (Like your /verify command)
@bot.tree.command(name="verify", description="sends the verification panel")
async def verify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="VERIFICATION",
        description="click the button below to verify yourself and gain access to the server.",
        color=0x2b2d31
    )
    await interaction.response.send_message(embed=embed, view=VerifyView())

# 6. RUN THE BOT SECURELY
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
