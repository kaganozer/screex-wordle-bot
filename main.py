import discord
from discord.ext import commands

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="s!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error has occured while trying to sync app commands: ", e)


async def load():
    folders = ["wordle", "game"]
    for folder in folders:
        for filename in os.listdir(f"./{folder}/cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"{folder}.cogs.{filename[:-3]}")
    await bot.load_extension("tree_error_handler")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


asyncio.run(main())
