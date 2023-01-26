import logging
import discord
from discord.ext import commands

import settings

logger = logging.getLogger(__name__)


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    async def update_presence():
        total_member_count = 0
        for guild in bot.guilds:
            if guild.member_count:
                total_member_count += guild.member_count

        activity = discord.Activity(
            name=f"{total_member_count} users", type=discord.ActivityType.listening
        )

        await bot.change_presence(activity=activity)

    @bot.event
    async def on_member_join(member: discord.Member):
        await update_presence()

    @bot.command()
    async def presence(ctx: commands.Context):
        await update_presence()

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
