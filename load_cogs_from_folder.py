import discord 
from discord.ext import commands
import settings
    
logger = settings.logging.getLogger("bot")
    
def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
        
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