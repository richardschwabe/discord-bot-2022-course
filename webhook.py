import asyncio 
import discord 
from discord import Webhook
import aiohttp 

async def anything(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(title="This is from a webhook!")
        await webhook.send(embed=embed, username="Richard Web")
        
if __name__ == "__main__":
    url = "https://discord.com/api/webhooks/1038811426304827492/nmEARi892tDLS0Xcf7BZImtUkh7yAKgUR244yA3LiU6jC2ekpW7YDY6pStVvZ2TMZwYw"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(anything(url))
    loop.close()