import random
import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class GiveAway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(self, ctx, prize: str, role:discord.Role = None):
        if role:
            winner = random.choice(role.members)
        else:
            winner = random.choice(self.bot.guilds[0].members)
        await ctx.send(f"And the winner is {winner.display_name}")


async def setup(bot):
    await bot.add_cog(GiveAway(bot))
