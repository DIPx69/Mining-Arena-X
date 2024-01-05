import telebot
import os
import config
import random
import commands as command
import json
import aiofiles
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
async def sell_all(call,reference,edit=True):
  idx = str(call.from_user.id)
  db = client["user"]
  datack = db[idx]
  datafind = await datack.find_one()
  coin = datafind["coin"]
  iron = datafind['iron']
  coal = datafind["coal"]
  silver = datafind["silver"]
  crimsteel = datafind["crimsteel"]
  gold = datafind["gold"]
  mythan = datafind["mythan"]
  magic = datafind["magic"]
  total = 0
  text = ""
  items = {
    "Iron": iron,
    "Coal": coal,
    "Silver": silver,
    "Crimsteel": crimsteel,
    "Gold": gold,
    "Mythan": mythan,
    "Magic": magic}
  updated_items = {}
  for item_name, item_quantity in items.items():
     if item_quantity > 0:
       price_var_name = f"{item_name.lower()}price"
       item_price = getattr(config, price_var_name)
       total += item_quantity * item_price
       item_str = await command.numtotext(item_quantity)
       text += f"{item_str} {item_name}\n"
       updated_items[item_name.lower()] = 0
  query = {}
  total_text = await command.numtotext(total)
  total_coin = await command.numtotext(total+coin)
  if total > 0:
    update = {'$inc': {'coin': total},'$set':updated_items}
    await datack.update_one(query, update)
    await bot.answer_callback_query(call.id,text=f"You Have Sold\n{text}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}", show_alert=True)
    if reference == "inventory":
     reference = "inventory mine"
    await command.sellmenu(call,reference)
  else:
     await bot.answer_callback_query(call.id,text=f"You Sold Nothing", show_alert=True)
     if edit:
       await command.sellmenu(call,reference)
async def sell_item(call,item_key,reference,edit=True):
   item_name = item_key.capitalize()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   item_quantity = datafind[item_key]
   if item_quantity > 0:
     price = getattr(config, f"{item_name.lower()}price")
     total = item_quantity * price
     total_coin = await command.numtotext(coin + total)
     total_text = await command.numtotext(total)
     query = {}
     update = {'$inc': {'coin': total},"$set":{item_key: 0}}
     await datack.update_one(query, update)
     item_quantity_str = await command.numtotext(item_quantity)
     await bot.answer_callback_query(call.id,text=f"You Have Sold {item_quantity_str} {item_name}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}",show_alert=True)
     if edit:
       if reference == "inventory":
         reference = "inventory mine"
       await command.sellmenu(call,reference)
   else:
     await bot.answer_callback_query(call.id, text=f"You Don't Have Any {item_name} To Sell", show_alert=True)