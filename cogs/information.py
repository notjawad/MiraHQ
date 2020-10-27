import discord
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="map",
                    brief="Get information about an Among Us map.",
                    invoke_without_command=True)
    async def map_(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @map_.command(name="skeld",
                  brief="Get a guide for the map The Skeld.")
    async def skeld_(self, ctx):
        embed = discord.Embed(colour=0x2F3136)
        embed.set_image(url="https://i.imgur.com/XMYTrtZ.jpg")
        await ctx.send(embed=embed)

    @map_.command(name="mirahq",
                  brief="Get a guide for the map MIRQ HQ.")
    async def mirahq_(self, ctx):
        embed = discord.Embed(colour=0x2F3136)
        embed.set_image(url="https://i.imgur.com/QgMTpTO.jpg")
        await ctx.send(embed=embed)

    @map_.command(name="polus",
                  brief="Get a guide for the map Polus.")
    async def polus_(self, ctx):
        embed = discord.Embed(colour=0x2F3136)
        embed.set_image(url="https://i.imgur.com/wZyEVcA.jpg")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Information(client))
