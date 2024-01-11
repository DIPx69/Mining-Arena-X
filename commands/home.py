import telebot
import asyncio
import os
import json
import aiofiles
import config 
import commands as command
import admin
from telebot import types
from telebot.types import Dice
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
ownerid = 1794942023
async def send_home_v2(message):
   sign = admin.update.sign
   user = message.chat.id
   user = str(user)
   keyboard = types.InlineKeyboardMarkup()
   if message.chat.id == ownerid:
     admin_button = types.InlineKeyboardButton(text='💻 Admin Panel',callback_data='admin_panel')
     log_button = types.InlineKeyboardButton(text=f'🌳 Log',callback_data='log')
     info_button = types.InlineKeyboardButton(text=f'📃 Server Info',callback_data='info')
     click_button = types.InlineKeyboardButton(text=f'☝🏻 Clicking',callback_data='clicking main')
     keyboard.add(click_button)
     keyboard.add(info_button,log_button)
     keyboard.add(admin_button)
   user_id = message.chat.id
   async with aiofiles.open("json_data/ban.json", 'r') as f:
      ban_ids = json.loads(await f.read())
   if any(user_id == ban_id['id'] for   ban_id in ban_ids):
     txt = "*[ACCOUNT BANNED]*\n\n*Unfortunately, this account has been banned due to a violation of the game's terms of service. The ban could be a result of spamming button, cheating, exploiting glitches, or engaging in behavior that disrupts fair gameplay. The game's administrators enforce these measures to maintain a fair and enjoyable environment for all players. If you believe this ban was issued in error, you may reach out to the game's support team for further clarification and resolution.*"
     ban_button = types.InlineKeyboardButton(text='Account Banned 🚫',callback_data='main_menu')
     appeal_button = types.InlineKeyboardButton(text="Contact With Support", url="https://t.me/MiningArenaSupportBot")
     keyboard.add(ban_button)
     keyboard.add(appeal_button)
   else:
     txt = f"*🏡 Main Menu*"
     profile_button = types.InlineKeyboardButton(text='👤 Profile',callback_data='profile')
     daily_button = types.InlineKeyboardButton(text='💲 Daily',callback_data='daily')
     inventory_button = types.InlineKeyboardButton(text='◼️ Inventory',callback_data='inventory mine')
     shop_button = types.InlineKeyboardButton(text='🏪 Shop',callback_data='shop')
     mining_button = types.InlineKeyboardButton(text='⛏️ Mining',callback_data='mine')
     upgrade_button = types.InlineKeyboardButton(text='⬆️ Upgrade',callback_data='upgrade_mine')
     leaderboard_button = types.InlineKeyboardButton(text='📊 Leadboard',callback_data='leaderboard')
     settings_button = types.InlineKeyboardButton(text='⚙️ Settings',callback_data='xsettings main')
     farming_button = types.InlineKeyboardButton(text='👨‍🌾 Farming',callback_data='farming_menu')
     keyboard.add(profile_button)
     keyboard.add(daily_button,inventory_button,shop_button)
     keyboard.add(upgrade_button,mining_button)
     keyboard.add(farming_button)
     keyboard.add(leaderboard_button,settings_button)
   message = await bot.send_message(message.chat.id,txt,parse_mode="Markdown",reply_markup=keyboard)
   await command.update_window_msg(message)
async def send_home_v2_call(call):
   sign = admin.update.sign
   user = call.from_user.id
   user = str(user)
   keyboard = types.InlineKeyboardMarkup()
   if call.from_user.id == ownerid:
     admin_button = types.InlineKeyboardButton(text='💻 Admin Panel',callback_data='admin_panel')
     log_button = types.InlineKeyboardButton(text=f'🌳 Log',callback_data='log')
     info_button = types.InlineKeyboardButton(text=f'📃 Server Info',callback_data='info')
     click_button = types.InlineKeyboardButton(text=f'☝🏻 Clicking',callback_data='clicking main')
     keyboard.add(click_button)
     keyboard.add(info_button,log_button)
     keyboard.add(admin_button)
   user_id = call.from_user.id
   async with aiofiles.open("json_data/ban.json", 'r') as f:
      ban_ids = json.loads(await f.read())
   if any(user_id == ban_id['id'] for   ban_id in ban_ids):
     txt = "*[ACCOUNT BANNED]*\n\n*Unfortunately, this account has been banned due to a violation of the game's terms of service. The ban could be a result of spamming button, cheating, exploiting glitches, or engaging in behavior that disrupts fair gameplay. The game's administrators enforce these measures to maintain a fair and enjoyable environment for all players. If you believe this ban was issued in error, you may reach out to the game's support team for further clarification and resolution.*"
     ban_button = types.InlineKeyboardButton(text='Account Banned 🚫',callback_data='ban_menu')
     appeal_button = types.InlineKeyboardButton(text="Contact With Support", url="https://t.me/MiningArenaSupportBot")
     keyboard.add(ban_button)
     keyboard.add(appeal_button)
   else:
     txt = "*🏡 Main Menu*"
     profile_button = types.InlineKeyboardButton(text='👤 Profile',callback_data='profile')
     daily_button = types.InlineKeyboardButton(text='💲 Daily',callback_data='daily')
     inventory_button = types.InlineKeyboardButton(text='◼️ Inventory',callback_data='inventory mine')
     shop_button = types.InlineKeyboardButton(text='🏪 Shop',callback_data='shop')
     mining_button = types.InlineKeyboardButton(text='⛏️ Mining',callback_data='mine')
     upgrade_button = types.InlineKeyboardButton(text='⬆️ Upgrade',callback_data='upgrade_mine')
     leaderboard_button = types.InlineKeyboardButton(text='📊 Leadboard',callback_data='leaderboard')
     settings_button = types.InlineKeyboardButton(text='⚙️ Settings',callback_data='xsettings main')
     farming_button = types.InlineKeyboardButton(text='👨‍🌾 Farming',callback_data='farming_menu')
     keyboard.add(profile_button)
     keyboard.add(daily_button,inventory_button,shop_button)
     keyboard.add(upgrade_button,mining_button)
     keyboard.add(farming_button)
     keyboard.add(leaderboard_button,settings_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)