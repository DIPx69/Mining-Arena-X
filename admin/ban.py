import telebot
import asyncio
import os
import aiofiles
import json
import motor.motor_asyncio
import commands as command
import dns.resolver
from telebot import types
from telebot.async_telebot import *
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
async def ban(message):
   try:
    user_id = message.text.split()[1] 
    user_id = int(user_id)
    user = await bot.get_chat(user_id)
    username = user.username
    username = username.replace("_", "\\_")
   except:
     await bot.send_message(message.chat.id,f"User Not Found",parse_mode="Markdown")
     return 0
   try:
     admin_txt = message.text.split()[2:]
     admin_text_2 = " ".join(admin_txt)
   except Exception as e:
     text = str(e)
     print(text)
     await bot.send_message(message.chat.id,f"Enter Note Also",parse_mode="Markdown")
     return 0
   async with aiofiles.open('json_data/ban.json', 'r') as f:
     userlist = json.loads(await f.read())
   if user_id in [item['id'] for item in userlist]:
      await bot.send_message(message.chat.id,f"*The User Is Already Banned*\nUsername @{username}",parse_mode="Markdown")
   if user_id not in [item['id'] for item in userlist]:
     userlist.append({'id': user_id})
     try:
      await bot.send_message(message.chat.id,f"*The User Is Banned Successfully*\nNote: *{admin_text_2}*\nUsername @{username}",parse_mode="Markdown")
     except telebot.asyncio_helper.ApiTelegramException as e:
       e = str(e)
       await bot.send_message(message.chat.id,f"*[ERROR]*\nError: *{e}*\n\n*Username* @{username}",parse_mode="Markdown")
       return 0
     idx = str(user_id)
     database = client[idx]
     collection = database["data"]
     query = {}
     update = {'$set':{'ban':1}}
     await collection.update_one(query,update)
     await bot.send_message(user_id,f" - Your account has been banned due to violations\n - Blocking the bot will result in the deletion of all your *Game* Data\n\n - Note From *Administration*\n\n*{admin_text_2}*",parse_mode="Markdown")
     async with aiofiles.open('json_data/ban.json', 'w') as f:
       await f.write(json.dumps(userlist))