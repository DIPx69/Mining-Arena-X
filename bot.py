# Importing Modules 
import os
import telebot
import asyncio
import json
import ast
import urllib
import urllib.parse
import requests
import aiohttp
import pytz
import sys
import ast
import time
from datetime import datetime
import aiofiles
import config
import random
import re
import threading

# Importing Local Module
import commands as command
import clicking as click
import farming as farm
import admin
import games as game
from commands.trivia import chat_timers,poll_track

# Importing Telebot Modules
from telebot import types
from telebot import apihelper
from telebot.types import Dice
from telebot.async_telebot import *

# Importing Flask App
from keep_alive import keep_alive

# Importing DNS And Database Module
import motor.motor_asyncio
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
print(client)
bot = AsyncTeleBot(token)
ownerid = 1794942023
uptime_start = time.time()
anti_spam = {}
use_anti_spam = {}
@bot.message_handler(commands=['top'])
async def quiz(message):
   db = client['leadboard']
   datack = db["data"]
   datafind = await datack.find_one()
   history = datafind['history']
   history_text = "*[Featured Player History]*\n"
   for every in history:
     timestamp = history[every]["timestamp"]
     dt_utc = datetime.utcfromtimestamp(timestamp)
     dt_utc = pytz.utc.localize(dt_utc)
     dt_dhaka = dt_utc.astimezone(pytz.timezone("Asia/Dhaka"))
     formatted_time = dt_dhaka.strftime("%M:%S")
     history_text += f'*[{every}]* {history[every]["name"]} {history[every]["mode"]} {history[every]["amount"]}\n'
   history_text = history_text.replace("_","\_")
   await bot.send_message(message.chat.id,history_text,parse_mode="Markdown")

@bot.message_handler(commands=['claim'])
async def claim(message):
   if message.chat.type == "private":
     await command.claim_reward(message)
   else:
     await bot.reply_to(message,"*This Command Is Only For Private Message*",parse_mode="Markdown")
@bot.message_handler(commands=['quiz'])
async def quiz(message):
   maintenance_info = await maintenance_check(message)
   if maintenance_info == True:
     return 0
   if str(message.from_user.id) in poll_track:
     await bot.send_message(message.chat.id,"*You Have A Ongoing Quiz*",parse_mode="Markdown")
   else:
     poll_track[str(message.from_user.id)] = {'on':69}
     await command.trivia_group(message)
@bot.message_handler(commands=['unban','u'])
async def unbanidx(message):
   user = message.from_user
   username = user.username
   username = username.replace("_", "\\_")
   if message.chat.id != ownerid:
     await bot.send_message(ownerid,f'@{username} *({message.from_user.id})* Trying To Run Admin Command',parse_mode="Markdown")
   else:
     await admin.unban(message)
@bot.message_handler(commands=['ban','b'])
async def banidx(message):
   user = message.from_user
   username = user.username
   username = username.replace("_", "\\_")
   if message.chat.id != ownerid:
     await bot.send_message(ownerid,f'@{username} *({message.from_user.id})* Trying To Run Admin Command',parse_mode="Markdown")
   else:
     await admin.ban(message)
@bot.message_handler(commands=['id'])
async def getid(message):
    if message.reply_to_message is not None and message.chat.type == "supergroup":
       getid = message.reply_to_message.from_user.id
       await bot.reply_to(message,f"ID: `{getid}`",parse_mode="MarkdownV2")
    elif message.chat.type == "private":
         await bot.send_message(message.chat.id,f"This Command Is Only For Group Chat\nJOIN @MiningArenaChats")
    elif message.reply_to_message is None:
         await bot.reply_to(message,f"Reply To User Message To Get Their ID")
@bot.message_handler(commands=['games'])
async def send_initial_button(message):
    maintenance_info = await maintenance_check(message)
    if maintenance_info == True:
     return 0
    txt = f"*Currently Available Games*\n\[1\\] /roll \- *Roll The Dice* 🎲\n\[2\\] /dart \- *Throw The Dart* 🎯\n\[3\\] /ball \- *Kick The Football* ⚽\n\[4\\] /basket \- *Throw The Basketball* 🏀"
    if message.chat.type == "private":
       txt += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*Games Are Currently Available In Official Group Chat*"
       markup = types.InlineKeyboardMarkup(row_width=1)
       text = 'Join @MiningArenaChats'
       url = 'https://t.me/MiningArenaChats'
       button1 = types.InlineKeyboardButton(text=text, url=url)
       markup.row(button1) 
       await bot.send_message(message.chat.id,txt,parse_mode="MarkdownV2",reply_markup=markup) 
    else:
      await bot.reply_to(message,txt,parse_mode="MarkdownV2") 
@bot.message_handler(func=lambda message: message.chat.type == 'private',commands=['roll','dart','basket','profile','ball','leaderboard','ttc','quiz'])
async def send_txt(message):
    maintenance_info = await maintenance_check(message)
    if maintenance_info == True:
     return 0
    markup = types.InlineKeyboardMarkup(row_width=1)
    text = 'Join @MiningArenaChats'
    url = 'https://t.me/MiningArenaChats'
    button1 = types.InlineKeyboardButton(text=text, url=url)
    markup.row(button1)
    command_name = message.text.split()[0]
    await bot.send_message(message.chat.id,f"{command_name} *Command Is Only For Official Group Chat*",parse_mode="Markdown",reply_markup=markup)
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup',commands=['roll'])
async def gamedice(message):
    maintenance_info = await maintenance_check(message)
    if maintenance_info == True:
     return 0
    await game.send_dice(message)
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup',commands=['dart'])
async def gamedart(message):
    maintenance_info = await maintenance_check(message)
    if maintenance_info == True:
     return 0
    await game.send_dart(message)
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup',commands=['basket'])
async def gamebasketball(message):
   maintenance_info = await maintenance_check(message)
   if maintenance_info == True:
     return 0 
   await game.send_basketball(message)
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup',commands=['ball'])
async def gamefootball(message):
   maintenance_info = await maintenance_check(message)
   if maintenance_info == True:
     return 0
   await game.send_football(message)
@bot.message_handler(commands=['add'])
async def title_add(message):
   await command.title_add(message)
@bot.message_handler(commands=['titlex'])
async def title(message):
   await command.title(message)
