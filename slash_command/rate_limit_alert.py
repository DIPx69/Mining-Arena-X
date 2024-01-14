import commands as command
import slash_command as slash

import asyncio
from telebot import types

from commands.set_up import client
from commands.set_up import bot
from games.basketball import bot_rate
async def send_alert(message,retry_after):
   try:
    text = f"""
```
Rate Limit Alert
``````
This Group Has Been Rate Limited For {retry_after} Seconds
```
"""
    await bot_rate_limit.send_message(message.chat.id,text,parse_mode="Markdown")
   except:
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Add Rate Limit Alert Bot',url='http://t.me/ratelimitalertbot?startgroup=botstart')
    keyboard.add(button)
    if message.chat.username is not None:
      username = "@" + message.chat.username
    else:
      username = message.chat.id
    text = f"""
```
Rate Limit Alert
``````
{username} Has Been Rate Limited For {retry_after} Second 
```
"""
    await bot.send_message(message.from_user.id,text,parse_mode="Markdown",reply_markup=keyboard)