import random
import discord
import peewee
from discord.ext import commands
import settings
from models.account import Account

logger = settings.logging.getLogger(__name__)


class EconomyBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def me(self, ctx):
        account = Account.fetch(ctx.message)

        await ctx.send(f"Your balance is: {account.amount}")

    @commands.command()
    async def coin(self, ctx, choice: str, amount: int):
        account = Account.fetch(ctx.message)

        if amount > account.amount:
            await ctx.send("You don't have enough credits.")
            return

        heads = random.randint(0, 1)
        won = False
        if heads and choice.lower().startswith("h"):
            won = True
            account.amount += amount
        elif not heads and choice.lower().startswith("t"):
            won = True
            account.amount += amount
        else:
            account.amount -= amount

        account.save()

        message = "You lost!"
        if won:
            message = "You won!"

        await ctx.send(message)



async def setup(bot):
    await bot.add_cog(EconomyBot(bot))