@bot.message_handler(commands=['title'])
async def title(message):
   if message.from_user.id != ownerid:
     await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
   else:
     await command.title_admin(message)
@bot.message_handler(commands=['x59xwjw'])
def sendcoin(message):
  try:
     if message.reply_to_message is not None:
        getid = int(message.reply_to_message.from_user.id)
        getidx = str(message.reply_to_message.from_user.id)
        getcoin = str(message.text.split()[1])
        getcoin = command.txttonum(getcoin)
     else:  
        getid = int(message.text.split()[1])
        getidx = message.text.split()[1]
        getcoin = str(message.text.split()[2])
        getcoin = command.txttonum(getcoin)
     idx = str(message.from_user.id)
     dblist = client.list_database_names()
     if getidx in dblist and getidx != idx:
        user = bot.get_chat(getid)
        username = user.username
        username = username.replace("_", "\\_")
        txt = f'*Sending {getcoin} To* @{username}'
        if message.chat.type == 'private':
           sendx = bot.send_message(message.chat.id,txt,parse_mode="Markdown")
        else:
          sendx = bot.reply_to(message,txt,parse_mode="Markdown")
        db = client[getidx]
        datack = db["data"]
        userdb = client[str(message.from_user.id)]
        userdatack = userdb["data"]
        userdatafind = userdatack.find_one()
        try:
         coin = userdatafind['coin']
         ban = userdatafind['ban']
        except:
         markup = types.InlineKeyboardMarkup(row_width=1)
         text = 'Start @MiningArenaBot'
         url = 'https://t.me/MiningArenaBot?start=start'
         button1 = types.InlineKeyboardButton(text=text, url=url)
         markup.row(button1)
         bot.edit_message_text("*You Need Start The Bot* @MiningArenaBot",message.chat.id,sendx.message_id,parse_mode="Markdown",reply_markup=markup)
         return 0
        if coin >= getcoin and ban == 0 and getcoin > 0:
           query = {}
           senduser = bot.get_chat(message.from_user.id)
           sendusername = senduser.username
           sendusername = sendusername.replace("_", "\\_")
           coinadd = {'$inc':{'coin': +getcoin}}
           coinrmv = {'$inc':{'coin': -getcoin}}
           datack.update_one(query,coinadd)
           userdatack.update_one(query,coinrmv)
           txt =f"*Shared  ₪  {getcoin} With* @{username}"
           bot.edit_message_text(txt,message.chat.id,sendx.message_id,parse_mode="Markdown")
           txt2 = f'*Your Friend* @{sendusername} *Shared  ₪ {getcoin} With You!*'
           if message.chat.type == 'supergroup':
              txt2 +="\n\nSent From @MiningArenaChats"
           bot.send_message(getid,txt2,parse_mode="Markdown")
        elif getcoin <= 0:
             txt =f"*You Need To Provide Real Amount Of Coins.*"
             bot.edit_message_text(txt,message.chat.id,sendx.message_id,parse_mode="Markdown")
        elif ban == 1:
             txt =f"*You Can't Send Coin Since Your Account Is Banned *"
             bot.edit_message_text(txt,message.chat.id,sendx.message_id,parse_mode="Markdown")
        elif coin < getcoin:
             txt =f"*You Don't Have  ₪  {getcoin}*"
             bot.edit_message_text(txt,message.chat.id,sendx.message_id,parse_mode="Markdown")
     elif getidx not in dblist:
       txt = f"*User Not Found In Database*"
       bot.reply_to(message,txt,parse_mode="Markdown")
     elif getidx == idx:
          txt = "*You Can't Share Yourself LOL*"
          bot.reply_to(message,txt,parse_mode="Markdown")
  except:
    txt = "*Try To Fill All Value*\n/send <id> <coin>"
    if message.chat.type == 'supergroup':
       txt += '\n\n*Or Reply To User Message With The Following Command*: /send <coin>'
    bot.send_message(message.chat.id,txt,parse_mode="Markdown")
@bot.message_handler(commands=['leaderboard'])
async def send(message):
   maintenance_info = await maintenance_check(message)
   if maintenance_info == True:
     return 0
   await command.leaderboardmenu_group(message)
@bot.message_handler(commands=['profilex'])
async def pro(message):
    await admin.adminprofile(message)
@bot.message_handler(commands=['re'])
async def pro(message):
    if ownerid != message.chat.id:
       return 0
    if message.reply_to_message is not None:
      try:
       textx = message.reply_to_message.text.split()[13]
       if textx.isdigit():
         getid = int(textx)
         await bot.delete_message(message.chat.id,message.id)
         await admin.refresh(message,getid)
       else:
         await bot.reply_to(message,"*Reply To A* /profilex *Command To Refresh*",parse_mode="Markdown")
      except:
         await bot.reply_to(message,"*Reply To A* /profilex *Command To Refresh*",parse_mode="Markdown")
    else:
      await bot.reply_to(message,"*Reply To A* /profilex *Command To Refresh*",parse_mode="Markdown")
@bot.message_handler(commands=['info'])
async def send_initial_button(message):
    uptime_seconds = int(time.time() - uptime_start)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    if days > 0:
       uptime_text = f"{days}d:{hours}h:{minutes}m:{seconds}s"
    else:
       uptime_text = f"{hours}h:{minutes}m:{seconds}s"
    txt = f"*Bot Name:* Mining Arena\n\n*Status:* {config.status}\n\n*Version:* {config.version}\n\nUptime: *{uptime_text}*\n\n*Ping: Checking*\n\n*Chats:* @MiningArenaChats\n\n*Update Channel:* @MiningArenaUpdates\n\nMade With ❤️ By @PROJECTX69"
    if message.chat.type == "private":
       start_time = time.time()
       response = await bot.send_message(message.chat.id,txt,parse_mode="Markdown")
       end_time = time.time()
       txt = f"*Bot Name:* Mining Arena\n\n*Status:* {config.status}\n\n*Version:* {config.version}\n\nUptime: *{uptime_text}*\n\n*Ping: {int((end_time - start_time) * 1000)}ms*\n\n*Chats:* @MiningArenaChats\n\n*Update Channel:* @MiningArenaUpdates\n\nMade With ❤️ By @PROJECTX69"
       await bot.edit_message_text(txt,message.chat.id,response.message_id,parse_mode="Markdown")
    else:
       txt = f"*Bot Name:* Mining Arena\n\n*Status:* {config.status}\n\nUptime: *{uptime_text}*\n\n*Chats:* @MiningArenaChats\n\n*Update Channel:* @MiningArenaUpdates\n\nMade With ❤️ By @PROJECTX69"
       await bot.reply_to(message,txt,parse_mode="Markdown")
