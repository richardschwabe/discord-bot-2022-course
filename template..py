import logging
import discord
from discord.ext import commands

import settings

logger = logging.getLogger(__name__)


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("pong")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
