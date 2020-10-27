import datetime

import discord
from discord.ext import commands


class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = client.db
        self.current_games = client.db['current_games']
        self.categories = client.db['categories']

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        results = await self.categories.find_one({
            "guild_id": guild.id
        })
        if results:
            return
        else:
            cat = await guild.create_category(name="Among Us Manager")
            await self.categories.insert_one({
                "guild_id": guild.id,
                "cat_id": cat.id
            })

    @commands.command(name="create",
                      brief="Create an Among Us session.",
                      aliases=["cr"],
                      usage="am.create <code> <imposters> <language> <map>")
    async def create_session(self, ctx, code: str, imposters: int, langauge: str, *, map_name: str):
        current_hosts = await self.current_games.find_one({
            "host_id": ctx.author.id
        })
        try:
            if current_hosts:
                await ctx.send(
                    "You are already part of a game, please leave your current game before creating a new one.")
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
                                    f"**🔊 Voice Chat**: {vc.mention}\n" \
                                    f"**🎮 Players**: {len([m for m in vc.members])}"
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
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
                      usage="am.end")
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
                                  description=f"I have ended your game, {ctx.author.mention}")
            await ctx.send(embed=embed)
        except Exception as error:
            print(error)
            await ctx.send("You do not have a game in session.")


def setup(client):
    client.add_cog(Manager(client))