async def maintenance_check(message):
   async with aiofiles.open('maintenance.json', 'r') as f:
     maintenance_info = json.loads(await f.read())
   user_id = message.from_user.id
   if maintenance_info["status"] == True and user_id != ownerid:
     reason = maintenance_info["reason"]
     reason = reason.replace("nl","\n")
     if message.chat.type == "private":
       await bot.send_message(message.chat.id,f"*[BOT IS UNDER MAINTENANCE]*\n\nDeveloper Note:\n*{reason}*",parse_mode="Markdown")
     else:
       await bot.reply_to(message,f"*[BOT IS UNDER MAINTENANCE]*\n\nDeveloper Note:\n*{reason}*",parse_mode="Markdown")
     return True
   else:
     return False
@bot.message_handler(commands=['del'])
async def del_x(message):
   global anti_spam
   del anti_spam[str(message.from_user.id)]
@bot.message_handler(commands=['start'])
async def send_initial_button(message):
    user_id = message.from_user.id
    try:
     command_name = message.text.split()[1]
    except:
     command_name = "start"
    maintenance_info = await maintenance_check(message)
    if maintenance_info == True:
     return 0
    if message.chat.type == "private" and command_name == "start" :
       await command.datack(message)
       await command.send_home_v2(message)
    elif message.chat.type != "private":
      markup = types.InlineKeyboardMarkup(row_width=1)
      text = 'Try To Run In Private Message'
      url = 'https://t.me/MiningArenaBot?start=start'
      button1 = types.InlineKeyboardButton(text=text, url=url)
      markup.row(button1)
      await bot.reply_to(message,"*You Can't Start The Bot In Group Chat*",parse_mode="Markdown",reply_markup=markup)
# Advance Admin Panel 
@bot.message_handler(commands=['update'])
async def updateleadboard(message):
    await admin.leadboard_update(message)
    await admin.updateleaderboard()
    print("1")
@bot.message_handler(commands=['set','s'])
async def set_text(message):
   user = message.from_user
   username = user.username
   username = username.replace("_", "\\_")
   if message.chat.id != ownerid:
     await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
   else:
     await admin.set_text(message)
@bot.message_handler(commands=['notice'])
async def notice(message):
  async with aiofiles.open('maintenance.json', 'r') as f:
    maintenance_info = json.loads(await f.read())
  if maintenance_info["status"] == False:
    await bot.send_message(message.chat.id,"*Bot Isn't In Maintenance Mode*",parse_mode="Markdown")
  else:
     reason = maintenance_info["reason"]
     reason = reason.replace("nl","\n")
     if message.chat.type == "private":
       await bot.send_message(message.chat.id,f"*[BOT IS UNDER MAINTENANCE]*\n\nDeveloper Note:\n*{reason}*",parse_mode="Markdown")
     else:
       await bot.reply_to(message,f"*[BOT IS UNDER MAINTENANCE]*\n\n*{reason}*",parse_mode="Markdown")
@bot.message_handler(commands=['maintenance','m'])
async def maintenance(message):
   user = message.from_user
   username = user.username
   username = username.replace("_", "\\_")
   if message.chat.id != ownerid:
     await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
   else:
     await admin.maintenance(message)
@bot.message_handler(commands=['c'])
async def send(message):
   keyboard = types.ReplyKeyboardRemove(selective=None)
   await bot.send_message(message.chat.id,"Removed Reply keyboard",reply_markup=keyboard)
@bot.message_handler(commands=['post'])
async def post(message):
   await admin.post_preview(message)
@bot.message_handler(commands=['fix'])
async def fix(message):
   await command.fixlvl(message)
@bot.message_handler(commands=['ttc'])
async def ttc(message):
   maintenance_info = await maintenance_check(message)
   if maintenance_info == True:
     return 0
   await game.confirmation(message)
@bot.message_handler(commands=['rt'])
async def restart(message):
   if message.from_user.id == ownerid:
     a = await bot.send_message(message.chat.id,f'Restarting Bot',parse_mode="Markdown")
     print('Restarting script...')
     os.execv(sys.executable, ['python'] + sys.argv)
     await bot.edit_message_text(f"Bot Restarted",message.chat.id,a.message_id,parse_mode="MarkdownV2")
@bot.message_handler(commands=['xd'])
async def xjen(message):
   get_id = str(message.text.split()[1])
   db = client["user"]
   datack = db[get_id]
   #user_data = await datack.find_one()
   #data = {"$set":{'potato_seed': 0, 'broccoli': 0, 'broccoli_seed': 0, 'carrot': 0, 'carrot_seed': 0, 'corn': 0, 'corn_seed': 0, 'potato': 0, 'tile_1': 0, 'tile_2': 0, 'tile_3': 0, 'tile_4': 0, 'tile_5': 0, 'tile_6': 0, 'tile_7': 0, 'tile_8': 0, 'tile_9': 0, 'tile_name_1': 'None', 'tile_name_2': 'None', 'tile_name_3': 'None', 'tile_name_4': 'None', 'tile_name_5': 'None', 'tile_name_6': 'None', 'tile_name_7': 'None', 'tile_name_8': 'None', 'tile_name_9': 'None', 'watermelon': 0, 'watermelon_seed': 0, 'water': 0}}
   query = {}
   user_data = await datack.find_one()
   await bot.send_message(message.from_user.id,user_data)
@bot.message_handler(commands=['x69'])
async def xjsj(message):
   getidx = str(message.from_user.id)
   db = client["user"]
   datack = db[getidx]
   query = {}
   update = {
    '$set': {
        "tile_1": 0,
        "tile_name_1": "None",
        "tile_2": 0,
        "tile_name_2": "None",
        "tile_3": 0,
        "tile_name_3": "None",
        "tile_4": 0,
        "tile_name_4": "None",
        "tile_5": 0,
        "tile_name_5": "None",
        "tile_6": 0,
        "tile_name_6": "None",
        "tile_7": 0,
        "tile_name_7": "None",
        "tile_8": 0,
        "tile_name_8": "None",
        "tile_9": 0,
        "tile_name_9": "None"
    }
}
   await datack.update_one(query,update)
   await bot.send_message(message.chat.id,"Done")
