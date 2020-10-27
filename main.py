import os

import discord
import dotenv
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

dotenv.load_dotenv("config.env")

# Mongodb instance
mongo_client = AsyncIOMotorClient(
    'xxx')
db = mongo_client['manager']


async def get_prefix(bot, message):
    get = await db['prefixes'].find_one({
        "guild_id": message.guild.id
    })
    prefix = get['prefix']
    return prefix


client = commands.AutoShardedBot(command_prefix=get_prefix, intents=discord.Intents.all(), activity=discord.Game(name="Among Us"))

# Store MongoDB connection in a bot variable.
client.db = db


# Load all cogs
if __name__ == "__main__":
    for filename in os.listdir('cogs'):
        if filename.endswith('.py') and not filename.startswith('-'):
            client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv("BOT_TOKEN"))
