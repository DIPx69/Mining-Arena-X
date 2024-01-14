import time
from datetime import datetime, timedelta
import commands as command
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

ownerid = 1794942023
leaderboard_data = {}
leaderboard_time = 0
async def time_convert(last_time: int):
   uptime_seconds = int(time.time() - last_time)
   days = uptime_seconds // (24 * 3600)
   hours = (uptime_seconds % (24 * 3600)) // 3600
   minutes = (uptime_seconds % 3600) // 60
   seconds = uptime_seconds % 60
   if days > 0:
     uptime_text = f"{days}d:{hours}h:{minutes}m:{seconds}s"
   else:
     uptime_text = f"{hours}h:{minutes}m:{seconds}s"
   return uptime_text
async def leaderboardmenu(call):
   keyboard = types.InlineKeyboardMarkup() 
   total_mine_button = types.InlineKeyboardButton(text='〽️ Total Mining', callback_data='total_mine_lb')
   level_button = types.InlineKeyboardButton(text='〽️ Level', callback_data='level_lb')
   coin_button = types.InlineKeyboardButton(text='〽️ Coin', callback_data='coin_lb')
   prestige_button = types.InlineKeyboardButton(text='〽️ Prestige', callback_data='prestige_lb')
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='main_menu')
   keyboard.add(total_mine_button,level_button)
   keyboard.add(coin_button,prestige_button)
   keyboard.add(back_button)
   await bot.edit_message_text("*Select Leaderboard*",call.from_user.id,call.message.id, parse_mode="Markdown",reply_markup=keyboard)
async def leaderboardmenu_group(message):
   keyboard = types.InlineKeyboardMarkup() 
   total_mine_button = types.InlineKeyboardButton(text='〽️ Total Mining', callback_data='total_mine_lb_group')
   level_button = types.InlineKeyboardButton(text='〽️ Level', callback_data='level_lb_group')
   coin_button = types.InlineKeyboardButton(text='〽️ Coin', callback_data='coin_lb_group')
   prestige_button = types.InlineKeyboardButton(text='〽️ Prestige', callback_data='prestige_lb_group')
   keyboard.add(total_mine_button,level_button)
   keyboard.add(coin_button,prestige_button)
   await bot.reply_to(message,"*Select Leaderboard*",parse_mode="Markdown",reply_markup=keyboard)
async def leaderboardmenu_group_call(call):
   keyboard = types.InlineKeyboardMarkup() 
   total_mine_button = types.InlineKeyboardButton(text='〽️ Total Mining', callback_data='total_mine_lb_group')
   level_button = types.InlineKeyboardButton(text='〽️ Level', callback_data='level_lb_group')
   coin_button = types.InlineKeyboardButton(text='〽️ Coin', callback_data='coin_lb_group')
   prestige_button = types.InlineKeyboardButton(text='〽️ Prestige', callback_data='prestige_lb_group')
   keyboard.add(total_mine_button,level_button)
   keyboard.add(coin_button,prestige_button)
   await bot.edit_message_text("*Select Leaderboard*",call.message.chat.id,call.message.id, parse_mode="Markdown",reply_markup=keyboard)
async def total_mine(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 60:
     datafind = await datack.find_one()
     leaderboard_data["leaderboard"] = datafind
     leaderboard_time = datafind['minetime']
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['minetime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['mine']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def coin_lb(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 60:
     datafind = await datack.find_one()
     leaderboard_data["leaderboard"] = datafind
     leaderboard_time = datafind['cointime']
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['cointime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['coin']
   last_update = await time_convert(timex)
   leadboardtxt += f"\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*"
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def level_lb(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 61:
     datafind = await datack.find_one()
     leaderboard_data["leaderboard"] = datafind
     leaderboard_time = datafind['leveltime']
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['leveltime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['level']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def prestige_lb(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 61:
     datafind = await datack.find_one()
     leaderboard_data["leaderboard"] = datafind
     leaderboard_time = datafind['prestigetime']
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['prestigetime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['prestige']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def total_mine_group(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 61:
     datafind = await datack.find_one()
     leaderboard_data["leaderboard"] = datafind
     leaderboard_time = datafind['minetime']
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['minetime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['mine']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb_group')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.message.chat.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def coin_lb_group(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 61:
     datafind = await datack.find_one()
     leaderboard_time = datafind['cointime']
     leaderboard_data["leaderboard"] = datafind
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['cointime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['coin']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb_group')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.message.chat.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def level_lb_group(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 61:
     datafind = await datack.find_one()
     leaderboard_time = datafind['leveltime']
     leaderboard_data["leaderboard"] = datafind
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['leveltime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['level']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb_group')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.message.chat.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def prestige_lb_group(call):
   global leaderboard_data
   global leaderboard_time 
   now_time = int(time.time())
   db = client['leadboard']
   datack = db["data"]
   last_update_sec = int(now_time-leaderboard_time)
   if last_update_sec >= 61:
     datafind = await datack.find_one()
     leaderboard_time = datafind['prestigetime']
     leaderboard_data["leaderboard"] = datafind
   else:
     datafind = leaderboard_data["leaderboard"]
   timex = datafind['prestigetime']  
   dt = datetime.fromtimestamp(timex)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   time2 = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   leadboardtxt = datafind['prestige']
   last_update = await time_convert(timex)
   leadboardtxt += f'\nLast Update *{last_update}* Seconds Ago\n*{time2}*\n*Leaderboard Updates Every 60 Seconds.*'
   keyboard = types.InlineKeyboardMarkup() 
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='back_lb_group')
   keyboard.add(back_button)
   await bot.edit_message_text(leadboardtxt,call.message.chat.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)