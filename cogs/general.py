from discord.ext import commands
import discord
import requests
import json
import random
import io
import os
from utils.api import CF_API, CF_USER_API
from pathlib import Path


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="hello", description="nonsense")
    async def hello(self, ctx):
        await ctx.send("Niko 0 Major")   

    @commands.hybrid_command(name="userid", description="return sender's id")
    async def userid(self, ctx):
        await ctx.send(ctx.author.id)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))