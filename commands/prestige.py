import telebot
import os
import config
import random
import commands as command
import json
import aiofiles
import dns.resolver
import config
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
async def prestigestat(call):
    keyboard = keyboard = types.InlineKeyboardMarkup()
    idx = str(call.from_user.id)
    db = client["user"]
    datack = db[idx]
    datafind = await datack.find_one()
    prestigelvl = datafind['prestige']
    coin = datafind['coin']
    lvl = datafind['lvl']
    nxt = prestigelvl+1
    coinrequirement = nxt*config.eachprestigecoin
    coinrequirement_str = await command.numtotext(coinrequirement)
    coin_str = await command.numtotext(coin)
    lvlrequirement = nxt*config.eachprestigelvl
    coinpercentage = coin/coinrequirement*100
    coinpercentage = "{:.2f}".format(coinpercentage)
    lvlpercentage = lvl/lvlrequirement*100
    lvlpercentage = "{:.2f}".format(lvlpercentage)
    if coin >= coinrequirement and lvl >= lvlrequirement:
       confirm_button = types.InlineKeyboardButton(text='💊 Confirm Prestige', callback_data='confirmprestige')
       keyboard.add(confirm_button) 
       warn = f"""Prestiging means losing nearly everything you've ever earned in the currency system (coins, levels,items,seeds etc) in exchange for increasing your 'Prestige Level' and upgrading your status\n
```
Things you won't lose:```
*- Item Multiplier
- XP Multiplier
- Total Mining
- Your Settings
- Farming Progress & Inventory (Excluding Seeds)
- Mini Game Status*
```
Basically Everything About Mining
```
"""
    else:
      warn = ""
    home_button = types.InlineKeyboardButton(text='🏡 Home', callback_data='main_menu')
    back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='profile')
    keyboard.add(home_button,back_button)
    txt = f"""
```
PRESTIGE {nxt} REQUIREMENT
``````
Coin: {coin_str}/{coinrequirement_str} [{coinpercentage}%]
Level: {lvl}/{lvlrequirement} [{lvlpercentage}%]
``` {warn}
"""
    txtx = f'*[PRESTIGE {nxt} REQUIREMENT]*\n\n - Coin:* {coin_str}/{coinrequirement_str}                   *{coinpercentage}%*\n - Level:* {lvl}/{lvlrequirement}                           *{lvlpercentage}%*\n{warn}'
    await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def confirmprestige(call):
    idx = str(call.from_user.id)
    db = client["user"]
    datack = db[idx]
    datafind = await datack.find_one()
    prestigelvl = datafind['prestige']     
    coin = datafind['coin']
    lvl = datafind['lvl']
    automineon = datafind['automineon']
    nxt = prestigelvl+1
    coinrequirement = nxt*config.eachprestigecoin
    lvlrequirement = nxt*config.eachprestigelvl
    if coin >= coinrequirement and lvl >= lvlrequirement and automineon == 0:
       keyboard = types.InlineKeyboardMarkup()
       yes_button = types.InlineKeyboardButton(text='✅ Yes', callback_data='prestigeyes')
       no_button = types.InlineKeyboardButton(text='❌ No', callback_data='prestigeno')
       keyboard.add(yes_button, no_button)
       txt = f"""
```
This is your final warning. This cannot be undone
``````
Are you absolutely sure you want to prestige ?
```
"""
       txtx = "*This is your final warning. This cannot be undone.\nAre you absolutely sure you want to prestige?*"
       await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
    elif automineon == 1:
       await bot.answer_callback_query(call.id, text="You Can't Prestige While Mining", show_alert=True)
    else:
     await command.prestigestat(call)
async def prestigeyes(call):
  idx = str(call.from_user.id)
  db = client["user"]
  datack = db[idx]
  datafind = await datack.find_one()
  automineon = datafind['automineon']
  prestigelvl = datafind['prestige']     
  coin = datafind['coin']
  lvl = datafind['lvl']
  nxt = prestigelvl+1
  coinrequirement = nxt*config.eachprestigecoin
  lvlrequirement = nxt*config.eachprestigelvl
  if automineon == 0 and coin >= coinrequirement and lvl >= lvlrequirement:
    await command.prestigedone(call)
    await command.send_home_v2(call.message)
  elif automineon == 1:
    txt = "*You Can't Prestige While You Are Mining*"
    await bot.edit_message_text(txt,call.chat.id,call.message.id,parse_mode="Markdown")
    await bot.delete_message(call.from_user.id,call.message.id)
    await command.send_home_v2(call.message)
async def prestigedone(call):
    idx = str(call.from_user.id)
    db = client["user"]
    datack = db[idx]
    query = {}
    item = random.randint(1,6)
    itemamount = random.randint(1,config.maxitem)
    coinreward  = random.randint(1,config.maxcoin)
    newdata = {'$set':{"coin":0,"minex":0,"minexexp":0,"xpboost":0,"xpboostexp":0,"iron":0,"coal":0,"silver":0,"crimsteel":0,"gold":0,"mythan":0,"magic":0,"lvl":1,"xp":0,"nxtlvlxp":100,"minecooldown":0,"mineon": 0,"autominelvl": 5,"maximum_automine_lvl":5,"potato_seed":0,"broccoli_seed":0,"carrot_seed":0,"corn_seed":0,"watermelon_seed":0,"xpboost_on":0,"minex_on":0}}
    if item == 1:
       name = "Iron"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"iron": +itemamount,'coin': +coinreward}}
    if item == 2:
       name = "Coal"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"coal": +itemamount,'coin': +coinreward}}
    if item == 3:
       name = "Silver"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"silver": +itemamount,'coin': +coinreward}}
    if item == 4:
       name = "Crimsteel"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"crimsteel": +itemamount,'coin': +coinreward}}
    if item == 5:
       name = "Gold"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"gold": +itemamount,'coin': +coinreward}}
    if item == 6:
       name = "Mythan"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"mythan": +itemamount,'coin': +coinreward}}
    if item == 7:
       name = "Magic"
       adddata = {'$inc':{"prestige": +1,"prestigecoin": +1,"magic": +itemamount,'coin': +coinreward}}
    txt =f"""
Congratulations 🎉 you absolute gamer. You have put in the time, effort, and sometimes tears to reach this point. You have earned this prestige and the rewards associated, and don't let anyone tell you otherwise. We're proud of you
```
Earned Items
``````
{itemamount}x {name}
{await command.numtotext(coinreward)} Coin
1 Prestige Coin
```
"""
    await datack.update_one(query,newdata)
    await datack.update_one(query,adddata)
    await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown")