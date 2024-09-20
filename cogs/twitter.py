import discord
from discord.ext import commands
import aiohttp
from discord import Webhook
from datetime import datetime

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="twitter", description="Commande pour poster un tweet sur le salon")
    async def twitter_command(self, ctx: discord.ApplicationContext, tweet: str, image_url: str = None):
        embed = discord.Embed(
            title="🔵 **Tweet**",
            description=f"{tweet}",
            color=discord.Color.blue()
        )
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.display_avatar.url)
        if image_url:
            embed.set_image(url=image_url)
        

        embed.set_thumbnail(url="https://th.bing.com/th/id/R.5a554460df3a35d8f82998867f8cef08?rik=nAR5pirhoH23iw&riu=http%3a%2f%2flogo-logos.com%2fwp-content%2fuploads%2f2016%2f11%2fTwitter_logo_white-blue.png&ehk=62dyJZMX8L1jdE143mrrfrzH5uPu9PRiYHUq2ZBY0I4%3d&risl=&pid=ImgRaw&r=0")
        embed.set_footer(text="Twitter", icon_url="https://th.bing.com/th/id/R.5a554460df3a35d8f82998867f8cef08?rik=nAR5pirhoH23iw&riu=http%3a%2f%2flogo-logos.com%2fwp-content%2fuploads%2f2016%2f11%2fTwitter_logo_white-blue.png&ehk=62dyJZMX8L1jdE143mrrfrzH5uPu9PRiYHUq2ZBY0I4%3d&risl=&pid=ImgRaw&r=0")

        webhook_url = 'https://discord.com/api/webhooks/1284300502489763920/qAOz5oiyK2cIcSXrizfcZ0oBN64MwLynTEK60BHd7pTTRQlmESSDn1zTxliFu8GNlwIV'

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.send(embed=embed, username="Twitter", avatar_url='https://th.bing.com/th/id/R.5a554460df3a35d8f82998867f8cef08?rik=nAR5pirhoH23iw&riu=http%3a%2f%2flogo-logos.com%2fwp-content%2fuploads%2f2016%2f11%2fTwitter_logo_white-blue.png&ehk=62dyJZMX8L1jdE143mrrfrzH5uPu9PRiYHUq2ZBY0I4%3d&risl=&pid=ImgRaw&r=0')

def setup(bot):
    bot.add_cog(Twitter(bot))

