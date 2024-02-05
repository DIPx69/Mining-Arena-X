import config
import random
import commands as command
import slash_command as slash
from telebot import types
import asyncio

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

async def percentage_helper(coin:int,text):
   if text.endswith("%"):
     percentage = int(text.replace("%",''))
     percentaged_coin = int(percentage / 100 * coin)
   elif text.isdigit():
     percentaged_coin = int(text)
   elif text.lower() == "max":
     percentaged_coin = coin
   elif text.lower() == "half":
     percentaged_coin = int(coin/2)
   else:
     percentaged_coin = await command.txttonum(text)
   return percentaged_coin


async def withdraw_coin(user_id:int,coin:int):
   db = client["user"]
   datack = db[str(user_id)]
   query = {}
   update = {'$inc': {"coin": coin,'bank': -coin}}
   print(update)
   await datack.update_one(query, update)
async def withdraw(message):
   status = await slash.check_lock(message)
   if status is True:
     return False
   get_commands = message.text.split()
   try:
     idx = str(message.from_user.id)
     db = client["user"]
     datack = db[idx]
     datafind = await datack.find_one()
     coin_amount = get_commands[1]
     coin_amount = await percentage_helper(datafind["bank"],coin_amount)
     print(coin_amount)
     max_bank = datafind["max_bank"]
     bank = datafind["bank"]
     coin = datafind["coin"]
   except:
     text = """
```
Please provide coin amount 
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return
   if datafind['bank'] < coin_amount:
     text = """
```
You can't withdraw because there isn't enough money in your bank
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return
   elif datafind["bank"] <= 0:
     text = """
```
You can't withdraw because there isn't enough money in your bank 
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return
   elif coin_amount <= 0:
     text = """
```
Amount needs to be greater than 0 
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return
   else:
     text = f"""
```
Withdrawn: {await command.numtotext(coin_amount)}
Pocket: {await command.numtotext(coin + coin_amount)}
Bank: {await command.numtotext(bank - coin_amount)}
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     await withdraw_coin(message.from_user.id,coin_amount)