import random
import commands as command

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def shop(call):
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text='Back',callback_data='clicking main')
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   max_banana = datafind['max_banana']
   banana = datafind['banana']
   upgrade_cost = max_banana * 20
   upgrade_button = types.InlineKeyboardButton(text=f'[1] Upgrade [{upgrade_cost}x 🍌]', callback_data='clicking upgrade max_banana')
   keyboard.add(upgrade_button)
   keyboard.add(back_button)
   text = f"""
Upgrades are permanent and can be leveled up multiple times
```
Current Banana: {banana}x 🍌
``````Shop
[1] {max_banana}/20 Sharper Tools
Get More Banana - {upgrade_cost}x 🍌
```
"""
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)