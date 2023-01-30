import logging
from jokeapi import Jokes
import discord
from discord.ext import commands
import utils

import settings

logger = logging.getLogger(__name__)


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"User: {bot.user} (ID: {bot.user.id})")
        await utils.load_videocmds(bot)

    @bot.command()
    async def joke(ctx: commands.Context):
        j = await Jokes()
        blacklist = ["racist"]
        if not ctx.message.channel.is_nsfw():
            blacklist.append("nsfw")
        joke = await j.get_joke(blacklist=blacklist)
        msg = ""
        if joke["type"] == "single":
            msg = joke["joke"]
        else:
            msg = joke["setup"]
            msg += f"||{joke['delivery']}||"
        await ctx.send(msg)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
