import os

import discord
import dotenv
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

client = commands.AutoShardedBot(command_prefix='am.',
                                 intents=discord.Intents.all())  # To create an instance of class commands.Bot
dotenv.load_dotenv("config.env")

# Mongodb instance
mongo_client = AsyncIOMotorClient(
    'xxx')
db = mongo_client['manager']
client.db = db



@client.event
async def on_ready():
    print(f"Client {client.user}\n"
          f"ID: {client.user.id}")


# Load all of the cogs
if __name__ == "__main__":
    for filename in os.listdir('cogs'):
        if filename.endswith('.py') and not filename.startswith('-'):
            client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv("BOT_TOKEN"))
