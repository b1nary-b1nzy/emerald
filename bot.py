import discord
from discord.ext import commands
import aiohttp
import json
import random
import os
import io
import asyncio

client = commands.Bot(command_prefix='e.', owner_id=437150834888015872)
client.session = aiohttp.ClientSession()
client.commands_run = 0
client.load_extension('cogs.Information')
if 'TOKEN' in os.environ:
  heroku = True
  TOKEN = os.environ['TOKEN']

@client.event
async def on_ready():
  print('Logged in as:')
  print(client.user.name)
  print(client.user.id)
  while True:
    await client.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name='for e.help!'))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name=f'to {len(client.guilds)} guilds!'))
    await asyncio.sleep(10)
    
client.run(os.environ['TOKEN'])
