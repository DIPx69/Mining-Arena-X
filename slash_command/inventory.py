import telebot
import os
import commands as command
import slash_command as slash
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

from slash_command import slash_lock

async def predict_word(prefix):
   available_item = ["farm","mine"]
   matches = [name for name in available_item if name.startswith(prefix)]
   if matches:
     return matches[0]
   else:
     return False


async def view_inventory(message,mode:str):
   idx = str(message.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   keyboard = types.InlineKeyboardMarkup()
   if mode == "mine":
    button = types.InlineKeyboardButton(text='FARM INVENTORY',callback_data='slash inventory farm')
    keyboard.add(button)
    iron = datafind['iron']
    coal = datafind['coal']
    silver = datafind['silver']
    crimsteel = datafind['crimsteel']
    gold = datafind['gold']
    mythan = datafind['mythan']
    magic = datafind['magic']
    minex = datafind['minex']
    xpboost = datafind['xpboost']
    if message.chat.type == "private":
      header = "MINE INVENTORY"
    else:
      header = "       MINE INVENTORY"
    text = f"""```
{header}
``````ORES
Iron: {await command.numtotext(iron)}
Coal: {await command.numtotext(coal)}
Silver: {await command.numtotext(silver)}
Crimsteel: {await command.numtotext(crimsteel)}
Gold: {await command.numtotext(gold)}
Mythan: {await command.numtotext(mythan)}
Magic: {await command.numtotext(magic)}
``````ITEMS
MineX: {await command.numtotext(minex)}
XP Boost: {await command.numtotext(xpboost)}
``` """
    await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard) 
   else:
    button = types.InlineKeyboardButton(text='MINE INVENTORY',callback_data='slash inventory mine')
    keyboard.add(button)
    potato = datafind['potato']
    corn = datafind['corn']
    carrot = datafind['carrot']
    broccoli = datafind['broccoli']
    watermelon = datafind['watermelon']
    potato_seed = datafind['potato_seed']
    corn_seed = datafind['corn_seed']
    carrot_seed = datafind['carrot_seed']
    broccoli_seed = datafind['broccoli_seed']
    watermelon_seed = datafind['watermelon_seed']
    water = datafind["water"]
    if message.chat.type == "private":
      header = "FARM INVENTORY"
    else:
      header = "       FARM INVENTORY"
    text = f"""```
{header}
``````Tools
💦 Water: {await command.numtotext(water)}
``````Plants
🥔 Potato: {await command.numtotext(potato)}
🌽 Corn: {await command.numtotext(corn)}
🥕 Carrot: {await command.numtotext(carrot)}
🥦 Broccoli: {await command.numtotext(broccoli)}
🍉 Watermelon: {await command.numtotext(watermelon)}
``````Seeds
🥔 Seeds: {await command.numtotext(potato_seed)} 
🌽 Seeds: {await command.numtotext(corn_seed)}
🥕 Seeds: {await command.numtotext(carrot_seed)}
🥦 Seeds: {await command.numtotext(broccoli_seed)}
🍉 Seeds: {await command.numtotext(watermelon_seed)}
```
"""
    await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard) 

async def view_inventory_call(call,mode:str):
   status = await slash.is_commander(call)
   if status:
     return False
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   keyboard = types.InlineKeyboardMarkup()
   if mode == "mine":
    button = types.InlineKeyboardButton(text='FARM INVENTORY',callback_data='slash inventory farm')
    keyboard.add(button)
    iron = datafind['iron']
    coal = datafind['coal']
    silver = datafind['silver']
    crimsteel = datafind['crimsteel']
    gold = datafind['gold']
    mythan = datafind['mythan']
    magic = datafind['magic']
    minex = datafind['minex']
    xpboost = datafind['xpboost']
    if call.message.chat.type == "private":
      header = "MINE INVENTORY"
    else:
      header = "       MINE INVENTORY"
    text = f"""```
{header}
``````ORES
Iron: {await command.numtotext(iron)}
Coal: {await command.numtotext(coal)}
Silver: {await command.numtotext(silver)}
Crimsteel: {await command.numtotext(crimsteel)}
Gold: {await command.numtotext(gold)}
Mythan: {await command.numtotext(mythan)}
Magic: {await command.numtotext(magic)}
``````ITEMS
MineX: {await command.numtotext(minex)}
XP Boost: {await command.numtotext(xpboost)}
``` """
    await bot.edit_message_text(text,call.message.chat.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
   else:
    button = types.InlineKeyboardButton(text='MINE INVENTORY',callback_data='slash inventory mine')
    keyboard.add(button)
    potato = datafind['potato']
    corn = datafind['corn']
    carrot = datafind['carrot']
    broccoli = datafind['broccoli']
    watermelon = datafind['watermelon']
    potato_seed = datafind['potato_seed']
    corn_seed = datafind['corn_seed']
    carrot_seed = datafind['carrot_seed']
    broccoli_seed = datafind['broccoli_seed']
    watermelon_seed = datafind['watermelon_seed']
    water = datafind["water"]
    if call.message.chat.type == "private":
      header = "FARM INVENTORY"
    else:
      header = "       FARM INVENTORY"
    text = f"""```
{header}
``````Tools
💦 Water: {await command.numtotext(water)}
``````Plants
🥔 Potato: {await command.numtotext(potato)}
🌽 Corn: {await command.numtotext(corn)}
🥕 Carrot: {await command.numtotext(carrot)}
🥦 Broccoli: {await command.numtotext(broccoli)}
🍉 Watermelon: {await command.numtotext(watermelon)}
``````Seeds
🥔 Seeds: {await command.numtotext(potato_seed)} 
🌽 Seeds: {await command.numtotext(corn_seed)}
🥕 Seeds: {await command.numtotext(carrot_seed)}
🥦 Seeds: {await command.numtotext(broccoli_seed)}
🍉 Seeds: {await command.numtotext(watermelon_seed)}
```
"""
    await bot.edit_message_text(text,call.message.chat.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard) 
async def inventory(message):
   status = await slash.check_lock(message)
   if status is True:
     return False
   try:
    inventory_mode = message.text.split()[1]
    inventory_mode = await predict_word(inventory_mode)
    if inventory_mode == False:
       raise InventoryError("Inventory Not Found")
   except:
     inventory_mode = "mine"
   await view_inventory(message,inventory_mode)