import discord
from discord.ext import commands
import settings
import utils
import database
from models.account import Account
logger = settings.logging.getLogger(__name__)

def run():

    # Check if data table exist, then skip or create
    data_exist = database.db.table_exists("account")
    if not data_exist:
        database.db.create_tables([Account])
        print("Data table account created")

    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        await utils.load_videocmds(bot)

        await bot.load_extension("cogs.economy")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()
