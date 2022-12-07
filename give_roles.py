import random
import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    async def setup_roles():
        role_names = ['girl', 'boy', 'new', 'oldtime']
        for role_item in role_names:
            if role_item not in [r.name for r in bot.guilds[0].roles]:
                await bot.guilds[0].create_role(
                    name=role_item,
                    hoist=True
                )

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        await setup_roles()


    @bot.command()
    async def add(ctx, member: discord.Member, role: discord.Role ):
        if member and role:
            await member.add_roles(role)
            desc = f"{member.name} received {role.name} role"
            embed = discord.Embed(title="New role assigned", description=desc)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Not found...")

    @bot.command()
    async def remove(ctx, member: discord.Member, role: discord.Role ):
        if member and role:
            await member.remove_roles(role)
        else:
            await ctx.send("Not found...")


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()