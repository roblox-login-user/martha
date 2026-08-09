import io
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

SPECIAL_USER_ID = 000000000000000000  # waiting for user/id

user_warns = {}
warned_messages = set()

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
    "𓈒  ✿  **extra** :: \n\n"
    "
