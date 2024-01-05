import telebot
import asyncio
import os
import json
import time 
import aiofiles
import config 
import random
import commands as command
import admin
from telebot import types
from telebot.types import Dice
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
from dotenv import load_dotenv
from telebot import formatting
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
async def time_left(timestamp: int):
   if timestamp > int(time.time()):
     time_left = int(timestamp - time.time())
     days = time_left // (24 * 3600)
     hours = (time_left % (24 * 3600)) // 3600
     minutes = (time_left % 3600) // 60
     seconds = time_left % 60
     if days > 0:
       time_left = f"tile ready in {days}d:{hours}h:{minutes}m:{seconds}s"
     elif hours > 0:
       time_left = f"tile ready in {hours}h:{minutes}m:{seconds}s"
     elif minutes > 0:
       time_left = f"tile ready in {minutes}m:{seconds}s"
     else:
       time_left = f"tile ready in {seconds}s"
   else:
     time_left = "tile ready to harvest"
   return str(time_left)
async def progress_maker(tiles):
   icons = {
    "potato": "🥔",
    "potato_seed": "🥔",
    "corn": "🌽",
    "corn_seed": "🌽",
    "carrot": "🥕",
    "carrot_seed": "🥕",
    "broccoli": "🥦",
    "broccoli_seed": "🥦",
    "watermelon": "🍉",
    "watermelon_seed": "🍉",
    "None": "🚫",
    "water": "💦"
}
   farm_text = ""
   for tile in tiles:
     progress = await time_left(int(tiles[tile]["time"]))
     name = tiles[tile]['name']
     icon = icons[name]
     if name == "None":
       text = f"{tile}    {icon} Empty Tile\n"
     elif name == "water":
       text = f"{tile}    {icon} Waterd Tile\n"
     else:
       text = f"{tile}    {icon} {name.title()} {progress}\n"
     farm_text += text
   return farm_text
async def farm_json_maker(data):
   farm_json = {}
   for tile in range(1, 10):
    farm_json[str(tile)] = {
        "name": data[f"tile_name_{tile}"],
        "time": data[f"tile_{tile}"]
    }
   return farm_json
async def use_item(call,item,tile, notification=True):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   quantity = datafind[item]
   if quantity <= 0:
     if notification:
       await bot.answer_callback_query(call.id, text=f"Sorry, you don't have this item", show_alert=True)
   else:
     now_time = int(time.time())
     tile_name = datafind[f"tile_name_{tile}"]
     tile_time = datafind[f"tile_{tile}"] 
     plant_list = [
    "potato",
    "corn",
    "carrot",
    "broccoli",
    "watermelon"]
     plant_dict = {
    "potato_seed": "potato",
    "corn_seed": "corn",
    "carrot_seed": "carrot",
    "broccoli_seed": "broccoli",
    "watermelon_seed": "watermelon"}
     seed_list = [
    "potato_seed",
    "corn_seed",
    "carrot_seed",
    "broccoli_seed",
    "watermelon_seed"
]
     if item in seed_list:
       if tile_name == "None":
         if notification:
           await bot.answer_callback_query(call.id, text=f"Please water the tile first", show_alert=True)
         return False
       elif tile_name in plant_list and now_time >= tile_time:
         if notification:
           await bot.answer_callback_query(call.id, text=f"You can only plant seeds on an empty tile that is watered", show_alert=True)
         return False
       elif tile_name == "water":
         query = {}
         plant_name = plant_dict[item]
         plant_cooldown = f"{plant_name}_cooldown"
         plant_cooldown = getattr(config, plant_cooldown)
         next_end_time = int(time.time()) + plant_cooldown
         if item in seed_list:
           update = {
    "$set": {
        f"tile_name_{tile}": plant_dict[item],
        f"tile_{tile}": next_end_time
    },
    "$inc": {
        item: -1
    }
}
         await datack.update_one(query,update)
         return True
       else:
        if notification:
          await bot.answer_callback_query(call.id, text=f"You can only plant seeds on an empty tile that is watered", show_alert=True)
        return False
     if item == "water":
       item_list = ["potato","corn","carrot","broccoli","watermelon","water"]
       if tile_name in item_list:
         if notification:
           await bot.answer_callback_query(call.id, text=f"You can only use Water on empty tiles", show_alert=True)
         return False
       elif tile_name in seed_list and now_time >= tile_time:
         if notification:
           await bot.answer_callback_query(call.id, text=f"Water can only be used on empty tiles", show_alert=True)
         return False
       else:
         query = {}
         chance = random.random()
         if chance <= 0.1:
           keyboard = types.InlineKeyboardMarkup()
           delete_button = types.InlineKeyboardButton(text='Delete',callback_data=f'delete')
           keyboard.add(delete_button)
           text = "- You have lost 1 💧 *Water*\n- Tip: There is a 10% chance of losing water"
           await bot.send_message(call.from_user.id,text,parse_mode="Markdown",reply_markup=keyboard)
           data = -1
         else:
           data = 0
         update = {"$set":{f"tile_name_{tile}":"water"},"$inc":{"water": data}}
         await datack.update_one(query,update)
         return True
