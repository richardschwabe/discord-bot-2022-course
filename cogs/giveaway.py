import random
import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)

class GiveAway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(self, ctx, prize: str, winners : int = 1, role:discord.Role = None):
        members_selection = []
        if role:
            members_selection = role.members
        else:
            members_selection = ctx.channel.guild.members

        filtered_members = []
        for member in members_selection:
            if not member.bot:
                filtered_members.append(member)

        if not len(filtered_members):
            return

        if len(filtered_members) < winners:
            await ctx.message.author.send("Hey refinde your list. everyone would win!")
            return

        winners_list = []

        while len(winners_list) < winners:
            winner = random.choice(filtered_members)
            if winner.display_name not in winners_list:
                await ctx.send(f"The winner for {prize} is {winner.display_name}")
                winners_list.append(winner.display_name)



async def setup(bot):
    await bot.add_cog(GiveAway(bot))
