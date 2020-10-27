import datetime

import discord
from discord.ext import commands


class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = client.db
        self.current_games = client.db['current_games']
        self.categories = client.db['categories']

    @commands.command(name="create",
                      brief="Create an Among Us session.",
                      aliases=["cr"],
                      usage="mh. create <code> <imposters> <language> <map>")
    @commands.guild_only()
    async def create_session(self, ctx, code: str, imposters: int, langauge: str, *, map_name: str):
        current_hosts = await self.current_games.find_one({
            "host_id": ctx.author.id
        })
        try:
            if current_hosts:
                embed = discord.Embed(colour=0x2F3136,
                                      timestamp=datetime.datetime.utcnow(),
                                      description="You are already part of a game,\nplease leave your current game before creating a new one.")
                await ctx.send(embed=embed)
            else:
                # Get the category from the databse and create the voice channel under that category
                get_cat = await self.categories.find_one({
                    "guild_id": ctx.guild.id
                })
                cat = self.client.get_channel(get_cat['cat_id'])
                vc = await ctx.guild.create_voice_channel(name=f"{ctx.author.display_name}'s Lobby",
                                                          userlimit=10, category=cat)
                invite = await vc.create_invite(reason=f"{ctx.author.display_name}'s Among Us Lobby")

                # Create an embed object and send it
                embed = discord.Embed(colour=0x2F3136)
                embed.description = f"**🔢 Code**: {code.upper()}\n" \
                                    f"**🗺️ Map**: {map_name.capitalize()}\n" \
                                    f"**<:imposter:770452353001717783> Imposters**: {imposters}\n" \
                                    f"**🌐 Language**: {langauge.capitalize()}\n" \
                                    f"**🔊 Voice Chat**: {vc.mention}"
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_thumbnail(url=ctx.author.avatar_url)
                msg = await ctx.send(content=invite, embed=embed)

                await self.current_games.insert_one({
                    "voice_id": vc.id,
                    "host_id": ctx.author.id,
                    "message_id": msg.id,
                    "channel_id": msg.channel.id
                })

        except Exception as error:
            await ctx.send(error)

    @commands.command(name="end",
                      brief="End an Among Us session.",
                      usage="mh. end")
    @commands.guild_only()
    async def end_session(self, ctx):
        try:
            # Remove channel id from the database and delete the voice channel and message from the guild.
            get_channel = await self.current_games.find_one({
                "host_id": ctx.author.id
            })
            await self.current_games.delete_many({
                "host_id": ctx.author.id
            })
            # Delete voice channel
            voice_channel = ctx.guild.get_channel(get_channel['voice_id'])
            await voice_channel.delete()

            # Delete left over messages
            text_channel = ctx.guild.get_channel(get_channel['channel_id'])
            message = await text_channel.fetch_message(get_channel['message_id'])
            await message.delete()

            embed = discord.Embed(colour=0x2F3136,
                                  timestamp=datetime.datetime.utcnow(),
                                  description=f"Hey {ctx.author.mention}, I have ended your game.\nThank you for playing!")
            await ctx.send(embed=embed)
        except Exception as error:
            print(error)
            embed = discord.Embed(color=0x2F3136,
                                  timestamp=datetime.datetime.utcnow(),
                                  description="You do not have a game in session.")
            await ctx.send(embed=embed)

    @commands.command(name="mute",
                      brief="Mute everyone in your current Voice Channel.",
                      usage="mh. mute")
    async def mute_all(self, ctx):
        for m in ctx.author.voice.channel.members:
            await m.edit(mute=True)
        await ctx.message.add_reaction("👍🏻")

    @commands.command(name="unmute",
                      brief="Unmute everyone in your current Voice Channel.",
                      usage="mh. unmute")
    async def unmute_all(self, ctx):
        for m in ctx.author.voice.channel.members:
            await m.edit(mute=False)
        await ctx.message.add_reaction("👍🏻")


def setup(client):
    client.add_cog(Manager(client))
