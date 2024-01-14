import random
import commands as command

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
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
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   max_banana = datafind['max_banana']
   banana = datafind['banana']
   random_banana = random.randint(1,max_banana)
   text = f"""```
{random_banana}x 🍌 [ MAX : {max_banana}x 🍌 ]
```━━━━━━━━━━━━━━━━━━━━━━━━━━━
```Backpack
{banana+random_banana}x 🍌
```
"""
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
   update = {'$inc': {'banana': random_banana}}
   query = {}
   await datack.update_one(query,update)