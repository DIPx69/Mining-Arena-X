import telebot
import os
import config
from telebot import  types
import commands as command
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

async def farm_shop(call,reference):
   keyboard = types.InlineKeyboardMarkup()
   buy_button = types.InlineKeyboardButton(text='🧺 Buy',callback_data=f'farm_shop seeds_buy {reference}')
   sell_button = types.InlineKeyboardButton(text='🧺 Sell',callback_data=f'farm_shop sell_menu {reference}')
   if reference == "inventory":
     reference = "inventory farm"
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data=reference)
   keyboard.add(buy_button,sell_button)
   keyboard.add(home_button,back_button)
   await bot.edit_message_text("*[FARM SHOP]*\n\n*Select Option*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
