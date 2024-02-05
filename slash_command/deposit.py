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

from slash_command import slash_lock

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


async def deposit_coin(user_id:int,coin:int):
   db = client["user"]
   datack = db[str(user_id)]
   query = {}
   update = {'$inc': {"coin": -coin,'bank': coin}}
   print(update)
   await datack.update_one(query, update)
async def deposit(message):
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
     coin_amount = await percentage_helper(datafind["coin"],coin_amount)
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
   if datafind['coin'] <= 0:
     text = """
```
You can't deposit because you don't have enough money
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return
   elif datafind['coin'] < coin_amount:
     text = """
```
You cannot deposit more money than what you currently have
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
   elif bank + coin_amount > max_bank:
     deposit_able = max_bank - bank
     if deposit_able > 0:
       text = f"""
```
Deposited: {await command.numtotext(deposit_able)}
Pocket: {await command.numtotext(coin - deposit_able)}
Bank: {await command.numtotext(bank + deposit_able)}
```
"""
       await bot.reply_to(message,text,parse_mode="Markdown")
       await deposit_coin(message.from_user.id,deposit_able)
     else:
       text = f"""
```
You already have a full bank
```
"""
       await bot.reply_to(message,text,parse_mode="Markdown")
   else:
     text = f"""
```
Deposited: {await command.numtotext(coin_amount)}
Pocket: {await command.numtotext(coin - coin_amount)}
Bank: {await command.numtotext(bank + coin_amount)}
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     await deposit_coin(message.from_user.id,coin_amount)