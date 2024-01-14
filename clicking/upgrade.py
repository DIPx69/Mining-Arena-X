import random
import commands as command

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023

async def upgrade(call,name:str):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   if name == "max_banana":
     max_banana = datafind['max_banana']
     banana = datafind['banana']
     upgrade_cost = max_banana * 20
     if upgrade_cost <= banana:
       update = {'$inc': {'banana': -upgrade_cost,"max_banana": +1}}
       query = {}
       await datack.update_one(query,update)
       return True
     else:
       await bot.answer_callback_query(call.id, text=f"You Don't Have Enough Banana To Upgrade", show_alert=True)
       return False