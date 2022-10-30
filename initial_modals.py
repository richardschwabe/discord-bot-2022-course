import traceback
import settings
import discord 
from discord.ext import commands
    
logger = settings.logging.getLogger("bot")

class FeedbackModal(discord.ui.Modal, title="This is the title"):
    
    message = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label= "Message",
        required=True, 
        max_length=500,
        placeholder="Type your message"
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thank you", ephemeral=True)
    
    async def on_timeout(self) -> None:
        ...
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message("Ooops", ephemeral=True)
        traceback.print_tb(error.__traceback__)

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

    @bot.tree.command()
    async def feedback(interaction: discord.Interaction):       
        feedback_model = FeedbackModal()
        await interaction.response.send_modal(feedback_model)
        
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()