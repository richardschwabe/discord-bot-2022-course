import settings
import discord 
from discord.ext import commands
import utils
    
logger = settings.logging.getLogger("bot")
    
class SimpleView(discord.ui.View):
    
    def __init__(self):
        super().__init__()
        self.foo = None
        
    
    @discord.ui.button(label="Say Hello", style=discord.ButtonStyle.green)
    async def hello(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("World", ephemeral=True)
        self.foo = True 
        self.stop()
        
        
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.foo = False
        self.stop()

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        await utils.load_videocmds(bot)

    @bot.command()
    async def button(ctx):
        view = SimpleView()
        await ctx.send(view=view)
        await view.wait()
        
        if view.foo is None:
            logger.error("Timedout")
        elif view.foo:
            logger.info("Confirmed / Finished")
        else:
            logger.info("Cancelling")
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()