import discord
import os

intents = discord.Intents.default()
intents.message_content = True

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

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"logged in as {self.user}".lower())

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == ",rules":
            try:
                await message.delete()
            except discord.Forbidden:
                pass
            except discord.HTTPException:
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
            await message.channel.send(embed=embed)

client = MyClient()

@client.tree.command(name="verify", description="sends the verification panel")
async def verify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="VERIFICATION",
        description="click the button below to verify yourself and gain access to the server.",
        color=0x2b2d31
    )
    await interaction.response.send_message(embed=embed, view=VerifyView())

# This grabs your token securely from Bot-Hosting's environment variables
client.run(os.getenv("DISCORD_BOT_TOKEN"))
