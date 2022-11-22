import enum
from re import A
import typing
import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")

def is_owner():
    def predicate(interaction : discord.Interaction):
        if interaction.user.id == interaction.guild.owner_id:
            return True
    return app_commands.check(predicate)

def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!",intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

    @bot.tree.command()
    @is_owner()
    async def say(interaction: discord.Interaction, text_to_send : str):
        """ Simon Says ... """
        await interaction.response.send_message(f"{text_to_send}", ephemeral=True)

    @say.error
    async def say_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("Not allowed!", ephemeral=True)

    # Youtuber question in comment about Permission check
    @bot.tree.command()
    @app_commands.checks.has_permissions(kick_members=True)
    async def kicker(interaction: discord.Interaction):
        """ Check exception type ... """
        await interaction.response.send_message(f"You have the permissions", ephemeral=True)

    @kicker.error
    async def kicker_error(interaction: discord.Interaction, error):
        logger.info(type(error)) #<class 'discord.app_commands.errors.MissingPermissions'>
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You have no permissions to run this command", ephemeral=True)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()
