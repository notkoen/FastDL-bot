
# FastDL Bot

(Current version: 0.6)

A discord bot written in Python using the discord.py library to allow players to query map download links and shortcuts to both FastDL and resource packs. This bot was written for Zeddy's Zombie Escape server specifically where several players have reported issues of downloading maps. The goal of this project is to allow new players to easily find and download maps directly without having to look for fastDL links.

I am currently satisified with how the bot is right now. There is obviously room for lots of improvement and changes (things like optimization and speed). However, the current method works, and I don't expect there to be any issues.

## Installation

1. Run `pip install -r requirements.txt` to install all bot required libraries
2. Open the `.env` file and fill in all the information
3. Upload both `mapcycle.txt` and `bigmaps.txt` to a public website for accessing (eg. GitHub)
4. Run the bot with `python bot.py`

## Future Roadmap

- Code refactoring and optimization
- Add self-update without the need to restart the bot for whenever new map updates are done
