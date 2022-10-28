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


    @bot.group()
    async def math(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"No, {ctx.subcommand_passed} does not belong to math")
            
            
    @math.group()
    async def simple(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")
        
    @simple.command()
    async def add(ctx, one : int  , two : int ):
        await ctx.send(one + two)
    
    @simple.command()
    async def substract(ctx, one : int  , two : int ):
        await ctx.send(one - two)
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()