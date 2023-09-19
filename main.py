from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from trading import (buy_now, sell_now, sell_limit, sell_stop, buy_stop, 
                     move_sl_to_be, delete_buy_stops, close_trade, initializeMt5)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

channel_name = "bot-trading-signals"

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Signed in as {bot.user}')
    await initializeMt5()

@bot.event
async def on_message(message):
    if message.channel.name == channel_name:
        content = message.content.upper().split('\n')
        if len(content) >= 3:
            command, tp, sl = content[0], content[1], content[2]
            if command.startswith('BUY ') and command.endswith(' NOW'):
                tp_price = float(tp.split('-')[1].strip())
                sl_price = float(sl.split('-')[1].strip())
                await buy_now(tp_price, sl_price)
            
            if command.startswith('SELL GOLD NOW'):
                tp_price = float(tp.split('-')[1].strip())
                sl_price = float(sl.split('-')[1].strip())
                await sell_now(tp_price, sl_price)
                
            elif ' SELL LIMITS @' in command:
                _, price = command.split(' SELL LIMITS @')
                tp_price = float(tp.split('-')[1].strip())
                sl_price = float(sl.split('-')[1].strip())
                await sell_limit(float(price), tp_price, sl_price)
            
            elif ' SELL STOPS @' in command:
                _, price = command.split(' SELL STOPS @')
                tp_price = float(tp.split('-')[1].strip())
                sl_price = float(sl.split('-')[1].strip())
                await sell_stop(float(price), tp_price, sl_price)
            
            elif ' BUY STOPS @' in command:
                _, price = command.split(' BUY STOPS @')
                tp_price = float(tp.split('-')[1].strip())
                sl_price = float(sl.split('-')[1].strip())
                await buy_stop(float(price), tp_price, sl_price)
        
        else:
            if content[0].startswith('MOVE SL TO B/E'):
                price_part = content[0].split('AT')
                new_price = None if len(price_part) < 2 else float(price_part[1].strip())
                await move_sl_to_be(new_price)
            
            elif content[0] == 'DELETE BUY STOPS':
                await delete_buy_stops()
            
            elif content[0].startswith('CLOSE '):
                close_data = content[0].split('CLOSE ')[1].strip()
                await close_trade(close_data)

bot.run(BOT_TOKEN)
