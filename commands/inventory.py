import telebot
import os
import commands as command
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
async def inventory(call):
    idx = str(call.from_user.id)
    db = client["user"]
    datack = db[idx]
    datafind = await datack.find_one()
    await command.mine_check(call,datafind)
    iron = datafind['iron']
    coal = datafind['coal']
    silver = datafind['silver']
    crimsteel = datafind['crimsteel']
    gold = datafind['gold']
    mythan = datafind['mythan']
    magic = datafind['magic']
    minex = datafind['minex']
    xpboost = datafind['xpboost']
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
    header = "MINE INVENTORY"
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
    keyboard = types.InlineKeyboardMarkup() 
    farm_inventory = types.InlineKeyboardButton(text='👨🏻‍🌾 Farm Inventory',callback_data='inventory farm')
    buy_button = types.InlineKeyboardButton(text='🔰 Buy',callback_data='buy menu inventory')
    sell_button = types.InlineKeyboardButton(text='🔰 Sell',callback_data='sell menu inventory')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(farm_inventory)
    keyboard.add(buy_button,sell_button)
    keyboard.add(back_button)
    await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup = keyboard)
async def inventory_farm(call):
    idx = str(call.from_user.id)
    db = client["user"]
    datack = db[idx]
    datafind = await datack.find_one()
    await command.mine_check(call,datafind)
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
    header = "FARM INVENTORY"
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
    keyboard = types.InlineKeyboardMarkup() 
    mine_inventory = types.InlineKeyboardButton(text='⛏️ Mine Inventory',callback_data='inventory mine')
    buy_button = types.InlineKeyboardButton(text='🧺 Buy',callback_data='farm_shop seeds_buy inventory')
    sell_button = types.InlineKeyboardButton(text='🧺 Sell',callback_data='farm_shop sell_menu inventory')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(mine_inventory)
    keyboard.add(buy_button,sell_button)
    keyboard.add(back_button)
    await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup = keyboard)