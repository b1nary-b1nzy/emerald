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
    
  @commands.command(aliases=['ui'])
  async def userinfo(self, ctx, user: discord.Member = None):
    """Get userinfo for yourself, or someone in the guild"""
    if user is None:
      user = ctx.author
    color = ctx.author.color
    guild = ctx.message.guild
    roles = sorted(user.roles, key=lambda r: r.position)
    rolenames = ', '.join([r.name for r in roles if r != '@everyone']) or 'None'
    shared = sum(1 for m in self.client.get_all_members() if m.id == user.id)
    highrole = user.top_role.name
    if highrole == "@everyone":
      role = "N/A"

    if user.avatar_url[54:].startswith('a_'):
      avi = 'https://cdn.discordapp.com/avatars/' + user.avatar_url[35:-10]
    else:
      avi = user.avatar_url
	
        
    time = ctx.message.created_at
    desc = f'{user.name} is currently in {user.status} mode.'
    member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1
    em = discord.Embed(color=color, description=desc, timestamp=time)
    em.add_field(name=f'Username', value=f'{user.name}#{user.discriminator}')
    em.add_field(name=f'User ID', value= user.id)
    em.add_field(name=f'Servers Shared', value=f'{shared}')
    em.add_field(name=f'Highest Role', value=highrole)
    em.add_field(name=f'Account Created At', value = user.created_at.__format__('Date: **%d/%b/%Y**\nTime: **%H:%M:%S**'))
    em.add_field(name=f'Member Number', value=member_number)
    em.add_field(name=f'Joined At', value=user.joined_at.__format__('%d/%b/%Y at %H:%M:%S'))
    em.add_field(name=f'Roles', value=rolenames)
    em.set_footer(text = f"Member since: {user.joined_at.__format__('%d/%b/%Y at %H:%M:%S')}")
    em.set_thumbnail(url=avi or None)
    await ctx.send(embed=em)

  @commands.command()
  async def stats(self, ctx):
    """Get some stats for Emerald"""
    member = 0
    for i in self.client.guilds:
      for x in i.members:
        member += 1
    color = discord.Color(value=0xe212d1)
    embed = discord.Embed(color=color, title="Kala Bot Statistics")
    embed.description = "Emerald Stats"
    embed.add_field(name=f"Creator", value='BloodyPikachu#7452')
    embed.add_field(name=f"Servers", value=f"{len(self.bot.guilds)}")
    embed.add_field(name=f'Users', value=member)
    embed.add_field(name=f'Ping', value=f'{self.client.latency * 100:.4f} ms')
    embed.add_field(name=f'Version', value='0.0.1 Alpha')
    embed.add_field(name=f'Start Date', value="9/4/18")
    embed.add_field(name=f'Coding Language', value=f'Python, discord.py rewrite')
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Information(client))
