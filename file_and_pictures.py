import pathlib
import random
import logging

import requests

import discord
from discord.ext import commands

import settings

logger = logging.getLogger(__name__)


def get_random_cat_image():
    cat_images = pathlib.Path(settings.BASE_DIR / "images" / "cats").glob("**/*")
    return random.choice(list(cat_images))


def get_random_dog_image_url():
    url = "https://dog.ceo/api/breeds/image/random"
    res = requests.get(url)
    data = res.json()
    if "message" in data:
        return data["message"]
    return None


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def dog(ctx: commands.Context):
        random_dog_image = get_random_dog_image_url()
        if not random_dog_image:
            await ctx.message.delete(3)
            return

        embed = discord.Embed(title="Random Dog showed up")
        embed.set_image(url=random_dog_image)
        await ctx.send(embed=embed)

    @bot.command()
    async def cat(ctx):
        random_cat_local_path = get_random_cat_image()
        cat_image_file = discord.File(
            random_cat_local_path, filename=random_cat_local_path.name
        )

        embed = discord.Embed(title="Random Cat showed up")
        embed.set_image(url=f"attachment://{random_cat_local_path.name}")
        await ctx.send(embed=embed, file=cat_image_file)

    @bot.command()
    async def meeting(ctx):
        meeting_notes_file_path = pathlib.Path(settings.BASE_DIR / "data" / "text.txt")
        meeting_file = discord.File(
            meeting_notes_file_path, filename=meeting_notes_file_path.name
        )
        await ctx.send(file=meeting_file)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
