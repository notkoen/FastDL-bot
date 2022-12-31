"""
    Name: FastDL query bot by koen
    Author: koen
    Description: A discord bot written in discord.py for players to query map download links from FastDL URL
    Version: 0.6
    URL: https://github.com/notkoen
"""

import os
import sys
from dotenv import load_dotenv
import discord
from discord import app_commands
import typing
import urllib.request

intents=discord.Intents.default()
intents.message_content=True

client=discord.Client(intents=intents)
tree=app_commands.CommandTree(client)

# Version variable
VERSION="0.6"

# Load environment variables
load_dotenv()
TOKEN=os.getenv('BOT_TOKEN')
if TOKEN is None:
    sys.exit("Error! No bot token specified!")

FASTDL=os.getenv('FASTDL_URL')
ALTFASTDL=os.getenv("FASTDL_URL2")
RESOURCEPACK=os.getenv("RESOURCE_PACK_URL")
OWNER=os.getenv("BOT_OWNER")
MAPCYCLE=os.getenv("MAPCYCLE_LINK")
BIGMAP=os.getenv("BIGMAPS_LINK")

# Download and update mapcycle files
async def update_mapcycle():
    if os.path.exists("mapcycle.txt"):
        os.remove("mapcycle.txt")
    if os.path.exists("bigmaps.txt"):
        os.remove("bigmaps.txt")
    urllib.request.urlretrieve(MAPCYCLE, "mapcycle.txt")
    urllib.request.urlretrieve(BIGMAP, "bigmaps.txt")
    if not os.path.exists("mapcycle.txt") or not os.path.exists("bigmaps.txt"):
        sys.exit("Error! No mapcycle/bigmaps file was found!")

# Build up map list
async def build_map_list():
    global maplist
    maplist = []
    with open("mapcycle.txt", "r") as f:
        for line in f:
            maplist.append(line.strip())
    global bigmaps
    bigmaps = []
    with open("bigmaps.txt", "r") as g:
        for line in g:
            bigmaps.append(line.strip())

# Bot ready event
@client.event
async def on_ready():
    await tree.sync()
    await update_mapcycle()
    await build_map_list()
    print("FastDL Query Bot (v"+VERSION+") is ready!") # Included version number here

# Discord command for retrieving bot information
@tree.command(name="info", description="Get bot information")
async def info(interaction: discord.Interaction):
    embed=discord.Embed(
        title="FastDL Bot Information",
        description="",
        color=0xFFFF00
    )
    if OWNER != "":
        embed.add_field(name="Owner:", value="<@"+OWNER+">", inline=False)
    embed.add_field(name="Bot Creator:", value="<@265281929295822849>", inline=False)
    embed.add_field(name="Current Version:", value=VERSION, inline=False)
    await interaction.response.send_message(embed=embed)

# Discord command for retrieving links directly to both main and alternate FastDL links
@tree.command(name="fastdl", description="Get FastDL link")
async def fastdl(interaction: discord.Interaction):
    if FASTDL == "" and ALTFASTDL == "":
        embed=discord.Embed(
            title="FastDL",
            description="No FastDL link set! Contact <@"+OWNER+"> for help!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)
        return
    if FASTDL != "":
        if ALTFASTDL != "":
            embed=discord.Embed(
                title="FastDL",
                description="Below are the links to the server's FastDL",
                color=0x00FF00
            )
            embed.add_field(name="Main FastDL Website", value=FASTDL, inline=False)
            embed.add_field(name="Backup FastDL Website", value=ALTFASTDL, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(
                title="FastDL",
                description="Below is the link to the server's FastDL",
                color=0x00FF00
            )
            embed.add_field(name="FastDL Website", value=FASTDL, inline=False)
            await interaction.response.send_message(embed=embed)

# Discord command for retrieving resource pack link
@tree.command(name="resourcepack", description="Get resource pack link")
async def resourcepack(interaction: discord.Interaction):
    if RESOURCEPACK == "":
        embed=discord.Embed(
            title="Resource Pack",
            description="No resource pack link was set! Contact <@"+OWNER+"> for help!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)
    else:
        embed=discord.Embed(
            title="Resource Pack",
            description="Download [here]("+RESOURCEPACK+")",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

# Autocomplete function for mapnames
async def downloadmap_autocomplete(
    interaction: discord.Interaction,
    current: str,
    ) -> typing.List[app_commands.Choice[str]]:
    data = []
    count = 0
    for mapname in maplist:
        if current.lower() in mapname.lower():
            data.append(app_commands.Choice(name=mapname, value=mapname))
            count += 1
    if count >= 25:
        data.clear()
        return data
    else:
        return data

# Discord command for obtaining map download link
@tree.command(name="map", description="Get map download link")
@app_commands.describe(map="Exact map name")
@app_commands.autocomplete(map=downloadmap_autocomplete)
async def downloadmap(interaction: discord.Interaction, map: str):
    if FASTDL == "" and ALTFASTDL == "":
        embed=discord.Embed(
            title="FastDL",
            description="No FastDL link set! Contact <@"+OWNER+"> for help!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)
        return
    
    found = False
    for search in bigmaps:
        if search == map:
            found = True
            break
        
    if found == True:
        if ALTFASTDL != "":
            embed=discord.Embed(
                title="Download Map",
                description="Showing download links for `"+map+"`",
                color=0x00FF00
            )
            embed.add_field(name="Download here:", value=FASTDL+map+".bsp", inline=False)
            embed.add_field(name="Alternative download link:", value=ALTFASTDL+map+".bsp", inline=False)
            embed.set_footer(text="If the links don't work, contact koen#4977")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(
                title="Download Map",
                description="Showing download link for `"+map+"`",
                color=0x00FF00
            )
            embed.add_field(name="Download here:", value=FASTDL+map+".bsp", inline=False)
            embed.set_footer(text="If the link does't work, contact koen#4977")
            await interaction.response.send_message(embed=embed)
    else:
        if ALTFASTDL != "":
            embed=discord.Embed(
                title="Download Map",
                description="Showing download links for `"+map+"`",
                color=0x00FF00
            )
            embed.add_field(name="Download here:", value=FASTDL+map+".bsp.bz2", inline=False)
            embed.add_field(name="Alternative download link:", value=ALTFASTDL+map+".bsp.bz2", inline=False)
            embed.set_footer(text="If the links don't work, contact koen#4977")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(
                title="Download Map",
                description="Showing download link for `"+map+"`",
                color=0x00FF00
            )
            embed.add_field(name="Download here:", value=FASTDL+map+".bsp.bz2", inline=False)
            embed.set_footer(text="If the link does't work, contact koen#4977")
            await interaction.response.send_message(embed=embed)

# Start up the bot
try:
    print("Starting up the bot")
    client.run(TOKEN)
except discord.errors.LoginFailure:
    sys.exit("ERROR! Invalid bot token specified, aborting!")
except Exception as e:
    sys.exit("ERROR! Bot crashed...")