import discord
from discord.ext import commands
import os
from config import key 
from config import TOKEN
from Data.databasehadler import DatabaseHandler

database_handler = DatabaseHandler("pathfinder_data.db", key)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Charger les extensions (cogs)
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    await bot.sync_commands()


# Fonction pour charger automatiquement les cogs
def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.{filename[:-3]}")

load_cogs()
bot.run(TOKEN)
