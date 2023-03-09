import discord
from discord.ext import commands
import os

import config as cfg # This is the config file

# Create the bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Load all cogs
for filename in os.listdir("./cogs"):
    # Check if the file is a python file
    if filename.endswith(".py"):
        # Load the cog
        bot.load_extension(f"cogs.{filename[:-3]}")

# When the bot is ready
@bot.event
async def on_ready():
    # Print the bot's name and ID
    print(f"{bot.user.name} is up and ready!")

bot.run(cfg.token)