@bot.message_handler(commands=['admin'])
async def send(message):
    user = message.from_user
    username = user.username
    username = username.replace("_", "\\_")
    if message.chat.id != ownerid:
       await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
    else:
      txt = "*Advanced Administration Panel*\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n/edit • /e <id> /valuename <value> | *Edit User Data*\n\n/remove <id> | *Remove User From Database*\n\n/profilex <id> | *Inspect User Profile*\n\n/update | *Update Leaderboard*\n\n/maintenance • /m <True/False> <reason>\n\n/set <Set Maintenance Info>\n\n/ban • /b <userid> <note|optional> | Ban User\n\n/unban • /u <userid> <note|optional> | Unban User"
      await bot.send_message(message.chat.id,txt,parse_mode="Markdown")
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup',commands=['profile'])
async def profile(message):
  maintenance_info = await maintenance_check(message)
  if maintenance_info == True:
     return 0
  try:
    if message.reply_to_message is not None:
       getid = int(message.reply_to_message.from_user.id)
       getidx = str(message.reply_to_message.from_user.id)
    else:
      try:
       getid = int(message.text.split()[1])
       getidx = str(message.text.split()[1])
      except:
       getid = int(message.from_user.id)
       getidx = str(message.from_user.id)
    user = await bot.get_chat(getid)
    username = user.username
    db = client["user"]
    datack = db[getidx]
    datafind = await datack.find_one()
    ban = datafind["ban"]
    coin = await command.numtotext(datafind["coin"])
    lvl = datafind["lvl"]
    totalmine = datafind['mymine']
    xp = datafind['xp']
    prestigelvl = datafind['prestige']
    prestigecoin = datafind['prestigecoin']
    nxtlvlxp = datafind['nxtlvlxp']
    dice_won = datafind["dice_won"]
    dice_lose = datafind["dice_lose"]
    dice_total = dice_won+dice_lose
    dart_won = datafind["dart_won"]
    dart_lose = datafind["dart_lose"]
    dart_total = dart_won+dart_lose
    basketball_won = datafind["basketball_won"]
    basketball_lose = datafind["basketball_lose"]
    basketball_total = basketball_won+basketball_lose
    football_won = datafind["football_won"]
    football_lose = datafind["football_lose"]
    football_total = football_won+football_lose
    active_title = datafind["active_title"]
    if ban == 0:
       txt = f"*[ @{username} - {active_title} ]*\n\n - Coin: *{coin}*\n - ID: `{getid}`\n\n - Prestige Level: *{prestigelvl}*\n - Prestige Coin: *{prestigecoin}* 🪙 \n\n*[MINING STATS]*\n - Total Mining: *{totalmine}*\n - Level: *{lvl}*\n - XP BAR: *{xp}/{nxtlvlxp}*\n\n*[MINI GAME STATS]*  *Win/Lose/Total*\n -   🎲   *[ {dice_won} || {dice_lose} || {dice_total} ]*\n -   🎯   *[ {dart_won} || {dart_lose} || {dart_total} ]*\n -   🏀   *[ {basketball_won} || {basketball_lose} || {basketball_total} ]*\n -   ⚽   *[ {football_won} || {football_lose} || {football_total} ]*"
    elif str(message.from_user.id) == getidx:
      txt =f"*You Can't View Your Profile Since Your Account Is Banned*"
    else:
      txt =f"*You Can't View @{username}'s Profile Since His/Her Account Is Banned*"
    await bot.reply_to(message,txt,parse_mode="Markdown")
  except Exception as e:
   print(str(e))
   await bot.reply_to(message,"*User Not Found In Database*",parse_mode="Markdown")
@bot.message_handler(commands=['edit','e'])
async def edit(message):
    if message.reply_to_message is None:
      await admin.edituser_no_reply(message)
    else:
      textx = message.reply_to_message.text.split()[13]
      if textx.isdigit():
         getid = int(textx)
         await bot.delete_message(message.chat.id,message.id)
         await admin.edituser_reply(message,getid)
@bot.message_handler(commands=['valuename'])
async def valuename(message):
    user = message.from_user
    username = user.username
    username = username.replace("_", "\\_")
    if message.chat.id != ownerid:
       await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
    else:
      txt = '*Currently Available Value*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`coin` Coin Value For User\n\n`prestige` Prestige Value\n\n`prestigecoin` Prestige Coin Value\n\n`minex` MineX Value\n\n`xpboost` XPBOOST Value\n\n`minexexp` MineX Expire Timestamp\n\n`xpboostexp` XPBOOST Expire Timestamp\n\n`iron` Iron Value\n\n`coal` Coal Value\n\n`silver` Silver Value\n\n`crimsteel` Crimsteel Value\n\n`gold` Gold Value\n\n`mythan` Mythan Value\n\n`magic` Magic Value\n\n`mymine` Total Mine Value \n\n`lvl` Level Value\n\n`xp` XP Value\n\n`nxtlvlxp` Next Level XP Value\n\n`dailycooldown` Daily Cooldown Timestamp\n\n`warn` Total Warning Value\n\n`automineon` AutoMine On Off Value\n\n`autominelvl` Autom Mining Level Value\n\n`xpmulti` XP Multiplier Value\n\n`itemmulti` Item Multiplier Value'
      await bot.send_message(message.chat.id,txt,parse_mode="MarkdownV2")
@bot.message_handler(commands=['remove'])
async def remove(message):
  try:
    user = message.from_user
    username = user.username
    username = username.replace("_", "\\_")
    if message.chat.id != ownerid:
       await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
    else:
      send = await bot.send_message(message.chat.id,"*Trying To Remove The User*",parse_mode="Markdown")
      getid = int(message.text.split()[1])
      idx = str(getid)
      db = client["user"]
      user = await db.list_collection_names()
      if idx in user:
         user_id = getid   
         chat = await bot.get_chat(user_id)
         username = chat.username
         username = username.replace("_", "\\_")
         await db.drop_collection(idx)
         try:
           filename = f'json data/active_window.json'
           async with aiofiles.open(filename, 'r') as f:
            window = json.loads(await f.read())
           try:
             if str(user_id) in window:
               window.remove(str(user_id))
           except:
             ...
           async with aiofiles.open(filename, 'w') as f:
             await f.write(json.dumps(window)) 
         except:
           ...
         await bot.edit_message_text(f"*User Removed From Database*\nID: `{idx}`\nUsername: @{username}",message.chat.id,send.message_id,parse_mode="MarkdownV2")
         return await command.send_home_v2(message)
      else:
        await bot.edit_message_text(f"*User Not Found In Database*",message.chat.id,send.message_id,parse_mode="Markdown")
        return await command.send_home_v2(message)
  except:
    await bot.edit_message_text(f"*Use A Valid ID*",message.chat.id,send.message_id,parse_mode="Markdown")
    return await command.send_home_v2(message)
