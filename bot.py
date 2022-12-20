"""
    Name: FastDL query bot by koen
    Author: koen
    Description: A discord bot written in discord.py for players to query map download links from FastDL URL
    Version: 0.1
    URL: https://github.com/notkoen
"""

import os
import sys

from dotenv import load_dotenv

import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

# Specify global variables
FASTDL_SET = True
ALTFASTDL_SET = True
RPACK = True

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
if TOKEN is None:
    sys.Exit("Error! No bot token specified!")

FASTDL = os.getenv('FASTDL_URL')
if FASTDL is None:
    print("Warning! No fastDL URL specified. /map and /fastdl feature will be disabled")
    FASTDL_SET = False

ALTFASTDL = os.getenv("FASTDL_URL2")
if ALTFASTDL is None:
    print("Warning! Alternate fastDL URL not specified. /map and /fastdl will only show one link if applicable")
    ALTFASTDL_SET = False

RESOURCEPACK = os.getenv("RESOURCE_PACK_URL")
if RESOURCEPACK is None:
    print("Warning! No resource pack URL specified. /resourcepack will be disabled")
    RPACK = False

# Bot ready event
@client.event
async def on_ready():
    await tree.sync()
    print("FastDL Query Bot (v0.1) is ready!") # Included version number here

# Discord command for retrieving links directly to both main and alternate FastDL links
@tree.command(name = "fastdl", description = "Get FastDL link(s)")
async def fastdl(interaction: discord.Interaction):
    if not FASTDL_SET and not ALTFASTDL_SET:
        await interaction.response.send_message("Command is disabled as no FastDL link was set!")
        return
    if FASTDL_SET:
        if ALTFASTDL_SET:
            await interaction.response.send_message("Main FastDL:\n" + FASTDL + "\n\nBackup FastDL:\n" + ALTFASTDL)
        else:
            await interaction.response.send_message("Main FastDL:\n" + FASTDL)

# Discord command for retrieving resource pack link
@tree.command(name = "resourcepack", description = "Get resource pack link")
async def resourcepack(interaction: discord.Interaction):
    if not RPACK:
        await interaction.response.send_message("Command is disabled as no resource pack link was set")
    else:
        await interaction.response.send_message("Resource pack:\n" + RESOURCEPACK)

# Discord command for obtaining map download link
@tree.command(name = "map", description = "Get map download link")
@app_commands.describe(map_name = "Exact map name")
@app_commands.describe(big_map = "Over 150mb")
async def downloadmap(interaction: discord.Interaction, map_name: str, big_map: bool):
    if not FASTDL_SET and not ALTFASTDL_SET:
        await interaction.response.send_message("FastDL link not set! No download link URL available")
        return
    match big_map:
        case True:
            if ALTFASTDL_SET:
                await interaction.response.send_message("Download link:\n" + FASTDL + map_name + ".bsp\n\nBackup download link:\n" + ALTFASTDL + map_name + ".bsp\n\n*If both links don't work, try setting `big_map` to false!*")
            else:
                await interaction.response.send_message("Download link:\n" + FASTDL + map_name + ".bsp\n\n*If the link doesn't work, try setting `big_map` to false!*")
        case False:
            if ALTFASTDL_SET:
                await interaction.response.send_message("Download link: \n" + FASTDL + map_name + ".bsp.bz2\n\nBackup download link:\n" + ALTFASTDL + map_name + ".bsp.bz2\n\n*If both links don't work, try setting `big_map` to true!*")
            else:
                await interaction.response.send_message("Download link: \n" + FASTDL + map_name + ".bsp.bz2\n\n*If the link doesn't work, try setting `big_map` to true!*")

# Start up the bot
try:
    print("Starting up the bot")
    client.run(TOKEN)
except discord.errors.LoginFailure:
    sys.Exit("ERROR! Invalid bot token specified, aborting!")
except Exception as e:
    sys.Exit("ERROR! Bot crashed...")