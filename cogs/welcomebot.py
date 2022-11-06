import discord
from discord.ext import commands 
import settings 

logger = settings.logging.getLogger(__name__)

class WelcomeBot(commands.Cog):
    new_member_role_name = "New Member"
    rules_message_id = 1038736170680594443
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.rules_message_id == payload.message_id:
            if payload.emoji.name == "✅":
                for role in await self.bot.guilds[0].fetch_roles():
                    if role.name == self.new_member_role_name:
                        await payload.member.add_roles(role)
                        break
    
    async def setup_role(self):
        exists = False
        for role in await self.bot.guilds[0].fetch_roles():
            if role.name == self.new_member_role_name:
                exists = True
                break
        if exists:
            return 
        permissions= discord.Permissions.none()
        permissions.view_channel = True
        
        await self.bot.guilds[0].create_role(
            name=self.new_member_role_name,
            color=discord.Color.red(),
            hoist=True, 
            permissions =permissions
        )
        
async def setup(bot):
    welcome_bot = WelcomeBot(bot)
    await bot.add_cog(welcome_bot)
    await welcome_bot.setup_role()