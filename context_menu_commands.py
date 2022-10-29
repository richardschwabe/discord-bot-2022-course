from re import A
import settings
import discord 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!",intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
       
    @bot.tree.context_menu(name="Show join date")
    async def get_joined_date(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"Member joined: {discord.utils.format_dt(member.joined_at)} ", ephemeral=True)
  
    @bot.tree.context_menu(name="Report Message")
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Message reported ", ephemeral=True)

    # Only member & user can be used via Union
    # In addition context menu works on messages
    # @bot.tree.context_menu(name="Report Message")
    # async def report_message(interaction: discord.Interaction, channel: discord.VoiceChannel):
        # await interaction.response.send_message(f"Message reported ", ephemeral=True)
    
    
       
           
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()