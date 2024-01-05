import telebot
import os
import pymongo
import commands as command
import dns.resolver
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
async def switch_lvl(call):
   level = int(call.data.split()[1])
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   query = {}
   update = {"$set":{"autominelvl": level}}
   await datack.update_one(query,update)
   await command.upgrade_menu(call)
async def page_list(call,total_page:int):
   keyboard = types.InlineKeyboardMarkup(row_width=3)
   pages = [types.InlineKeyboardButton(text=f"{i}", callback_data=f"adjust {i}") for i in range(1,total_page+1)]
   keyboard.add(*pages)
   back = types.InlineKeyboardButton(text='🔙 Back', callback_data='adjust 1')
   keyboard.add(back)
   await bot.edit_message_text(f"Select Your Page Number",call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown",reply_markup=keyboard)
async def switch_pickaxe(call):
  row_buttons = []
  get_page_number = int(call.data.split()[1])
  idx = str(call.from_user.id)
  db = client["user"]
  datack = db[idx]
  datafind = await datack.find_one()
  autominelvl = datafind["maximum_automine_lvl"]
  automineon = datafind["automineon"]
  keyboard = types.InlineKeyboardMarkup(row_width=4)
  levels = [i for i in range(1,autominelvl+1)]
  level_data = {}
  for page_num, start_index in enumerate(range(0, len(levels), 50), start=1):
     page = levels[start_index:start_index + 50]
     json_data = {str(page_num):page}
     level_data[str(page_num)] = page
  total_page = len(level_data)
  level_json = level_data[str(get_page_number)]
  if automineon == 0:
    for i in level_json:
      button = types.InlineKeyboardButton(text=f"{i}", callback_data=f"minelvl {i}")
      row_buttons.append(button)
    keyboard.add(*row_buttons)
    if get_page_number != total_page:
     next_emoji = "⏭️"
    else:
     next_emoji = ""
    if get_page_number != 1:
     prev_emoji = "⏮️"
    else:
     prev_emoji = ""
    next_button = types.InlineKeyboardButton(text=f'{next_emoji}',callback_data=f'adjust {get_page_number+1}')
    prev_button = types.InlineKeyboardButton(text=f'{prev_emoji}',callback_data=f'adjust {get_page_number-1}')
    switch_page_button = types.InlineKeyboardButton(text=f'{get_page_number}/{total_page}',callback_data=f'page_list {total_page}')
    keyboard.add(prev_button,switch_page_button,next_button)
  else:
   warning = types.InlineKeyboardButton(text=f"You Can't Adjust Level While Mining", callback_data=f"x")
   keyboard.add(warning) 
  back = types.InlineKeyboardButton(text='🔙 Back', callback_data='upgrade_mine')
  keyboard.add(back)
  await bot.edit_message_text(f"Select Your Level\n\nPage *{get_page_number}* Of *{total_page}*",call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown",reply_markup=keyboard)