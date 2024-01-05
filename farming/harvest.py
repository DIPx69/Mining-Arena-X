import telebot
import asyncio
import os
import json
import time 
import aiofiles
import config 
import random
import commands as command
import farming as farm
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

async def harvest(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   tiles = await farm.farm_json_maker(datafind)
   text = ""
   updated_items = {}
   remove_tile = {}
   any_harvest = 0
   harvested_item = {
    'potato': 0,
    'potato_seed': 0,
    'corn': 0,
    'corn_seed': 0,
    'carrot': 0,
    'carrot_seed': 0,
    'broccoli': 0,
    'broccoli_seed': 0,
    'watermelon': 0,
    'watermelon_seed': 0
}
   seed_dict = {
    "potato": "potato_seed",
    "corn": "corn_seed",
    "carrot": "carrot_seed",
    "broccoli": "broccoli_seed",
    "watermelon": "watermelon_seed"}
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
   for tile in tiles:
     now_time = int(time.time())
     tile_name = datafind[f"tile_name_{tile}"]
     tile_time = datafind[f"tile_{tile}"]
     if now_time >= tile_time and tile_time != 0:
       remove_tile.update({f"tile_{tile}": 0,f"tile_name_{tile}": "None"})
       any_harvest = 1
       seeds = random.randint(1,2)
       plant = 1
       seed_name = seed_dict[tile_name].title()
       seed_name = seed_name.replace("_", " ")
       harvested_item[tile_name] += plant
       namex = seed_dict[tile_name]
       harvested_item[namex] += seeds
   text = "You successfully harvested\n\n"
   for key,value in harvested_item.items():
     keyx = key.replace("_"," ")
     if value != 0:
       text += f" - {value}x {icons[key]} {keyx.title()}\n"
   if any_harvest == 0:
     await bot.answer_callback_query(call.id,text="You have no plants that are ready to harvest!", show_alert=True)
     return False
   else:
     update = {'$inc':harvested_item,'$set':remove_tile}
     query = {}
     await datack.update_one(query, update)
     delete_button = types.InlineKeyboardButton(text=f'DELETE', callback_data='delete')
     keyboard.add(delete_button) 
     await bot.send_message(call.from_user.id,text,parse_mode="Markdown",reply_markup=keyboard)
     return True