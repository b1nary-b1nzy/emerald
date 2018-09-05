import discord
from discord.ext import commands
import os
import json
import aiohttp
import datetime
import time


class Information:
  """Information Commands"""
  def __init__(self, client):
    self.client = client
    self.session = session

def setup(client):
  client.add_cog(Information(client))
