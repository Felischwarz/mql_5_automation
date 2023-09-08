from discord.ext import commands

import discord

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


#env file
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

channel_name = "bot-trading-signals"


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Angemeldet als {bot.user}')

@bot.event
async def on_message(message):
    print("test")
    if message.channel.name == channel_name and message.content.startswith('BUY'):
        # Führe deine Funktion hier aus
        await print("BUY")


bot.run(BOT_TOKEN)
