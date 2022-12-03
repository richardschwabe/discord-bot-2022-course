
import settings
import discord 
from discord.ext import commands
import utils
    
logger = settings.logging.getLogger("bot")
        
def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        await utils.load_videocmds(bot)
    
    @bot.command()
    async def paginate(ctx):
        embed = discord.Embed()
        await ctx.send(embed=embed)
        
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()