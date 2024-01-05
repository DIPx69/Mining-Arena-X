import telebot
import asyncio
import os
import json
import aiofiles
import config 
import commands as command
import farming as farm
import admin
from telebot import types
from telebot.types import Dice
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
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
   farming_text = f"""
   {call.from_user.first_name} {call.from_user.last_name}'s Farm

Progress
"""
   farming_text += await farm.progress_maker(tiles)
   try:
    await bot.edit_message_text(farming_text,call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)
   except:
     print(" ")
