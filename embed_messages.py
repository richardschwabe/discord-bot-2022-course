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
    
    @bot.command()
    async def ping(ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_teal(), 
            description="this is the description", 
            title="this is the title"
        )
        
        embed.set_footer(text="this is the footer")
        embed.set_author(name="Richard", url="https://www.youtube.com/channel/UCIJe3dIHGq1lIAxCCwx8eyA")
        
        embed.set_thumbnail(url="https://yt3.ggpht.com/GiBCvnzO8e3_cPclwtRCUqLye86F0_xNOPK0FYeshaths5DO2SLvJq9cBVZ0BL-oNwjt90huIw=s108-c-k-c0x00ffffff-no-rj")
        embed.set_image(url="https://i.ytimg.com/vi/SoqYG_5pQBA/maxresdefault.jpg")
        
        embed.add_field(name="Channel", value="https://www.youtube.com/channel/UCIJe3dIHGq1lIAxCCwx8eyA", inline=False)
        embed.add_field(name="Website", value="richardschwabe.de" )
        embed.insert_field_at(1,name="Tree", value="https://linktr.ee/richardschwabe")
        
        await ctx.send(embed=embed)
    
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()