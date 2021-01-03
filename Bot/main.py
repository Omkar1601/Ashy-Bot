import discord
from discord.ext import commands
import os
import sqlite3
from Server import KeepAlive
from Constants import Constants
import asyncio
import requests


bot = commands.Bot(command_prefix = 'ashy!', owner_ids = Constants.OWNER_IDS)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('and thriving'))
    cogs = ['Cogs.Farming.QueuePoster', 'Cogs.Farming.ProgressPoster', 'Cogs.Farming.FinishedPoster', 'Cogs.Farming.Cute', 'Cogs.Farming.Custom', 'Cogs.Farming.OrderEdit', 'Cogs.Farming.OrderPage']
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f"{cog} loaded.")
        except Exception :
            print(Exception)
        
    mydb = sqlite3.connect("Farm.sqlite")
    cursor = mydb.cursor()
    cursor.execute("create table if not exists FARM(Farmer_ID text, Buyer_ID text, Card_Name text, Card_Amount text, Loc text, Price text, Farm_ID text, Farm_Type text)")
    cursor.execute("create table if not exists CUSTOM(Farmer_ID text, Custom_Msg text)")
        
    while bot.is_ready:
        requests.get("")
        await asyncio.sleep(60)
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

KeepAlive()
token= os.environ.get("TOKEN")
bot.run(token, bot = True, reconnect = True)