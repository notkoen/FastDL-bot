"""
    Name: FastDL query bot by koen
    Author: koen
    Description: A discord bot written in discord.py for players to query map download links from FastDL URL
    Version: 0.2
    URL: https://github.com/notkoen
"""

import os
import sys

from dotenv import load_dotenv

import discord
from discord import app_commands

intents=discord.Intents.default()
intents.message_content=True

client=discord.Client(intents=intents)
tree=app_commands.CommandTree(client)

# Load environment variables
load_dotenv()
TOKEN=os.getenv('BOT_TOKEN')
if TOKEN is None:
    sys.exit("Error! No bot token specified!")

FASTDL=os.getenv('FASTDL_URL')
ALTFASTDL=os.getenv("FASTDL_URL2")
RESOURCEPACK=os.getenv("RESOURCE_PACK_URL")

# Bot ready event
@client.event
async def on_ready():
    await tree.sync()
    print("FastDL Query Bot (v0.2) is ready!") # Included version number here

# Discord command for retrieving links directly to both main and alternate FastDL links
@tree.command(name="fastdl", description="Get FastDL link(s)")
async def fastdl(interaction: discord.Interaction):
    if FASTDL == "" and ALTFASTDL == "":
        embed=discord.Embed(
            title="FastDL",
            description="No FastDL link set! Contact <@265281929295822849> for help!",
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
            embed.add_field(name="Main FastDL:", value=FASTDL, inline=False)
            embed.add_field(name="Backup FastDL:", value=ALTFASTDL, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Main FastDL:\n" + FASTDL)

# Discord command for retrieving resource pack link
@tree.command(name="resourcepack", description="Get resource pack link")
async def resourcepack(interaction: discord.Interaction):
    if RESOURCEPACK == "":
        embed=discord.Embed(
            title="Resource Pack",
            description="No resource pack link was set! Contact <@265281929295822849> for help!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)
    else:
        embed=discord.Embed(
            title="Resource Pack",
            description=RESOURCEPACK,
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

# Discord command for obtaining map download link
@tree.command(name="map", description="Get map download link")
@app_commands.describe(map_name="Exact map name")
@app_commands.describe(big_map="Over 150mb")
async def downloadmap(interaction: discord.Interaction, map_name: str, big_map: bool):
    if FASTDL == "" and ALTFASTDL == "":
        embed=discord.Embed(
            title="FastDL",
            description="No FastDL link set! Contact <@265281929295822849> for help!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)
        return
    match big_map:
        case True:
            if ALTFASTDL != "":
                embed=discord.Embed(
                    title="Map Download Link",
                    description="`" + map_name + "`",
                    color=0x00FF00
                )
                embed.add_field(name="Download Link:", value=FASTDL + map_name + ".bsp", inline=False)
                embed.add_field(name="Backup Download Link:", value=ALTFASTDL + map_name + ".bsp", inline=False)
                embed.set_footer(text="If the download links don't work, try setting 'big_map' to false!")
                await interaction.response.send_message(embed=embed)
            else:
                embed=discord.Embed(
                    title="Map Download Link",
                    description="`" + map_name + "`",
                    color=0x00FF00
                )
                embed.add_field(name="Download Link:", value=FASTDL + map_name + ".bsp", inline=False)
                embed.set_footer(text="If the download link doesn't work, try setting 'big_map' to false!")
                await interaction.response.send_message(embed=embed)
        case False:
            if ALTFASTDL != "":
                embed=discord.Embed(
                    title="Map Download Link",
                    description="`" + map_name + "`",
                    color=0x00FF00
                )
                embed.add_field(name="Download Link:", value=FASTDL + map_name + ".bsp.bz2", inline=False)
                embed.add_field(name="Backup Download Link:", value=ALTFASTDL + map_name + ".bsp.bz2", inline=False)
                embed.set_footer(text="If the download links don't work, try setting 'big_map' to false!")
                await interaction.response.send_message(embed=embed)
            else:
                embed=discord.Embed(
                    title="Map Download Link",
                    description="`" + map_name + "`",
                    color=0x00FF00
                )
                embed.add_field(name="Download Link:", value=FASTDL + map_name + ".bsp.bz2", inline=False)
                embed.set_footer(text="If the download link doesn't work, try setting 'big_map' to false!")
                await interaction.response.send_message(embed=embed)

# Start up the bot
try:
    print("Starting up the bot")
    client.run(TOKEN)
except discord.errors.LoginFailure:
    sys.exit("ERROR! Invalid bot token specified, aborting!")
except Exception as e:
    sys.exit("ERROR! Bot crashed...")