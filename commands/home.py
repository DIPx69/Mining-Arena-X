import asyncio
import json
import aiofiles
import time
 
import commands as command
import farming as farm
import admin

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def send_home_v2(message):
   user = str(message.chat.id)
   keyboard = types.InlineKeyboardMarkup()
   db = client["user"]
   datack = db[user]
   datafind = await datack.find_one()
   tiles = await farm.farm_json_maker(datafind)
   harvest_able = await farm.harvest_able(tiles,datafind)
   dailycooldown = datafind['dailycooldown']
   if int(time.time()) > dailycooldown:
     claim_able = '🟢'
   else:
     claim_able = '💵'
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
     daily_button = types.InlineKeyboardButton(text=f'{claim_able} Daily',callback_data='daily')
     inventory_button = types.InlineKeyboardButton(text='◼️ Inventory',callback_data='inventory mine')
     shop_button = types.InlineKeyboardButton(text='🏪 Shop',callback_data='shop')
     mining_button = types.InlineKeyboardButton(text='⛏️ Mining',callback_data='mine')
     upgrade_button = types.InlineKeyboardButton(text='⬆️ Upgrade',callback_data='upgrade_mine')
     leaderboard_button = types.InlineKeyboardButton(text='📊 Leadboard',callback_data='leaderboard')
     settings_button = types.InlineKeyboardButton(text='⚙️ Settings',callback_data='xsettings main')
     farming_button = types.InlineKeyboardButton(text=f'👨‍🌾 Farming ({harvest_able}/9)',callback_data='farming_menu')
     keyboard.add(profile_button)
     keyboard.add(daily_button,inventory_button,shop_button)
     keyboard.add(upgrade_button,mining_button)
     keyboard.add(farming_button)
     keyboard.add(leaderboard_button,settings_button)
   message = await bot.send_message(message.chat.id,txt,parse_mode="Markdown",reply_markup=keyboard)
   await command.update_window_msg(message)
async def send_home_v2_call(call):
   user = call.from_user.id
   user = str(user)
   keyboard = types.InlineKeyboardMarkup()
   db = client["user"]
   datack = db[user]
   datafind = await datack.find_one()
   tiles = await farm.farm_json_maker(datafind)
   harvest_able = await farm.harvest_able(tiles,datafind)
   dailycooldown = datafind['dailycooldown']
   if int(time.time()) > dailycooldown:
     claim_able = '🟢'
   else:
     claim_able = '💵'
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
     daily_button = types.InlineKeyboardButton(text=f'{claim_able} Daily',callback_data='daily')
     inventory_button = types.InlineKeyboardButton(text='◼️ Inventory',callback_data='inventory mine')
     shop_button = types.InlineKeyboardButton(text='🏪 Shop',callback_data='shop')
     mining_button = types.InlineKeyboardButton(text='⛏️ Mining',callback_data='mine')
     upgrade_button = types.InlineKeyboardButton(text='⬆️ Upgrade',callback_data='upgrade_mine')
     leaderboard_button = types.InlineKeyboardButton(text='📊 Leadboard',callback_data='leaderboard')
     settings_button = types.InlineKeyboardButton(text='⚙️ Settings',callback_data='xsettings main')
     farming_button = types.InlineKeyboardButton(text=f'👨‍🌾 Farming ({harvest_able}/9)',callback_data='farming_menu')
     keyboard.add(profile_button)
     keyboard.add(daily_button,inventory_button,shop_button)
     keyboard.add(upgrade_button,mining_button)
     keyboard.add(farming_button)
     keyboard.add(leaderboard_button,settings_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)