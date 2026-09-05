import os

import discord
from discord.ext import commands

import mycord

from dotenv import load_dotenv


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    await bot.load_extension(
        "cogs.rocketleague"
    )


bot.run(
    os.getenv("DISCORD_TOKEN")
)