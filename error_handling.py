import random
import settings
import discord 
from discord.ext import commands
    
logger = settings.logging.getLogger("bot")
    
def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    
    @bot.event
    async def on_command_error(ctx, error):   
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("handled error globally")
            
    @bot.command()
    async def add(ctx, one : int  , two : int ):
        await ctx.send(one + two)

    @add.error
    async def add_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("handled error locally")
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()