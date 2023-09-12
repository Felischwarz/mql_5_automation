from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from trading import (buy_now, gold_sell_limit, gold_sell_stop, 
                     gold_buy_stop, move_sl_to_be, delete_buy_stops, close_trade)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

channel_name = "bot-trading-signals"

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Angemeldet als {bot.user}')

@bot.event
async def on_message(message):
    content = message.content
    channel = message.channel

    if channel.name != channel_name:
        return

    try:
        if content.startswith("BUY "):
            item, _, price_data = content[4:].partition("NOW")
            tp_price, sl_price = map(float, price_data.strip().split()[2::2])
            await buy_now(item.strip(), tp_price, sl_price)

        elif content.startswith("GOLD SELL LIMITS "):
            _, price_data = content[17:].split("@")
            limit_price, tp_price, sl_price = map(float, price_data.split()[0::2])
            await gold_sell_limit(limit_price, tp_price, sl_price)
            
        elif content.startswith("GOLD SELL STOPS "):
            _, price_data = content[17:].split("@")
            stop_price, tp_price, sl_price = map(float, price_data.split()[0::2])
            await gold_sell_stop(stop_price, tp_price, sl_price)
        
        elif content.startswith("GOLD BUY STOPS "):
            _, price_data = content[16:].split("@")
            stop_price, tp_price, sl_price = map(float, price_data.split()[0::2])
            await gold_buy_stop(stop_price, tp_price, sl_price)
        
        elif content.startswith("MOVE SL TO B/E "):
            _, new_sl_price = content[14:].split("at")
            await move_sl_to_be(float(new_sl_price.strip()))

        elif content.startswith("Delete BUY STOPS"):
            await delete_buy_stops()
        
        elif content.startswith("CLOSE "):
            _, close_data = content[6:].split("HERE")
            await close_trade(close_data.strip())

    except ValueError:
        await channel.send("Incorrect input. Check the command and price syntax.")
    except Exception as e:
        await channel.send(f"An error has occurred: {e}")

bot.run(BOT_TOKEN)