@bot.message_handler(func=lambda message: message.chat.type == 'group')
async def handle_group_message(message):
    pass
@bot.message_handler(func=lambda message: message.chat.type == 'group', commands=['start'])
async def handle_group_command(message):
    pass
@bot.poll_answer_handler(func=lambda poll: True)
async def register_poll_answer(poll):
   if str(poll.user.id) in poll_track:
     user_data = poll_track[f"{str(poll.user.id)}"]
     del poll_track[f"{str(poll.user.id)}"]
     if poll.user.id == user_data["user_id"]: 
       keyboard = types.InlineKeyboardMarkup()
       again_button = types.InlineKeyboardButton(text='⁉️ Again',callback_data='again_quiz')
       keyboard.add(again_button)
       await bot.stop_poll(user_data["chat_id"],user_data["message_id"],reply_markup=keyboard)
       if user_data["correct_option_id"] == poll.option_ids[0]:
         query = {}
         coin = random.randint(4000,10000)
         msg = await bot.send_message(user_data["chat_id"],f"*Hey @{poll.user.username}\nYou Have Won {coin} Coin*\n",parse_mode="Markdown")
         db = client["user"]
         user_db = db[str(poll.user.id)]
         data = {"$inc":{"coin": coin}}
         await user_db.update_one(query,data)
         await asyncio.sleep(0.75)
         await bot.delete_message(msg.chat.id,msg.message_id)
     elif poll.user.id != user_data["user_id"]:
       name = user_data["name"]
       msg = await bot.send_message(user_data["chat_id"],f"*Hey @{poll.user.username}\nOnly @{name} Can Answer This Quiz\n*",parse_mode="Markdown")
       await asyncio.sleep(1.5)
       await bot.delete_message(msg.chat.id,msg.message_id)