async def use(call,name,markup=True):
   permanent_name = name
   keyboard = types.InlineKeyboardMarkup()

   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   tiles = await farm_json_maker(datafind)
   quantity = datafind[name]
   name_ = name.replace("_", " ")
   seed_tools = {
    "water": "💦",
    "potato_seed": "🥔",
    "corn_seed": "🌽",
    "carrot_seed": "🥕",
    "broccoli_seed": "🥦",
    "watermelon_seed": "🍉"}
   del seed_tools[permanent_name]
   icons = {
    "potato": "🥔",
    "potato_seed": "🥔",
    "corn": "🌽",
    "corn_seed": "🌽",
    "carrot": "🥕",
    "carrot_seed": "🥕",
    "broccoli": "🥦",
    "broccoli_seed": "🥦",
    "watermelon": "🍉",
    "watermelon_seed": "🍉",
    "None": "🚫",
    "water": "💦"
}
   farm_text = f"*Using*\n{icons[name]} {name_.title()} ({quantity})\n\nProgress\n"
   farm_text += await progress_maker(tiles)
   back_button = types.InlineKeyboardButton(text='🔙 Go Back',callback_data='use item')
   refresh_button = types.InlineKeyboardButton(text='🔃 Refresh',callback_data=f'use {permanent_name}')
   all_button = types.InlineKeyboardButton(text='All',callback_data=f'xuse_all {permanent_name}')
   main_button = types.InlineKeyboardButton(text='🏡 Home',callback_data=f'main_menu')
   buttons = []
   for index,tile in enumerate(tiles,1):
     button = types.InlineKeyboardButton(text=f'{index}',callback_data=f'use_item {permanent_name} {index}')
     buttons.append(button)
   keyboard.add(*buttons)
   items = {}
   for item in seed_tools.keys():
     if datafind[item] > 0:
       items.update({item: {"icon": icons[item]}})
   buttons = []
   for item in items.keys():
     button = types.InlineKeyboardButton(text=f"{items[item]['icon']}",callback_data=f'use {item}')
     buttons.append(button)
   keyboard.add(all_button)
   keyboard.add(*buttons)
   keyboard.add(refresh_button,main_button,back_button)
   try:
    if markup:
     await bot.edit_message_text(farm_text,call.from_user.id,call.message.id, parse_mode="Markdown",reply_markup=keyboard)
    else:
     await bot.edit_message_text(farm_text,call.from_user.id,call.message.id, parse_mode="Markdown")
   except:
     ...
async def all_items(call):
   keyboard = types.InlineKeyboardMarkup(row_width=4)
   icons = {
    "water": "💦",
    "potato": "🥔",
    "potato_seed": "🥔",
    "corn": "🌽",
    "corn_seed": "🌽",
    "carrot": "🥕",
    "carrot_seed": "🥕",
    "broccoli": "🥦",
    "broccoli_seed": "🥦",
    "watermelon": "🍉",
    "watermelon_seed": "🍉"
}
   seed_tools = {
    "water": "💦",
    "potato_seed": "🥔",
    "corn_seed": "🌽",
    "carrot_seed": "🥕",
    "broccoli_seed": "🥦",
    "watermelon_seed": "🍉"
}
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()

   water = datafind["water"]
   potato_seed = datafind["potato_seed"]
   potato = datafind["potato"]
   items = {}
   for item in seed_tools.keys():
     if datafind[item] > 0:
       items.update({item: {"icon": icons[item]}})
   buttons = []
   for item in items.keys():
     button = types.InlineKeyboardButton(text=f"{items[item]['icon']}",callback_data=f'use {item}')
     buttons.append(button)
   keyboard.add(*buttons)
   farming_text = f"*[Tools]*\n"
   water = str(water)
   water = water.replace("-","\-")
   farming_text += f"💦 Water *\({water}\)*\n*Tips: Visit Daily To Claim Your 💦 Water*"
   farming_text +=  "\n\n*[Seeds]*\n"
   seeds = {
    "potato_seed": "🥔 Potato Seeds",
    "corn_seed": "🌽 Corn Seeds",
    "carrot_seed": "🥕 Carrot Seeds",
    "broccoli_seed": "🥦 Broccoli Seeds",
    "watermelon_seed": "🍉 Watermelon Seeds"}
   for seed, seed_name in seeds.items():
    count = datafind[seed]
    count = str(count)
    count = count.replace("-","\-")
    farming_text += f"{seed_name} *\({count}\)*\n"
   back_button = types.InlineKeyboardButton(text='🔙 Go Back',callback_data='farming_menu')
   home_button = types.InlineKeyboardButton(text='🏡 Home',callback_data='main_menu')
   keyboard.add(home_button,back_button)
   await bot.edit_message_text(farming_text,call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)
