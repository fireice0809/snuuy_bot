from discord.ext import commands
import discord
import requests
import json
import random
import io
import os
import asyncio
from dotenv import load_dotenv
from utils.api import CF_API, CF_USER_API
from pathlib import Path

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="alo!", intents=discord.Intents.all())

rootpath = Path(__file__).resolve().parent

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            print(filename[:-3])
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print("Hello, when will Niko win a major?")
    #await channel.send("Hello, when will Niko win a major?")
    
asyncio.run(load_extensions())
bot.run(BOT_TOKEN)

