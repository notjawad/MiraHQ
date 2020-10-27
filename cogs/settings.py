import discord
from discord.ext import commands


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefixes = client.db['prefixes']

    @commands.command(name="setprefix",
                      brief="Set or update the custom prefix.",
                      usage="mh. <setprefix> <new_prefix>")
    async def set_prefix(self, ctx, prefix: str):
        get_prefix = await self.prefixes.find_one({
            "guild_id": ctx.guild.id
        })
        if not get_prefix:
            await self.prefixes.insert_one({
                "prefix": prefix,
                "guild_id": ctx.guild.id
            })
        else:
            embed = discord.Embed(colour=0x2F3136,
                                  description=f"Your custom prefix is already set to `{get_prefix['prefix']}`.\n"
                                              f"Use {get_prefix['prefix']}updateprefix to update it.")
            await ctx.send(embed=embed)

    @commands.command(name="updateprefix",
                      brief="Update your custom prefix.",
                      usage="<prefix> <updateprefix> <new_prefix>")
    async def update_prefix(self, ctx, prefix: str):
        get_prefix = await self.prefixes.find_one({
            "guild_id": ctx.guild.id
        })
        if not get_prefix:
            embed = discord.Embed(colour=0x2F3136,
                                  description="You have not set up a custom prefix. Use command `setprefix` to do so.")
            await ctx.send(embed=embed)
        else:
            await self.prefixes.update_one({"guild_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
            await ctx.send(f"Your custom prefix has been set to `{prefix}`")


def setup(client):
    client.add_cog(Settings(client))
