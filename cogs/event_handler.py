from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.categories = client.db['categories']

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.client.user} is ready.")

    # Create a category upon joining a guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        results = await self.categories.find_one({
            "guild_id": guild.id
        })
        if results:
            return
        else:
            cat = await guild.create_category(name="MiraHQ")
            await self.categories.insert_one({
                "guild_id": guild.id,
                "cat_id": cat.id
            })


def setup(client):
    client.add_cog(Events(client))
