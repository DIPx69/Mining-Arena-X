import telebot
import os
import config
import random
import multiprocessing
import commands as command
import slash_command as slash
import json
import aiofiles
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)


async def profile(message):
  try:
    if message.reply_to_message is not None:
      getid = int(message.reply_to_message.from_user.id)
      getidx = str(message.reply_to_message.from_user.id)
    else:
      try:
        getid = int(message.text.split()[1])
        getidx = str(message.text.split()[1])
      except:
        getid = int(message.from_user.id)
        getidx = str(message.from_user.id)
    user = await bot.get_chat(getid)
    username = user.username
    db = client["user"]
    datack = db[getidx]
    datafind = await datack.find_one()
    ban = datafind["ban"]
    coin = await command.numtotext(datafind["coin"])
    lvl = datafind["lvl"]
    totalmine = datafind['mymine']
    xp = datafind['xp']
    prestigelvl = datafind['prestige']
    prestigecoin = datafind['prestigecoin']
    nxtlvlxp = datafind['nxtlvlxp']
    dice_won = datafind["dice_won"]
    dice_lose = datafind["dice_lose"]
    dice_total = dice_won+dice_lose
    dart_won = datafind["dart_won"]
    dart_lose = datafind["dart_lose"]
    dart_total = dart_won+dart_lose
    basketball_won = datafind["basketball_won"]
    basketball_lose = datafind["basketball_lose"]
    basketball_total = basketball_won+basketball_lose
    football_won = datafind["football_won"]
    football_lose = datafind["football_lose"]
    football_total = football_won+football_lose
    active_title = datafind["active_title"]
    if ban == 0:
      text = f"""
```
@{username} - {active_title}
``````Balance
- Coin: {coin}
- ID: {getidx}
``````Prestige
- Prestige Level: {prestigelvl}
- Prestige Coin: {prestigecoin}
``````MINING
- Total Mining: {await command.numtotext(totalmine)}
- Level: {lvl}
- XP BAR: {xp}/{nxtlvlxp}
``````GAME
- 🎲[{dice_won}||{dice_lose}||{dice_total}]
- 🎯[{dart_won}||{dart_lose}||{dart_total}]
- 🏀[{basketball_won}||{basketball_lose}||{basketball_total}]
- ⚽[{football_won}||{football_lose}||{football_total}]  
```
"""
    elif str(message.from_user.id) == getidx:
      text = f"""
```
You Can't View Your Profile Since Your Account Is Banned
```
"""
    else:
      text = f"""
```
You Can't View @{username}'s Profile Since His/Her Account Is Banned
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
  except Exception as e:
    print(str(e))
    text = f"""
```
User Not Found In Database
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")