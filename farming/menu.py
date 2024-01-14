import asyncio
import time 
import random

import commands as command
import farming as farm
import admin

from telebot import types
from telebot import formatting

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def menu(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   await command.mine_check(call,datafind)
   tiles = await farm.farm_json_maker(datafind)
   use_item = types.InlineKeyboardButton(text='Use Item',callback_data='use item')
   harvest = types.InlineKeyboardButton(text='Harvest All',callback_data='harvest')
   farm_refresh = types.InlineKeyboardButton(text='🔃',callback_data='farm_refresh')
   back_button = types.InlineKeyboardButton(text='🔙 Go Back',callback_data='main_menu')
   keyboard.add(use_item,harvest)
   keyboard.add(farm_refresh,back_button)
   name = ""
   if call.from_user.first_name is not None:
     name += call.from_user.first_name
   if call.from_user.last_name is not None:
     name += " " + call.from_user.last_name
   if name == "":
     name = "God"
   farming_text = f"""
```
{name}'s Farm
```
Progress
"""
   farming_text += await farm.progress_maker(tiles)
   try:
    await bot.edit_message_text(farming_text,call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)
   except:
     print(" ")
