import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)

# Intents.voice_states is required!

class TemporaryVoice(commands.Cog):

    temporary_channels = []
    temporary_categories = []

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState)    :
        possible_channel_name = f"{member.nick}'s area"
        if after.channel:
            if after.channel.name == "temp":
                temp_channel = await after.channel.clone(name=possible_channel_name)
                await member.move_to(temp_channel)
                self.temporary_channels.append(temp_channel.id)
            if after.channel.name == 'teams':
                temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
                await temporary_category.create_text_channel(name="text")
                temp_channel = await temporary_category.create_voice_channel(name="voice")
                await member.move_to(temp_channel)
                self.temporary_categories.append(temp_channel.id)


        if before.channel:
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
            if before.channel.id in self.temporary_categories:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()

async def setup(bot):
    await bot.add_cog(TemporaryVoice(bot))