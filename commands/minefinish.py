import telebot
import os
import time
import dns.resolver
import asyncio
import aiofiles
import json
import commands as command
from telebot import types
import motor.motor_asyncio
import dns.resolver
from telebot.types import ForceReply, ReplyKeyboardMarkup
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
async def minefinish(call):
  keyboard = types.InlineKeyboardMarkup()
  delete_button = types.InlineKeyboardButton(text=f'✖️ DELETE ✖️', callback_data='delete')
  keyboard.add(delete_button) 
  try:
    filename = f'json data/active_window.json'
    user_id = call.from_user.id
    async with aiofiles.open(filename, 'r') as f:
       window = json.loads(await f.read())
    if window[str(user_id)]['message_id']:
      message_id = window[str(user_id)]['message_id']
    await bot.send_message(call.from_user.id,"*🔨 Mining Operation Complete! 🔨\n\nCongratulations! Your mining operation has finished successfully*",parse_mode="Markdown",reply_to_message_id=message_id,reply_markup=keyboard)
    await command.minemenu(call,int(message_id))
  except:
    await bot.send_message(call.from_user.id,"*🔨 Mining Operation Complete! 🔨\n\nCongratulations! Your mining ope has finished successfully*\nTry Opening Window By /start",parse_mode="Markdown",reply_markup=keyboard)