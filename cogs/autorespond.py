import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)

class AutorespondBot(commands.Cog):

    message_list = list()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.content.startswith(self.bot.command_prefix):
                if len(self.message_list) > 0:
                        for respond_config in self.message_list:
                            if respond_config['needle'].lower() in message.content.lower():
                                await message.channel.send(respond_config['message'])
                                break

    @commands.group()
    async def autorespond(self, ctx):
        ...

    @autorespond.command()
    async def create(self, ctx, needle: str, answer: str):
        respond_config = {
            'needle': needle,
            "message": answer
        }
        self.message_list.append(respond_config)

    @autorespond.command()
    async def edit(self, ctx, index: int, answer: str):
        self.message_list[index]["message"] = answer

    @autorespond.command()
    async def delete(self, ctx, index: int):
        self.message_list.pop(index)

    @autorespond.command()
    async def show(self, ctx,):
        result = "This is the configuration. Use the index at the front to edit and delete \n"
        code = "```"
        for index, item in enumerate(self.message_list):
            code += f"{index}: {item['needle']} -> {item['message']} \n"
        code += "```"

        result += code
        await ctx.send(result)



async def setup(bot):
    await bot.add_cog(AutorespondBot(bot))