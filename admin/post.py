import asyncio
import commands as command
import admin
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def post_preview(message):
  try:
    message_get = message.text.split()[1]
    mode = int(message_get)
  except:
    await bot.send_message(message.chat.id,"Enter Mode Number",parse_mode="Markdown")
    return 0
  async with aiofiles.open("json_data/post_config.json", 'r') as f:
     data = json.loads(await f.read())
  keyboard = types.InlineKeyboardMarkup()
  text = data["text"]
  button_text = data["button_text"]
  button_link = data["button_link"]
  photo = data["photo"]
  photo_url = data["photo_url"]
  username = data["username"]
  message_button = types.InlineKeyboardButton(text=button_text,url=button_link)
  group_button = types.InlineKeyboardButton(text="💬 JOIN OFFICIAL GROUP CHAT",url="https://t.me/MinibngArenaChats")
  keyboard.add(message_button)
  if mode == 1 and message.from_user.id == ownerid and photo == False:
     text += f"\n\nWill Post In {username}"
     await bot.send_message(message.chat.id,text,parse_mode="Markdown",reply_markup=keyboard)
  if mode == 1 and message.from_user.id == ownerid and photo:
     text += f"\n\nWill Post In {username}"
     await bot.send_photo(message.chat.id,photo=photo_url,caption=text,parse_mode="Markdown",reply_markup=keyboard)
  if mode == 2 and message.from_user.id == ownerid and photo == False:
     await bot.send_message(username,text,parse_mode="Markdown",reply_markup=keyboard)
  if mode == 2 and message.from_user.id == ownerid and photo:
     await bot.send_photo(username,photo=photo_url,caption=text,parse_mode="Markdown",reply_markup=keyboard)
  