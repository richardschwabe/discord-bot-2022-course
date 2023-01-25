import logging
import discord
from discord.ext import commands
import utils

import settings

logger = logging.getLogger(__name__)

ROLES = [1035163844064071720]


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"User: {bot.user} (ID: {bot.user.id})")
        await utils.load_videocmds(bot)

    async def enable_lockdown(guild, is_lockdown=True):
        for role in guild.roles:
            if role.id in ROLES:
                current_permissions = role.permissions
                if is_lockdown:
                    current_permissions.update(
                        send_messages=False,
                        use_application_commands=False,
                        send_messages_in_threads=False,
                    )
                else:
                    current_permissions.update(
                        send_messages=True,
                        use_application_commands=True,
                        send_messages_in_threads=True,
                    )
                await role.edit(permissions=current_permissions)

    @bot.command()
    async def lockdown(ctx: commands.Context):
        guild = ctx.message.guild
        await enable_lockdown(guild)

        await ctx.send("The server is in lockdown")

    @bot.command()
    async def unlock(ctx: commands.Context):
        guild = ctx.message.guild
        await enable_lockdown(guild, False)

        await ctx.send("The lockdown is over.")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
