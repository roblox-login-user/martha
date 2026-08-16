import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.command(name="o")
async def generate_order(ctx):
    fake_items = [
        "supreme box logo hoodie black size l",
        "rolex submariner date oystersteel",
        "rtx 4090 ti custom water cooled rig",
        "custom diamond cuban link chain 14k white gold",
        "louis vuitton keepall bandouliere 50",
        "private jet charter booking mia to jfk"
    ]
    
    fake_names = ["alex m", "jordan k", "chris v", "taylor s", "morgan d"]
    fake_addresses = [
        "742 evergreen terrace springfield",
        "1060 west addison street chicago",
        "350 5th ave new york ny",
        "221b baker street london"
    ]
    
    item = random.choice(fake_items)
    name = random.choice(fake_names)
    address = random.choice(fake_addresses)
    price = f"${random.randint(500, 15000):,}"

    embed = discord.Embed(
        title="new order panel",
        description="new fake order generated for the flex session.",
        color=0x00ffcc
    )
    embed.add_field(name="item", value=item, inline=False)
    embed.add_field(name="buyer", value=name, inline=True)
    embed.add_field(name="total price", value=price, inline=True)
    embed.add_field(name="shipping address", value=address, inline=False)
    
    view = orderbuttons()
    await ctx.send(embed=embed, view=view)

class orderbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="accept order", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("order accepted you are officially pretending to process a high roller transaction", ephemeral=True)

    @discord.ui.button(label="cancel order", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("order cancelled", ephemeral=True)

bot.run("MTUzMTQwNTYzOTI1Nzk0ODE3MA.Gzdz3j.7vymPtKf99m_Z4k6jq5yhkhmsfrgSQadn8S7fg")
