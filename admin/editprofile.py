import telebot
import os
from datetime import datetime, timedelta
import time
import commands as command
import admin
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023


async def edituser_no_reply(message):
  try:
    user = message.from_user
    username = user.username
    username = username.replace("_", "\\_")
    if message.from_user.id != ownerid:
      await bot.send_message(message.chat.id, "You Can't Run This Command")
      await bot.send_message(ownerid, f'@{username} *({message.from_user.id})* Trying To Run Admin Command', parse_mode="Markdown")
    else:
      text = f"""
```
Trying To Update Data
```
"""
      send = await bot.reply_to(message, text, parse_mode="Markdown")
      data_parts = message.text.split()
      if len(data_parts) < 4:
        await bot.edit_message_text(f"*Try To Fill All Value*", message.chat.id, send.message_id, parse_mode="Markdown")
        return

      getid = int(data_parts[1])
      getname = data_parts[2]
      getvalue = data_parts[3]
      getvalue = await command.txttonum(getvalue)
      idx = str(getid)
      db = client["user"]
      datack = db[idx]
      documents = await datack.find().to_list(None)
      field_set = set()
      for document in documents:
        field_set.update(document.keys())
      field_list = list(field_set)
      dblist = await db.list_collection_names()
      if idx in dblist and getname in field_list:
        user = await bot.get_chat(getid)
        username = user.username
        username = username.replace("_", "\\_")
        query = {}
        update = {'$set': {getname: getvalue}}
        await datack.update_one(query, update)
        text = f"""
```
Data Updated To {getvalue}
Username: @{username}
```
"""
        await bot.edit_message_text(text, message.chat.id, send.message_id, parse_mode="Markdown")
      else:
        if getname not in field_list and idx in dblist:
          await bot.edit_message_text(f"*Value Not Found In Database*", message.chat.id, send.message_id, parse_mode="Markdown")
        if idx not in dblist:
          await bot.edit_message_text(f"*User Not Found In Database*", message.chat.id, send.message_id, parse_mode="Markdown")
  except Exception as e:
    await bot.edit_message_text(f"*An Error Occurred: {e}*", message.chat.id, send.message_id, parse_mode="Markdown")


async def edituser_no_replyx(message):
  try:
    user = message.from_user
    username = user.username
    username = username.replace("_", "\\_")
    if message.from_user.id != ownerid:
      await bot.send_message(ownerid, f'@{username} *({message.from_user.id})* Trying To Run Admin Command', parse_mode="Markdown")
    else:
      send = await bot.send_message(message.chat.id, "*Trying To Update Data*", parse_mode="Markdown")
      getid = int(message.text.split()[1])
      getname = message.text.split()[2]
      getvalue = message.text.split()[3]
      getvalue = await command.txttonum(getvalue)
      idx = str(getid)
      db = client["user"]
      datack = db[idx]
      documents = datack.find()
      field_set = set()
      for document in documents:
        field_set.update(document.keys())
      field_list = list(field_set)
      dblist = await db.list_collection_names()
      if idx in dblist and getname in field_list:
        user = await bot.get_chat(getid)
        username = user.username
        username = username.replace("_", "\\_")
        query = {}
        update = {'$set': {getname: getvalue}}
        await datack.update_one(query, update)
        await bot.edit_message_text(f"*{getname.capitalize()}* Data Updated To *{getvalue}*\nUsername: @{username}", message.chat.id, send.message_id, parse_mode="Markdown")
      else:
        if getname not in field_list and idx in dblist:
          await bot.edit_message_text(f"*Value Not Found In Database*", message.chat.id, send.message_id, parse_mode="Markdown")
        if idx not in dblist:
          await bot.edit_message_text(f"*User Not Found In Database*", message.chat.id, send.message_id, parse_mode="Markdown")
  except:
    await bot.edit_message_text(f"*Try To Fill All Value*", message.chat.id, send.message_id, parse_mode="Markdown")


