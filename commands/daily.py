import telebot
import json
import os
import time
from datetime import datetime, timedelta
import asyncio
import config
import aiofiles
import commands as command
from telebot import types
import dns.resolver
import motor.motor_asyncio
from telebot.async_telebot import *
from telebot import types
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
channel_usernames = ['@MiningArenaUpdates', '@MiningArenaChats']
async def dailyx(call):
   idx = str(call.from_user.id)
   nxtclaimtimen = int((time.time() + config.dailycooldown))
   db = client["user"]
   collection = db[idx]
   query = {}
   update = {'$inc': {'coin': config.dailycoin},'$set': {'dailycooldown': nxtclaimtimen}}
   await collection.update_one(query, update)
async def verify(message):
    channel_1 = '@MiningArenaUpdates'
    channel_2 = '@MiningArenaChats'
    txt = "*Verifying Membership 📝*"
    send = await bot.send_message(message.chat.id,txt,parse_mode="Markdown")
    user_id = str(message.chat.id)
    chat_verify_1 = await bot.get_chat_member(channel_1, user_id)
    chat_verify_2 = await bot.get_chat_member(channel_2, user_id)
    if chat_verify_1.status != 'left' and chat_verify_2.status != 'left':
       msgid = str(message.id)
       await dailyMenu(message)
       await bot.delete_message(message.chat.id,send.message_id)
    else:
       markup = types.InlineKeyboardMarkup(row_width=2)
       button1_text = '@MiningArenaUpdates'
       button1_url = 'https://t.me/MiningArenaUpdates'
       button1 = types.InlineKeyboardButton(text=button1_text, url=button1_url)
       button2_text = '@MiningArenaChats'
       button2_url = 'https://t.me/MiningArenaChats'
       button2 = types.InlineKeyboardButton(text=button2_text, url=button2_url)
       if chat_verify_1.status == 'left' and chat_verify_2.status == 'left':
         markup.row(button1,button2)
       elif chat_verify_1.status == 'left':
            markup.row(button1)
       elif chat_verify_2.status == 'left':
            markup.row(button2)
       if chat_verify_1.status == "left":
          channel_1_status = ""
       else:
          channel_1_status = "\[JOINED\]"
       if chat_verify_2.status == "left":
          channel_2_status = ""
       else:
          channel_2_status = "\[JOINED\]"
       txtx = f"*You Need To Join This Channel To Claim Daily Bonus*\n@MiningArenaUpdates *{channel_1_status}*\n@MiningArenaChats *{channel_2_status}*"
       await bot.edit_message_text(txtx,message.chat.id,send.message_id,parse_mode="MarkdownV2",reply_markup=markup)
async def dailycooldown(call):
   timestamp = int(time.time())
   idx = str(call.from_user.id)
   db = client["user"]
   collection = db[idx]
   datafind = await collection.find_one()
   timestamp2 = datafind['dailycooldown']
   dt = datetime.fromtimestamp(timestamp2)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   nxttime = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   timestamp = int(time.time())
   if timestamp < timestamp2:
     await bot.answer_callback_query(call.id, text=f"You Can Claim Again In {await command.time_left(timestamp2)}\n{nxttime}", show_alert=True)
     await dailyMenu(call)
   else:
      await dailyMenu(call)
async def dailyclaim(call):
   timestamp = int(time.time())
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   timestamp2 = datafind['dailycooldown']
   streaks = datafind['streaks']
   difference = timestamp - timestamp2
   query = {}
   nxtclaimtimen = int((time.time() + config.dailycooldown))
   rewards = config.dailycoin*streaks
   random_water = random.randint(1,config.max_water)
   if timestamp > timestamp2:
      if difference > 172800:
        update = {'$inc': {'coin': rewards,'water': random_water},'$set': {'dailycooldown': nxtclaimtimen,'streaks': 1}}
        await datack.update_one(query, update)
        await bot.answer_callback_query(call.id, text=f"You Have Received {await command.numtotext(rewards)} Coin\n{random_water}x 💦 Water\nYou Have Lost Your Daily Streak", show_alert=True)
      else:
       update = {'$inc': {'coin': rewards,'streaks': +1,'water': random_water},'$set': {'dailycooldown': nxtclaimtimen}}
       await datack.update_one(query, update)
       await bot.answer_callback_query(call.id, text=f"You Have Received {await command.numtotext(rewards)} Coin\n{random_water}x 💦 Water\n+1 Streaks", show_alert=True)
   else:
     await bot.answer_callback_query(call.id, text=f"You Can Claim Again In {await command.time_left(timestamp2)}", show_alert=True)
   await dailyMenu(call)
async def dailyMenu(call):
   timestamp = int(time.time())
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   await command.mine_check(call,datafind)
   timestamp2 = datafind['dailycooldown']
   streaks = datafind['streaks']
   dt = datetime.fromtimestamp(timestamp2)
   dhaka_offset = timedelta(hours=6)
   dt_dhaka = dt + dhaka_offset
   nxttime = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
   keyboard = types.InlineKeyboardMarkup() 
   rewards = config.dailycoin*streaks
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
   if timestamp > timestamp2:
     claim_button = types.InlineKeyboardButton(text='🎁 Claim',callback_data='dailyclaim')
     next_daily = ""
   else:
     time_left = await command.time_left(timestamp2)
     claim_button = types.InlineKeyboardButton(text=f'In {time_left}',callback_data='dailycooldown')
     next_daily = f"- Next Claim: {nxttime}"
   max_water = config.max_water
   text = f"""
```Daily
- Daily Streak: {streaks}
- Rewards: {await command.numtotext(rewards)} || 💦 Water (0-{max_water})
``````
{next_daily}
```
"""
   txt = f"*[Daily Rewards]*\n\n- Daily Streak: {streaks}\n- Rewards: {await command.numtotext(rewards)} || *💦 Water (0-{max_water})* \n{next_daily}"
   keyboard.add(claim_button,back_button)
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def daily(message):
    timestamp = int(time.time())
    idx = str(message.chat.id)
    db = client["user"]
    datack = db[idx]
    datafind = await datack.find_one()
    timestamp2 = datafind['dailycooldown']
    dt = datetime.fromtimestamp(timestamp2)
    dhaka_offset = timedelta(hours=6)
    dt_dhaka = dt + dhaka_offset
    nxttime = dt_dhaka.strftime('%d-%m-%Y %I:%M:%S%p')
    user_id = message.chat.id
    filename = 'json_data/ban.json'
    async with aiofiles.open(filename, 'r') as f:
        ban_ids = json.loads(await f.read())
    if any(user_id == ban_id['id'] for   ban_id in ban_ids):
      await bot.send_message(message.chat.id,"You Can't Take Daily Bonus Since Your Account Is Banned.",parse_mode="Markdown")
    if timestamp < timestamp2:
       await bot.send_message(message.chat.id,f'You Can Claim Again In *{nxttime}*\nIn *{((timestamp - timestamp2)*-1)}* Seconds',parse_mode="Markdown")
    else:
      await dailyx(message)
      await bot.send_message(message.chat.id,f'You Have Received *{config.dailycoin} Coin*',parse_mode="Markdown")