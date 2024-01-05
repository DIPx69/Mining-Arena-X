import telebot
import os
import time
import dns.resolver
import asyncio
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
os.environ["userlist"] = ""
# User List Code
async def fetch_user_data(user):
  userdata = await bot.get_chat(user)
  username = userdata.username
  username = username.replace("_", "\\_")
  os.environ["userlist"] += f" \- @{username}  `{user}`\n"
async def userlist(call):
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='admin_panel')
   keyboard.add(back_button)
   await bot.edit_message_text("Generating User List",call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)
   userlist_x = client["user"]
   userlist = await userlist_x.list_collection_names()
   os.environ["userlist"] += f"Total User: *{len(userlist)}*\n"
   start = time.time()
   user_info = []
   tasks = [fetch_user_data(user) for user in userlist]
   await asyncio.gather(*tasks)
   end = time.time()
   totaltime = int(end - start)
   os.environ["userlist"] += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\nIt Took *{totaltime}* Second To Make This User List"
   await bot.edit_message_text(os.environ["userlist"],call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)
   os.environ["userlist"] = ""