async def edituser_reply(message, getid):
  try:
    user = message.from_user
    username = user.username
    username = username.replace("_", "\\_")
    if message.from_user.id != ownerid:
      await bot.send_message(ownerid, f'@{username} *({message.from_user.id})* Trying To Run Admin Command', parse_mode="Markdown")
    else:
      await bot.edit_message_text("*Trying To Update Data*", message.chat.id, message.reply_to_message.message_id, parse_mode="Markdown")
      getname = message.text.split()[1]
      getvalue = message.text.split()[2]
      getvalue = await command.txttonum(getvalue)
      idx = str(getid)
      db = client["user"]
      datack = db[idx]
      documents = await datack.find().to_list(None)
      field_set = set()
      for document in documents:
        field_set.update(document.keys())
      field_list = list(field_set)
      dblist = await db.list_collection_names()
      if idx in dblist and getname in field_list:
        user = await bot.get_chat(getid)
        username = user.username
        username = username.replace("_", "\\_")
        query = {}
        update = {'$set': {getname: getvalue}}
        await datack.update_one(query, update)
        user = await bot.get_chat(getid)
        username = user.username
        username = username.replace("_", "\\_")
        db = client["user"]
        datack = db[str(getid)]
        datafind = await datack.find_one()
        coin = datafind["coin"]
        coin_stx = await command.numtotext(datafind["coin"])
        coin_str = coin_stx.replace(".", "\.")
        lvl = datafind["lvl"]
        totalmine = datafind['mymine']
        xp = datafind['xp']
        nxtlvlxp = datafind['nxtlvlxp']
        prestigelvl = datafind['prestige']
        iron = datafind['iron']
        coal = datafind['coal']
        silver = datafind['silver']
        crimsteel = datafind['crimsteel']
        gold = datafind['gold']
        mythan = datafind['mythan']
        magic = datafind['magic']
        minex = datafind['minex']
        xpboost = datafind['xpboost']
        autominelvl = datafind['autominelvl']
        timestamp2 = datafind['dailycooldown']
        dt = datetime.fromtimestamp(timestamp2)
        dhaka_offset = timedelta(hours=6)
        dt_dhaka = dt + dhaka_offset
        nxttime = dt_dhaka.strftime('%d\\-%m\\-%Y %I:%M:%S%p')
        nowtime = time.time()
        dailytimeleft = timestamp2-nowtime
        if dailytimeleft > 0:
          dailytimeleft = int(dailytimeleft)
        else:
          dailytimeleft = 0
          timestamp2 = 0
          nxttime = "Never Take Daily"
        automine = datafind['automineon']
        if automine == 0:
          minetxt = "Auto Mine Is Off"
        else:
          end_time = datafind['end_time']
          dt = datetime.fromtimestamp(end_time)
          dhaka_offset = timedelta(hours=6)
          dt_dhaka = dt + dhaka_offset
          mine_end_time = dt_dhaka.strftime('%d\\-%m\\-%Y %I:%M:%S%p')
          time_left = str(int(end_time-nowtime))
          time_left = time_left.replace("-", "\-")
          minetxt = f"Auto Mine Is On {mine_end_time}\nIn {time_left} Seconds `{end_time}`"
        prestigecoin = datafind['prestigecoin']
        xpmulti = datafind['xpmulti']
        itemmulti = datafind['itemmulti']
        txt = f"*\[PROFILE \- @{username}\]*\n\n \- Total Coin : ₪ *\\{coin} \[{coin_str}\]*\n \- ID : `{getid}`\n\n \- Prestige Level: *{prestigelvl}*\n \- Prestige Coin: *{prestigecoin}*\n\n*\[MINING STATS\]*\n \- Total Mining : *{totalmine}*\n \- Level : *{lvl}*\n \- XP BAR : *{xp}/{nxtlvlxp}*\n\n*\[OTHER INFO\]*\n \- Next Daily: *{nxttime}*\n \- In *{dailytimeleft}* Second `{timestamp2}`\n\n \- {minetxt}\n \- Auto Mine Level: *{autominelvl}*\n\n*\[MULTIPLIER\]*\n \- Item Multiplier *{itemmulti}x*\n \- XP Multiplier *{xpmulti}x*\n\n*\[INVENTORY\]*\n \- Iron: *{iron}*\n \- Coal: *{coal}*\n \- Silver: *{silver}*\n \- Crimsteel: *{crimsteel}*\n \- Gold: *{gold}*\n \- Mythan: *{mythan}*\n \- Magic: *{magic}*\n\n*\[ITEMS\]*\n \- MineX: *{minex}*\n \- XP Boost: *{xpboost}*\n\n \- Reply This Message With /re To Refresh"
        await bot.edit_message_text(txt, message.chat.id, message.reply_to_message.message_id, parse_mode="MarkdownV2")
      else:
        if getname not in field_list and idx in dblist:
          await bot.send_message(message.chat.id, "*Value Not Found In Database*", parse_mode="Markdown")
          await admin.refresh(message, getid)
  except Exception as e:
    print(str(e))
    await bot.send_message(message.chat.id, "*Try To Fill All Value*", parse_mode="Markdown")
    await admin.refresh(message, getid)
