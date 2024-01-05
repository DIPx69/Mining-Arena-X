import telebot
import asyncio
import os
import motor.motor_asyncio
import commands as command
import admin
import dns.resolver
from telebot import types
from telebot.types import Dice
from telebot.async_telebot import *
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
async def adminmenu(call):
    keyboard = types.InlineKeyboardMarkup()
    list_button = types.InlineKeyboardButton(text='👤 User List',callback_data='user_list')
    message_to_user_button = types.InlineKeyboardButton(text='💌 Message To User',callback_data='message_to_user')
    message_to_all_user_button = types.InlineKeyboardButton(text='📪 Message To All User',callback_data='message_to_all_user')
    ban_list_button = types.InlineKeyboardButton(text='🚫 Ban List',callback_data='ban_list')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(list_button)
    keyboard.add(message_to_user_button,message_to_all_user_button)
    keyboard.add(ban_list_button)
    keyboard.add(back_button)
    await bot.edit_message_text("*Select Option*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)