import discord 
from discord.ext import commands
import settings
import utils
    
logger = settings.logging.getLogger("bot")
    
def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        await utils.load_videocmds(bot)

        await bot.load_extension("cogs.music")


    @bot.command()
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        
    @bot.command()
    async def unload(ctx, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}")
        
    @bot.command()
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()