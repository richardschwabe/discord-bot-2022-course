import typing
import settings
import discord 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")

class SlapReason(typing.NamedTuple):
    reason : str
    
class SlapTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str) -> SlapReason:
        return SlapReason(reason=f"*** {value} *** ")


def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!",intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        await bot.load_extension("slashcmds.welcome")
        
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
       
    @bot.tree.command()
    async def slap(interaction: discord.Interaction, reason: app_commands.Transform[SlapReason, SlapTransformer]):
        await interaction.response.send_message(f"Ouch {reason}", ephemeral=True)
    
    @bot.tree.command()
    async def range(interaction: discord.Interaction, value: app_commands.Range[int, None, 10]):
        await interaction.response.send_message(f"Range Result {value}", ephemeral=True)
        
    
       
           
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()