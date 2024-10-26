# Made by RoSwagger Developers at roswagger.com
# Visit our creator program here for unrestricted access for free at
# discord.roswagger.com

import discord
from discord.ext import commands
import requests
import time
from datetime import datetime, timezone
from dateutil import parser
from dateutil.relativedelta import relativedelta
from roswagger import Swagger
import json

with open('config.json', 'r') as cf:
    config = json.load(cf)

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())
    
def tostamp(ya):
    date = parser.parse(ya)
    return f"<t:{int(date.timestamp())}:R>"

def acc_age(ya2):
    creation_date = parser.parse(ya2)
    days_old = (datetime.now(timezone.utc) - creation_date).days
    return f"{days_old:,} days"  

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="roswagger.com"))
    print(f'{bot.user} is on')

@bot.command(name='u')
async def user_info(ctx, username: str):
    processing_embed = discord.Embed(description="> <a:loademoji:1299616656259153930> We are processing your request, please wait...", color=0xd3d3d3)
    processing_message = await ctx.send(embed=processing_embed)

    data = Swagger('all', username)

    if data.get('isBanned'):
        invalid_embed = discord.Embed(description="> :x: The account you are trying to lookup is banned.", color=0xd3d3d3)
        await processing_message.edit(embed=invalid_embed)
        return

    if "error" in data:
        error_embed = discord.Embed(description="> :x: Invalid username or User ID", color=0xd3d3d3)
        await processing_message.edit(embed=error_embed)
        return

    account_status = "Banned" if data.get('isBanned') else "Active"
    account_status_color = 0xff0000 if account_status == "Banned" else 0x00ff00

    creation_date_timestamp = tostamp(data['creationDate'])
    last_online_timestamp = tostamp(data['lastOnline'])
    account_age = acc_age(data['creationDate'])

    embed = discord.Embed(title=f"{data['username'].capitalize()}", url=f"https://roblox.com/users/{data['userId']}", color=0xd3d3d3)
    embed.add_field(name="ID", value=data['userId'], inline=True)

    verified_status = "Yes" if data['verified'] else "No"
    embed.add_field(name="Verified", value=verified_status, inline=True)

    inventory_status = "Private" if data.get('private') else "Public"
    embed.add_field(name="Inventory", value=inventory_status, inline=True)

    embed.add_field(name="Account Age", value=account_age, inline=True)
    embed.add_field(name="Creation", value=creation_date_timestamp, inline=True)
    embed.add_field(name="Last Online", value=last_online_timestamp, inline=True)
    embed.add_field(name="Last Location", value=data['lastLocation'], inline=True)

    rap_value = data.get('rap')
    value_value = data.get('value')

    if inventory_status == "Private":
        rap_link = f"[Private](https://rolimons.com/player/{data['userId']})"
        value_link = f"[Private](https://rolimons.com/player/{data['userId']})"
    else:
        rap_link = f"[{rap_value:,}](https://rolimons.com/player/{data['userId']})" if rap_value else "0"
        value_link = f"[{value_value:,}](https://rolimons.com/player/{data['userId']})" if value_value else "0"

    embed.add_field(name="RAP", value=rap_link, inline=True)
    embed.add_field(name="Value", value=value_link, inline=True)

    if data['description']:
        embed.add_field(name="Description", value=data['description'], inline=False)

    embed.set_thumbnail(url=data['thumbnails']['avatarThumbnail'])
    embed.set_footer(text=f"Powered by https://roswagger.com", icon_url="https://media.discordapp.net/attachments/1299619462470832139/1299620068979904552/roswagger.png?ex=671ddd02&is=671c8b82&hm=91383a6dd62aa74dce304b42f6c3271dda2c515f0c426df98216f45f737a453c&=&format=webp&quality=lossless&width=242&height=242")

    await processing_message.edit(embed=embed)



bot.run(config['botToken'])
