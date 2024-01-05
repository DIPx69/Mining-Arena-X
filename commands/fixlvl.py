import telebot
from telebot.types import ForceReply, ReplyKeyboardMarkup
import os
import config
import random
import commands as command
import json
import aiofiles
import asyncio
import time
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
import motor.motor_asyncio
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)

async def fixlvl(message):
  query = {}
  idx = str(message.from_user.id)
  db = client["user"]
  datack = db[idx]
  i = 2
  totalup = 0
  send = await bot.send_message(message.chat.id,"*Trying To Fix Your Bulk XP*",parse_mode="Markdown")
  while i > 0:
    datafind = await datack.find_one()
    lvl = datafind['lvl']
    xp = datafind['xp']
    nxtlvlxp = datafind['nxtlvlxp']
    if xp > nxtlvlxp:
      totalup += 1
      extra = xp - nxtlvlxp
      update = {"$inc": {"lvl": 1,"nxtlvlxp": 50},"$set": {"xp": extra}}
      await datack.update_one(query, update)
      await bot.edit_message_text(
        f"*Trying To Fix Your Bulk XP*\nTotal Level Up: *{totalup}* Times",message.chat.id,
        send.message_id,
        parse_mode="Markdown")
    else:
      await bot.edit_message_text(
        f"*Level Fixed Check Profile*\nTotal Level Up: *{totalup}* Times",
        message.chat.id,
        send.message_id,
        parse_mode="Markdown")