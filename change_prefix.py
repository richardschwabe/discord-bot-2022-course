import logging
import discord
from discord.ext import commands

import settings

logger = logging.getLogger(__name__)

guild_prefixes = {}


def get_prefix(bot, message):
    if message:
        if message.guild.id in guild_prefixes:
            return guild_prefixes[message.guild.id]
    return "!"


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=get_prefix, intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("pong")

    @bot.command()
    async def prefix(ctx: commands.Context, new_prefix: str):
        guild_prefixes.update({ctx.message.guild.id: new_prefix})
        await ctx.send("Prefix has been updated.")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
