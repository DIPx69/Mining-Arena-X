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

async def balance(message):
   get_commands = message.text.split()
   idx = str(message.from_user.id)
   username = "@" + message.from_user.username
   try:
     if int(len(get_commands)) > 1:
       args = message.text.split()[1]
       if args.startswith("@"):
         uid = await command.find_uid(args)
         if uid:
           idx = str(uid)
           username = message.text.split()[1]
         else:
           raise ValueError("Username Not Found")
       elif args.isdigit():
         idx = str(message.text.split()[1])
         user = await bot.get_chat(int(idx))
         username = user.username
       else:  
         raise ValueError("Username Not Found") 
   except Exception as e:     
     print(str(e))
     text = f"""
```
User Not Found In Database
```
"""
     await bot.reply_to(message, text, parse_mode="Markdown")
     return
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = await command.numtotext(datafind["coin"])
   bank = await command.numtotext(datafind["bank"])
   max_bank = await command.numtotext(datafind["max_bank"])
   bank_full_percentage = f"{datafind['bank'] / datafind['max_bank'] * 100:.1f}"
   text = f"""
```Balance
- Username: {username}
- Pocket: {coin}
- Bank: {bank} ({bank_full_percentage}% full)
- Bankspace: {max_bank}
```
"""
   await bot.reply_to(message,text,parse_mode="Markdown")