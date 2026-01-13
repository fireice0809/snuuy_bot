from discord.ext import tasks, commands
import discord
import requests
import json
import random
import io
import os
import pathlib
import pytz
import datetime
from utils.api import CF_API, CF_USER_API
from pathlib import Path

timezone_gmt7 = pytz.timezone('Asia/Ho_Chi_Minh') 
target_time = datetime.time(hour=7, minute=0, second=0, tzinfo=timezone_gmt7)

class CP(commands.Cog, name="cp"):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.daily_problem.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        self.daily_problem.start()
        self.base_url_daily = None

    @commands.group(name="cp", invoke_without_command=True)
    async def cp(self, ctx):
        """The main moderation command group."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed.")

    @tasks.loop(time=target_time)
    async def daily_problem(self):
        channel_id = 1447187754478997524
        channel = self.bot.get_channel(channel_id)
        await self.rando_daily(channel, 1200, 2000)

    async def rando_daily(self, ctx, *rating_bound):
        if (len(rating_bound) == 1):
            upper_rating = 9999
            lower_rating = int(rating_bound[0])
        elif (len(rating_bound) == 0):
            upper_rating = 9999
            lower_rating = 0
        else:
            upper_rating = int(rating_bound[1])
            lower_rating = int(rating_bound[0])

        probrem_list = CF_API()
        problem_list_file = probrem_list.fetch()
        problem_list_dict = json.loads(problem_list_file)
        problem_list_list = []

        for i in problem_list_dict:
            rate = i.get("rating", -1)
            if (int(rate) <= int(upper_rating) and int(rate) >= int(lower_rating)):
                problem_list_list.append([i["contestId"], i["index"]])


        rand_pos = random.randint(0, len(problem_list_list))
        
        self.base_url_daily = "https://codeforces.com/contest/"
        self.base_url_daily += str(problem_list_list[rand_pos][0])
        self.base_url_daily += "/problem/"
        self.base_url_daily += str(problem_list_list[rand_pos][1])
        await ctx.send(self.base_url_daily)
        #return base_url

    @cp.command(name="daily")
    async def daily(self, ctx):
        if (self.base_url_daily != None):
            await ctx.send("Daily problem: " + self.base_url_daily)
        else:
            await ctx.send("Daily problem set to: ")
            await self.rando_daily(ctx, 1200, 2000)
        

    @daily_problem.before_loop
    async def before_dail(self):    
        await self.bot.wait_until_ready()
    
    @cp.command(name="problemlist")
    async def problemlist(self, ctx):
        probrem_list = CF_API()
        problem_list_file = probrem_list.fetch()
        problem_list_file_bytes = problem_list_file.encode('utf-8')
        file_object = io.BytesIO(problem_list_file_bytes)
        discord_file = discord.File(file_object, filename="data.json")
        await ctx.send(file=discord_file)      

    @cp.command(name="random")
    async def random(self, ctx, *rating_bound):
        if (len(rating_bound) == 1):
            upper_rating = 9999
            lower_rating = int(rating_bound[0])
        elif (len(rating_bound) == 0):
            upper_rating = 9999
            lower_rating = 0
        else:
            upper_rating = int(rating_bound[1])
            lower_rating = int(rating_bound[0])

        probrem_list = CF_API()
        problem_list_file = probrem_list.fetch()
        problem_list_dict = json.loads(problem_list_file)
        problem_list_list = []

        for i in problem_list_dict:
            rate = i.get("rating", -1)
            if (int(rate) <= int(upper_rating) and int(rate) >= int(lower_rating)):
                problem_list_list.append([i["contestId"], i["index"]])


        rand_pos = random.randint(0, len(problem_list_list))
        
        base_url = "https://codeforces.com/contest/"
        base_url += str(problem_list_list[rand_pos][0])
        base_url += "/problem/"
        base_url += str(problem_list_list[rand_pos][1])
        await ctx.send(base_url)
        return base_url
    
    @cp.command(name="verify")
    async def verify(self, ctx, handle):
        file_path = Path(__file__).parent.parent / 'text' / 'user_dtb.json'

        with open(file_path, 'r') as file:
            user_dict = json.load(file)
        #print(user_dict)
        user_id = str(ctx.author.id)
        print(user_id, user_dict.get(user_id))
        if user_id in user_dict:
            await ctx.send("You have already linked this Discord account to a Codeforces handle. Please contact the bot owner (mewhensunny) if you want to link your Discord account to another Codeforces handle")
            return
        
        Verifier = CF_USER_API(ctx.author.id, handle)
        if Verifier.verify() == True:
            await ctx.send("Account successfully linked! Your Codeforces handle is now " + handle + "!")
            user_dict[ctx.author.id] = handle
            json_string = json.dumps(user_dict, indent=4)
            with open(file_path, 'w') as file:
                file.write(json_string)
        else:
            await ctx.send("Please submit a Compilation Error submission to this problem: " + "https://codeforces.com/contest/809/problem/A")
            await ctx.send("After successfully submitted please wait for 20 seconds then type this command again")


   
async def setup(bot) -> None:
    await bot.add_cog(CP(bot))