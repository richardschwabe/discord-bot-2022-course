import settings
import discord 
from discord.ext import commands
    
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    
    @bot.command()
    async def ping(ctx):
        # await ctx.message.author.send("Hello")
        user = discord.utils.get(bot.guilds[0].members, nick="User2")
        if user:
            await user.send("Hello 2")
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()