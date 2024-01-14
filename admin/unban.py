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
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)


async def unban(message):
  try:
    user_id = message.text.split()[1]
    user_id = int(user_id)
    user = await bot.get_chat(user_id)
    username = user.username
    username = username.replace("_", "\\_")
  except:
    await bot.send_message(message.chat.id, f"User Not Found", parse_mode="Markdown")
    return 0
  try:
    admin_txt = message.text.split()[2:]
    admin_text_2 = " ".join(admin_txt)
  except Exception as e:
    text = str(e)
    print(text)
    await bot.send_message(message.chat.id, f"Enter Note Also", parse_mode="Markdown")
    return 0
  async with aiofiles.open('json_data/ban.json', 'r') as f:
    userlist = json.loads(await f.read())
  if user_id in [item['id'] for item in userlist]:
    for i in range(len(userlist)):
      if userlist[i]["id"] == user_id:
        userlist.pop(i)
        break
    try:
      await bot.send_message(message.chat.id, f"*The User Is Unbanned*\nNote: *{admin_text_2}*\nUsername @{username}", parse_mode="Markdown")
    except telebot.asyncio_helper.ApiTelegramException as e:
      e = str(e)
      await bot.send_message(message.chat.id, f"*[ERROR]*\nError: *{e}*\n\n*Username* @{username}", parse_mode="Markdown")
      return 0
    idx = str(user_id)
    db = client["user"]
    datack = db[idx]
    query = {}
    update = {'$set': {'ban': 0}}
    await datack.update_one(query, update)
    await bot.send_message(user_id, f" - Your account has been unbanned\nClick *Account Banned 🚫* To Refresh The Window\n\n - Note From *Administration*\n\n*{admin_text_2}*", parse_mode="Markdown")
  else:
    if user_id not in [item['id'] for item in userlist]:
      await bot.send_message(message.chat.id, f"*User Not Found In Ban Database*", parse_mode="Markdown")
  async with aiofiles.open('json_data/ban.json', 'w') as f:
    await f.write(json.dumps(userlist))
