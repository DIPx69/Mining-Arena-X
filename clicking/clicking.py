import telebot
import os
import config
import random
import commands as command
import json
import dns.resolver
import config
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023

async def clicking(call):
   keyboard = types.InlineKeyboardMarkup()
   buttons = [types.InlineKeyboardButton(text='ㅤ', callback_data='clicking invalid'),types.InlineKeyboardButton(text='ㅤ', callback_data='clicking invalid'),types.InlineKeyboardButton(text='ㅤ', callback_data='clicking invalid')]
   random_button_index = random.randint(0, len(buttons) - 1)
   buttons[random_button_index].text = '🍌'
   buttons[random_button_index].callback_data = 'clicking click'
   back_button = types.InlineKeyboardButton(text='Back',callback_data='clicking main')
   keyboard.add(*buttons)
   keyboard.add(back_button)
   random_banana = random.randint(1,20)
   text = "✅ You Clicked\n"
   text += f"""```
{random_banana}x 🍌
```━━━━━━━━━━━━━━━━━━━━━━━━━━━
Keep Grinding 😉💪🏻
"""
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)