@bot.callback_query_handler(func=lambda call: True)
async def handle_callback_query(call):
    global anti_spam
    global use_anti_spam
    print(call.data)
    print(call.from_user.username)
    chat_type = call.message.chat.type
    data = call.json
    allowed_callback = ["delete"]
    async with aiofiles.open('maintenance.json', 'r') as f:
     maintenance_info = json.loads(await f.read())
    if maintenance_info["status"] == True and call.from_user.id != ownerid:
      reason = maintenance_info["reason"]
      reason = reason.replace("nl","\n")
      if len(reason) > 96:
        tzt = "..."
      else:
        tzt = ""
      await bot.answer_callback_query(call.id, text=f"Mining Arena Is Under Maintenance\n\n{reason[:97]}{tzt}\n\nTo Know More Type /notice", show_alert=True)
      return 0
    user_id = int(call.from_user.id)
    message_id = int(call.message.message_id)
    filename = f'json data/active_window.json'
    async with aiofiles.open(filename, 'r') as f:
     window = json.loads(await f.read())
    if str(user_id) in window:
      if window[str(user_id)]["message_id"] != message_id and chat_type == "private" and call.data not in allowed_callback:
        message_text = "Oops! Running the same command again? Only the latest one works. Please use the newest command. Thank you!"
        await bot.answer_callback_query(call.id,text=f"Command Duplication\n\n{message_text}", show_alert=True)
        return 0
    else:
      await command.update_window(call)
    if str(call.from_user.id) not in anti_spam and not call.data.startswith("use"):
     anti_spam[str(call.from_user.id)] = {"command": call.data}
     print(anti_spam)
    elif str(call.from_user.id) in anti_spam:
     warning_list = ["Oops! It looks like you're clicking multiple buttons simultaneously. Please avoid doing this.","Hold on! It appears you're hitting multiple buttons simultaneously. Let's avoid that, shall we?","Please avoid clicking multiple buttons at once. Thank you!","Stop multi-clicking buttons, please.","Avoid simultaneous button presses, please."]
     random_warn = random.choice(warning_list)
     await bot.answer_callback_query(call.id, text=f"NO DOUBLE-TAPS ALLOWED\n\n{random_warn}", show_alert=True)
     return 0

    # Callback Data Processing From Here
    if call.data =="main_menu":
      await command.send_home_v2_call(call)
    if call.data == "ban_menu":
     async with aiofiles.open("ban.json", 'r') as f:
      ban_ids = json.loads(await f.read())
      if any(user_id == ban_id['id'] for ban_id in ban_ids):
        await bot.answer_callback_query(call.id,text=f"You Can't Use Any Action While Your Account Is Banned",show_alert=True)
        del anti_spam[str(call.from_user.id)]
        return 0
      else:
       await command.send_home_v2_call(call)
    if call.data == "x":
      await bot.answer_callback_query(call.id,text=f"You Can't Adjust Level While Mining")
    if call.data == "home":
       try:
         await command.removeid(call)
       except:
         ...
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       text = '✖️ MENU CLOSED ✖️'
       url = 'https://t.me/MiningArenaChats'
       closed_button = types.InlineKeyboardButton(text=text, url=url)
       keyboard.row(closed_button)
       await bot.edit_message_text(f"*{call.message.text}*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
       #await command.send_home(call.message)
    if call.data == "confirmprestige":
       await command.confirmprestige(call)
    if call.data == 'prestigeyes':
        await command.prestigeyes(call)
    elif call.data == 'prestigeno':
        await command.send_home_v2_call(call)
    if call.data == 'home_2':
       await command.removeid(call)
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       text = '✖️ MENU CLOSED ✖️'
       url = 'https://t.me/MiningArenaChats'
       closed_button = types.InlineKeyboardButton(text=text, url=url)
       keyboard.row(closed_button)
       await bot.edit_message_text(f"*{call.message.text}*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
       #await command.send_home(call.message)
    if call.data == 'back_itemmulti' or call.data == "back_xpmulti":
       await command.prestigeshop_call(call)
    if call.data == 'itemmulti':
       await command.itemmulti_use_ask(call)
    if call.data == 'xpmulti':
       await command.xpmulti_use_ask(call)
    if call.data == 'confirm_itemmulti':
       idx = str(call.from_user.id)
       db = client["user"]
       datack = db[idx]
       datafind = await datack.find_one()
       prestigecoin = datafind['prestigecoin']
       if prestigecoin > 0:
          await command.itemmulti_use(call)
       else:
         await bot.answer_callback_query(call.id, text="You Don't Have Any Prestige Coin", show_alert=True)
    if call.data == 'confirm_xpmulti':
       idx = str(call.from_user.id)
       db = client["user"]
       datack = db[idx]
       datafind = await datack.find_one()
       prestigecoin = datafind['prestigecoin']
       if prestigecoin > 0:
          await command.xpmulti_use(call)
       else:
         await bot.answer_callback_query(call.id, text="You Don't Have Any Prestige Coin", show_alert=True)
    if call.data.startswith("sell"):
       item_name = call.data.split()[1]
       if item_name == "menu":
         reference = call.data.split()[2]
         await command.sellmenu(call,reference)
       elif item_name == "xall":
         reference = call.data.split()[2]
         await command.sell_all(call,reference,edit=True)
       elif item_name == "all_ask":
         reference = call.data.split()[2]
         await command.sell_items_all_ask(call,reference)
       elif item_name == "no_edit":
         item_name = call.data.split()[2]
         reference = "shop"
         await command.sell_item(call,item_name,reference,edit=False)
         await command.minemenu(call)
       else:
        reference = call.data.split()[2]
        await command.sell_item(call,item_name,reference)
    if call.data.startswith("farm_sell"):
       item_name = call.data.split()[1]
       reference = call.data.split()[2]
       if item_name =="all":
         await command.sell_plants_all(call,reference)
       elif item_name == "xall":
         await command.sell_plants_all(call,reference,edit=True)
       elif item_name =="all_ask":
         await command.sell_plants_all_ask(call,reference)
       else:
         await command.sell_plants(call,item_name,reference)
    if call.data.startswith("minex"):
       get_index = call.data.split()[1]
       if get_index == "back":
         await command.buymenu_call(call)
       elif get_index == "buy":
         await command.buy_minex(call)
       elif get_index == "custom":
         await command.minex_custom(call)
       else:
         get_index = int(get_index)
         await command.minex_buy(call,get_index)
    if call.data.startswith("xpboost"):
       get_index = call.data.split()[1]
       if get_index == "back":
         await command.buymenu_call(call)
       elif get_index == "buy":
         await command.buy_xpboost(call)
       elif get_index == "custom":
         await command.xpboost_custom(call)
       else:
         get_index = int(get_index)
         await command.xpboost_buy(call,get_index)
    if call.data == "max":
       upgrade = await command.max_upgrade(call)
       if upgrade:
         await command.upgrade_menu(call)
    if call.data == "level_adjust":
       await command.level_adjust(call)
       await command.upgrade_menu(call)
    if call.data == "upgrade_automine":
       upgrade = await command.upgrade_automine(call)
       if upgrade:
         await command.upgrade_menu(call)
    if call.data == "dailycooldown":
       await command.dailycooldown(call)
    if call.data == "dailyclaim":
       await command.dailyclaim(call)
    if call.data.startswith("view_mine"):
     item_name = call.data.split()[1]
     await command.view_mine(call,item_name)
    if call.data.startswith("switch"):
     item_name = call.data.split()[1]
     mine_item_name = call.data.split()[2]
     if item_name == "minex":
       await command.switch_minex(call,mine_item_name)
     elif item_name == "xpboost":
       await command.switch_xpboost(call,mine_item_name)
    if call.data.startswith("start_mine"):
       try:
         del anti_spam[str(call.from_user.id)]
       except:
         ...
       item_name = call.data.split()[1]
       await command.start_mine(call,item_name)
    if call.data == "refresh_mining":
       await command.minemenu(call)
    if call.data == "back_mining":
      await command.minemenu(call)
    if call.data == "claim_mine":
      notification = await bot.send_message(call.from_user.id,"*Heading to the cave to gather all the items*",parse_mode="Markdown")
      await command.claim_mine(call)
      await bot.edit_message_text("*Collected*",call.from_user.id,notification.message_id,parse_mode="Markdown")
      await bot.delete_message(call.from_user.id,notification.id)
    if call.data == "delete":
       del anti_spam[str(call.from_user.id)]
       await bot.delete_message(call.from_user.id,call.message.id)
       return 0

    # Clicking Game Callback
    if call.data.startswith("clicking"):
       command_name = call.data.split()[1]
       if command_name == "main":
         await click.main_menu(call)
       elif command_name == "click":
         await click.clicking(call)
    if call.data == "back_lb":
      await command.leaderboardmenu(call)
    if call.data == "total_mine_lb":
      await command.total_mine(call)
    if call.data == "level_lb":
      await command.level_lb(call)
    if call.data == "coin_lb":
      await command.coin_lb(call)
    if call.data == "prestige_lb":
      await command.prestige_lb(call)
    if call.data == "back_lb_group":
      if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
        username = data["message"]["reply_to_message"]["from"]["username"]
        await bot.answer_callback_query(call.id, text=f"Only @{username} Can Interact With This Button\n\nTry To Open A New Window", show_alert=True)
      else:
        await command.leaderboardmenu_group_call(call)
    if call.data == "total_mine_lb_group":
      if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
        username = data["message"]["reply_to_message"]["from"]["username"]
        await bot.answer_callback_query(call.id, text=f"Only @{username} Can Interact With This Button\n\nTry To Open A New Window", show_alert=True)
      else:
       await command.total_mine_group(call)
    if call.data == "level_lb_group":
      if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
        username = data["message"]["reply_to_message"]["from"]["username"]
        await bot.answer_callback_query(call.id, text=f"Only @{username} Can Interact With This Button\n\nTry To Open A New Window", show_alert=True)
      else:
       await command.level_lb_group(call)
    if call.data == "coin_lb_group":
      if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
        username = data["message"]["reply_to_message"]["from"]["username"]
        await bot.answer_callback_query(call.id, text=f"Only @{username} Can Interact With This Button\n\nTry To Open A New Window", show_alert=True)
      else:
       await command.coin_lb_group(call)
    if call.data == "prestige_lb_group":
     if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
        username = data["message"]["reply_to_message"]["from"]["username"]
        await bot.answer_callback_query(call.id, text=f"Only @{username} Can Interact With This Button\n\nTry To Open A New Window", show_alert=True)
     else: 
       await command.prestige_lb_group(call)
    if call.data == "profile":
      await command.profile(call)
    if call.data == "prestige":
      await command.prestigestat(call)
    if call.data == "daily":
      await command.dailyMenu(call)
    if call.data.startswith("farm_shop"):
      #if call.from_user.id != ownerid:
       #await bot.answer_callback_query(call.id, text=f"Farm Shop Is Under Development", show_alert=True)
      # del anti_spam[str(call.from_user.id)]
     #  return 0
      menu = call.data.split()[1]
      if menu == "menu":
       reference = call.data.split()[2]
       await command.farm_shop(call,reference)
      elif menu == "sell_menu":
         reference = call.data.split()[2]
         await  command.farm_shop_sell_menu(call,reference)
      elif menu == "buy_menu":
         reference = call.data.split()[2]
         await  command.farm_shop_buy_menu(call,reference)
      elif menu == "plants_sell":
        reference = call.data.split()[2]
        await command.sell_plants_menu(call,reference)
      elif menu == "seeds_sell":
        reference = call.data.split()[2]
        await command.sell_seeds_menu(call,reference)
      elif menu == "seeds_buy":
        reference = call.data.split()[2]
        await command.buy_seeds_menu(call,reference)
      elif menu == "plants_buy":
        await bot.answer_callback_query(call.id, text=f"Plants Shop Is Disabled Globally", show_alert=True)
    if call.data.startswith("farm_seed_sell"):
      item_name = call.data.split()[1]
      reference = call.data.split()[2]
      await command.sell_seed(call,item_name,reference)
    if call.data.startswith("farm_seed_buy"):
      item_name = call.data.split()[1]
      reference = call.data.split()[2]
      await command.buy_seed(call,item_name,reference)
    if call.data.startswith("farm_seed"):
       menu = call.data.split()[1]
       if menu == "sell":
         seed_name = call.data.split()[2]
         reference = call.data.split()[3]
         if seed_name == "all":
           await command.sell_seeds_all(call,reference)
         elif seed_name == "xall":
           await command.sell_seeds_all(call,reference,edit=True)
         elif seed_name == "all_ask":
           await command.sell_seeds_all_ask(call,reference)
         else:
           seed_quantity = call.data.split()[3]
           if seed_quantity.isdigit():
             reference = call.data.split()[4]
             await command.sell_seeds(call,seed_name,seed_quantity,reference)
           else:
             await command.sell_seeds_custom(call,seed_name)
       elif menu == "buy":
         seed_name = call.data.split()[2]
         seed_quantity = call.data.split()[3]
         if seed_quantity.isdigit():
           reference = call.data.split()[4]
           await command.buy_seeds(call,seed_name,seed_quantity,reference)
         else:
           await command.buy_seeds_custom(call,seed_name)
    if call.data.startswith("inventory"):
      try:
       inventory = call.data.split()[1]
      except:
       await bot.answer_callback_query(call.id, text=f"Kindly Run New /start Menu", show_alert=True)
      if inventory == "mine":
       await command.inventory(call)
      elif inventory == "farm":
       await command.inventory_farm(call)
    if call.data == "shop":
      await command.shopmenu(call)
    if call.data.startswith("buy"):
      menu = call.data.split()[1]
      if menu == "menu":
       reference = call.data.split()[2]
       await command.buymenu(call,reference)
      elif menu == "minex":
        reference = call.data.split()[2]
        await command.buy_minex(call,reference)
      elif menu == "xpboost":
        reference = call.data.split()[2]
        await command.buy_xpboost(call,reference)
      elif menu == "buy_minex":
        get_index = int(call.data.split()[2])
        reference = call.data.split()[3]
        await command.minex_buy(call,reference,get_index)
      elif menu == "buy_xpboost":
        get_index = int(call.data.split()[2])
        reference = call.data.split()[3]
        await command.xpboost_buy(call,reference,get_index)
      elif menu == "xpboost_custom":
       await command.xpboost_custom(call)
      elif menu == "minex_custom":
       await command.minex_custom(call)
    if call.data == "prestige_shop":
      await command.prestigeshop(call)
    if call.data == "mining":
      await command.miningmenu(call)
    if call.data == "mine":
      await command.minemenu(call)
    if call.data == "upgrade_mine":
      await command.upgrade_menu(call)
    if call.data == "cancel_ask":
      await command.cancel_mine_ask(call)
    if call.data == "cancel_mine":
      await command.active_miner_remove(call)
      await command.cancel_mine(call)
      await command.minemenu(call)
    if call.data == "leaderboard":
      await command.leaderboardmenu(call)
    if call.data == "info":
      await admin.info(call)
    if call.data.startswith("xsettings"):
       menu = call.data.split()[1]
       if menu == "main":
         del anti_spam[str(call.from_user.id)]
         await command.settingmenu(call)
       elif menu == "close":
         await command.close(call)
       elif menu == "shop":
         await command.settigs_shop(call)
       elif menu == "change":
         key = call.data.split()[2]
         await command.switch(call,key)
         await command.settigs_shop(call)
    if call.data == "admin_panel":
      await admin.adminmenu(call)
    if call.data == "user_list":
      await admin.userlist(call)
    if call.data == "message_to_user":
      await admin.sendmsgtouser(call)
    if call.data == "message_to_all_user":
      await admin.sendmsgtouser_all(call)
    if call.data =="ban_list":
      await admin.banlist(call)
    if call.data =="farming_menu":
       if call.from_user.id != ownerid:
        await bot.answer_callback_query(call.id, text=f"Farming Is Disabled Temporary", show_alert=True)
       else:
        await farm.menu(call)
    if call.data == "harvest":
      confirm = await farm.harvest(call)
      if confirm:
        await farm.menu(call)
    if call.data.startswith("use"):
      cmd = call.data.split()[1]
      if cmd == "item":
        await farm.all_items(call)
      else:
       await farm.use(call,cmd)
    if call.data.startswith("xuse_all"):
       item_name = call.data.split()[1]
       for tile_index in range(1, 10):
         message_text = call.message.text
         replace_tile_num_to_emoji = message_text.replace(f"{tile_index}    ", f"🟢  ")
         await asyncio.gather(bot.edit_message_text(replace_tile_num_to_emoji,call.from_user.id,call.message.id,parse_mode="Markdown"),farm.use_item(call,item_name,tile_index,notification=False))
       await farm.use(call,item_name)
    if call.data.startswith("use_item"):
       item_name = call.data.split()[1]
       tile_index = call.data.split()[2]
       if str(call.from_user.id) not in use_anti_spam:
         use_anti_spam[str(call.from_user.id)] = {}
       if str(tile_index) not in use_anti_spam[str(call.from_user.id)]:
         use_anti_spam[str(call.from_user.id)][str(tile_index)] = {"command": call.data}
         confirm = await farm.use_item(call,item_name,tile_index)
         if confirm:
           await farm.use(call,item_name)
         del use_anti_spam[str(call.from_user.id)][str(tile_index)]
       else:
         await bot.answer_callback_query(call.id, text=f"You Can't Spam A Tile Multiple Time", show_alert=True)
    if call.data == "farm_refresh":
      await farm.menu(call)
    if call.data.startswith("adjust"):
       await command.switch_pickaxe(call)
    if call.data.startswith("page_list"):
       total_page = int(call.data.split()[1])
       await command.page_list(call,total_page)
    if call.data == "again_quiz":
      if str(call.from_user.id) in poll_track:
        await bot.answer_callback_query(call.id, text=f"You Have A Ongoing Quiz", show_alert=True)
      else:
        poll_track[str(call.from_user.id)] = {'on':69}
        await command.trivia_call(call)
    if call.data == "title":
      await command.title(call)
    if call.data == "claim_reward":
      await command.claim_them(call)
    if call.data.startswith("answer"):
      if chat_timers[call.message.chat.id]:
        print(chat_timers)
        del chat_timers[call.message.chat.id]
        print(chat_timers) 
      get_answer = call.data.split(' ', 1)
      get_answer_2 = ast.literal_eval(get_answer[1])
      correct_answer = get_answer_2[0]
      user_answer = get_answer_2[1]
      if correct_answer == user_answer:
        await bot.answer_callback_query(call.id, text="You got that answer correct smarty-pants", show_alert=True)
      else:
       await bot.answer_callback_query(call.id, text=f"No nitwit, the correct answer was {correct_answer}", show_alert=True)
      await command.trivia(call)
    if call.data.startswith("title_switch"):
      get_index = call.data.split()[1]
      await command.switch_title_page(call,get_index)
    if call.data.startswith("set"):
       get_index = call.data.split()[1]
       await command.set_title(call,get_index)
    if call.data.startswith("ttc"):
       await game.sign(call)
    if call.data.startswith("accept"):
       get_id = int(call.data.split()[1])
       get_id_call = int(call.from_user.id)
       if get_id != get_id_call:
         await bot.answer_callback_query(call.id, text=f"You Can't Interact With Others Button", show_alert=True)
       else:
         await game.send_table(call,get_id)
    if call.data.startswith("decline"):
       get_id = int(call.data.split()[1])
       get_id_call = int(call.from_user.id)
       if get_id != get_id_call:
         await bot.answer_callback_query(call.id, text=f"You Can't Interact With Others Button", show_alert=True)
       else:
         text = call.message.text
         text = re.sub("Pending Confirmation","Action Declined", text)
         await bot.edit_message_text(f"*{text}*",call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
    if call.data.startswith("minelvl"):
      await command.switch_lvl(call)
    try:
      del anti_spam[str(call.from_user.id)]
    except:
      ...
    print(anti_spam)
    print()
@bot.message_handler(content_types=['new_chat_members'])
async def new_members(message):
   await bot.delete_message(message.chat.id,message.id)
   text =f"🎉 Welcome To Our Group\n\nDear @{message.from_user.username}\n\nWe're thrilled to have you join us in the Mining Arena community. Feel free to introduce yourself and share your mining adventures with us. If you have any questions or need assistance, don't hesitate to ask. Let's dig deep, conquer challenges, and become legendary miners together! 💪🌟"
   await bot.send_message(message.chat.id,text,parse_mode="Markdown")
@bot.message_handler(content_types=['left_chat_member'])
async def left_member(message):
   await bot.delete_message(message.chat.id,message.id)
   text = f"👋 Farewell @{message.from_user.username}\n\nIt's been a pleasure having you as part of our Mining Arena community. Your contributions and presence will be missed. Remember, the mining journey continues, and you're always welcome back if you decide to return. Wishing you all the best in your future endeavors! ⛏️🌟"
   await bot.send_message(message.chat.id,text,parse_mode="Markdown")
@bot.message_handler(content_types=['pinned_message'])
async def handle_pinned_message(message):
    await bot.delete_message(message.chat.id,message.id)
@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text'])
async def send_text(message):
   await command.datack(message)
   if message.reply_to_message is not None:
     reply_text = True
     itemname = message.reply_to_message.text.split()[0]
     print(message.reply_to_message.text.split())
     if itemname == "📨":
       await admin.sendmsg(message,message.text)
     if itemname == "💌":
       await admin.sendmsg_user(message)
     if itemname == "⚠️":
       await admin.saveid(message)
     if itemname == "[MINEX]":
        ammout = message.text
        await command.minex_buy_confirm(message,ammout)
     elif itemname == "[XPBOOST]":
         ammout = message.text
         await command.xpboost_buy_confirm(message,ammout)
     elif itemname == "[SELL":
       ammout = message.text
       item_name = message.reply_to_message.text.split()[1].lower()
       await command.seeds_sell_confirm(message,item_name,ammout)
     elif itemname == "[BUY":
       ammout = int(message.text)
       item_name = message.reply_to_message.text.split()[1].lower()
       item_name += "_seed"
       await command.seeds_buy_custom(message,item_name,ammout)
print("BOT IS RUNNING..")
if __name__ == "__main__":
   keep_alive()
   asyncio.run(bot.polling(non_stop=True))