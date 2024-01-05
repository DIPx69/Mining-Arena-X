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
    txt =f"*[INVENTORY]*\n - Iron: *{iron}*\n - Coal: *{coal}*\n - Silver: *{silver}*\n - Crimsteel: *{crimsteel}*\n - Gold: *{gold}*\n - Mythan: *{mythan}*\n - Magic: *{magic}*\n\n*[ITEMS]*\n - MineX: *{minex}*\n - XP Boost: *{xpboost}*"
    keyboard = types.InlineKeyboardMarkup() 
    farm_inventory = types.InlineKeyboardButton(text='👨🏻‍🌾 Farm Inventory',callback_data='inventory farm')
    buy_button = types.InlineKeyboardButton(text='🔰 Buy',callback_data='buy menu inventory')
    sell_button = types.InlineKeyboardButton(text='🔰 Sell',callback_data='sell menu inventory')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(farm_inventory)
    keyboard.add(buy_button,sell_button)
    keyboard.add(back_button)
    await bot.edit_message_text(txt,call.from_user.id,call.message.id,txt,parse_mode="Markdown",reply_markup = keyboard)
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
    txt =f"*[TOOLS]*\n - 💦 Water: *{water}*\n\n*[SEEDS]*\n"
    txt += f" - 🥔 Potato Seeds: *{potato_seed}*\n"
    txt += f" - 🌽 Corn Seeds: *{corn_seed}*\n"
    txt += f" - 🥕 Carrot Seeds: *{carrot_seed}*\n"
    txt += f" - 🥦 Broccoli Seeds: *{broccoli_seed}*\n"
    txt += f" - 🍉 Watermelon Seeds: *{watermelon_seed}*\n"
    txt += "\n*[PLANTS]*\n"
    txt += f" - 🥔 Potato: *{potato}*\n"
    txt += f" - 🌽 Corn: *{corn}*\n"
    txt += f" - 🥕 Carrot: *{carrot}*\n"
    txt += f" - 🥦 Broccoli: *{broccoli}*\n"
    txt += f" - 🍉 Watermelon: *{watermelon}*\n"
    keyboard = types.InlineKeyboardMarkup() 
    mine_inventory = types.InlineKeyboardButton(text='⛏️ Mine Inventory',callback_data='inventory mine')
    buy_button = types.InlineKeyboardButton(text='🧺 Buy',callback_data='farm_shop seeds_buy inventory')
    sell_button = types.InlineKeyboardButton(text='🧺 Sell',callback_data='farm_shop sell_menu inventory')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(mine_inventory)
    keyboard.add(buy_button,sell_button)
    keyboard.add(back_button)
    await bot.edit_message_text(txt,call.from_user.id,call.message.id,txt,parse_mode="Markdown",reply_markup = keyboard)