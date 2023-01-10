import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class HybridCog(commands.Cog):

    display_name = "Hybrid Custom Title by Richard"

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")

    @commands.hybrid_command()
    async def show(self, ctx: commands.Context):
        embed = discord.Embed(title="Show Commands and their Cogs")
        output = ""
        for command in self.bot.tree.walk_commands():
            output = f"{command.name} - {command.wrapped.module} - {command.wrapped._cog.display_name}"

        embed.add_field(name="Commands", value=output, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HybridCog(bot))
