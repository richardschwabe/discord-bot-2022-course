import typing
import discord
from discord.ext import commands

import settings

logger = settings.logging.getLogger(__name__)

@commands.command()
async def debug(ctx, item : typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel]):    
    logger.info(item.__repr__)
    embed = discord.Embed(
        title=f"{item.name} Info"
    )
    embed.add_field(name="ID", value=item.id, inline=False)
    embed.add_field(name="Type", value=item.type, inline=True)
    embed.add_field(name="Created at", value=discord.utils.format_dt(item.created_at), inline=False)
    
    if item.category:
        embed.add_field(name="Category", value=f"{item.category.name} (ID: {item.category.id})", inline=False)
    
    if isinstance(item, discord.VoiceChannel):
        embed.add_field(name="Bitrate", value=item.bitrate, inline=True)
        embed.add_field(name="User Limit", value=item.user_limit, inline=True)
        embed.add_field(name="Members", value=len(item.members), inline=True)
        if item.members:
            members_list = ""
            for member in item.members:
                members_list += f"{member.nick} (ID: {member.id}), "
            embed.add_field(name="Active Members Info", value=members_list[:-2], inline=False)
    
    if isinstance(item, discord.TextChannel):
        embed.add_field(name="News?", value="Yes" if item.is_news() else "No", inline=True)
        embed.add_field(name="NSFW?", value="Yes" if item.is_nsfw() else "No", inline=True)
    
    if isinstance(item, discord.StageChannel):
        embed.add_field(name="Bitrate", value=item.bitrate, inline=True)
        if item.moderators:
            moderators_list = ""
            for moderator in item.moderators:
                moderators_list += f"{moderator.display_name} (ID {moderator.id}),"
            embed.add_field(name="Moderators", value=moderators_list[:-1], inline=False)
        
        if item.listeners:
            listeners_list = ""
            for listener in item.listeners:
                listeners_list += f"{listener.display_name} (ID {listener.id}),"
            embed.add_field(name="Listeners", value=listeners_list[:-1], inline=False)
        
        if item.speakers:
            speakers_list = ""
            for speaker in item.speakers:
                speakers_list += f"{speaker.display_name} (ID {speaker.id}),"
            embed.add_field(name="Speakers", value=speakers_list[:-1], inline=False)
        
    await ctx.send(embed=embed)
    
@debug.error 
async def debug_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):        
        await ctx.send("Must have a channel to inspect")

async def setup(bot):
    bot.add_command(debug)