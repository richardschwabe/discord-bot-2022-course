import settings
import discord 
from discord.ext import commands
import utils
    
logger = settings.logging.getLogger("bot")
    
class SimpleView(discord.ui.View):
    
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.foo = None
        
    async def disable_all(self):
        for item in self.children:
            item.disabled = True 
            
        await self.message.edit(view=self)
        
    async def on_timeout(self) -> None:
        await self.message.channel.send("Timed out!")
        await self.disable_all()
    
    @discord.ui.button(label="Say Hello", 
                       style=discord.ButtonStyle.success)
    async def hello(self, 
                    interaction:discord.Interaction, 
                    button: discord.ui.Button):
        await interaction.response.send_message("World")
        self.foo = True 
        self.stop()
        
        
    @discord.ui.button(label="Cancel", 
                       style=discord.ButtonStyle.danger)
    async def cancel(self, 
                     interaction:discord.Interaction, 
                     button: discord.ui.Button):
        await interaction.response.send_message("Cancelling")
        self.foo = False
        self.stop()
        
    @discord.ui.button(label="Disabled", 
                       disabled=True,
                       style=discord.ButtonStyle.gray)
    async def disabled(self, 
                       interaction:discord.Interaction, 
                       button: discord.ui.Button):
        await interaction.response.send_message("Cancelling")
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
        view = SimpleView(timeout=5)
        
        button = discord.ui.Button(style=discord.ButtonStyle.primary, 
                                label="Open URL", 
                                url="https://www.youtube.com/@richardschwabe")
        
        view.add_item(button)
        
        message = await ctx.send(view=view)
        view.message = message
        await view.wait()
                
        if view.foo is None:
            logger.error("Timedout")
        elif view.foo:
            logger.info("Confirmed / Finished")
        else:
            logger.info("Cancelling")
        
        await view.disable_all()
        
        # await message.delete()
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()