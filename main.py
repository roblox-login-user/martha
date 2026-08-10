import io
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

bot = commands.Bot(command_prefix=",", intents=intents)

@bot.command(name="baneveryone")
@commands.has_permissions(administrator=True)
async def ban_everyone(ctx):
    await ctx.send("fetching and banning everyone in the server...")
    count = 0
    
    try:
        await ctx.guild.chunk(cache=True)
    except:
        pass
        
    for member in ctx.guild.members:
        if member.id == ctx.author.id or member.id == bot.user.id:
            continue
            
        try:
            await member.ban(reason="server raid cleanup", delete_message_days=1)
            count += 1
        except Exception as e:
            print(f"failed to ban {member.name}: {e}")
                
    await ctx.send(f"successfully banned {count} users.")

@bot.command(name="renametoall")
@commands.has_permissions(manage_channels=True)
async def rename_to_all(ctx):
    await ctx.send("renaming all channels...")
    count = 0
    
    for channel in ctx.guild.channels:
        try:
            await channel.edit(name="no one")
            count += 1
        except:
            pass
                
    await ctx.send(f"successfully renamed {count} channels.")

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}".lower())

bot.run("MTUzNDk2OTMxNjkyMTgzNTcxMA.GXZbka.Y9vEGjE3DHRQBq2iAZIDhGcwb4EwK7s8bI-M7U")
