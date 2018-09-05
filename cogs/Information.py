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

def setup(client):
  client.add_cog(Information(client))
