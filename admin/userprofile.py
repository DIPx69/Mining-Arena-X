from datetime import datetime, timedelta
import time
import commands as command

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def adminprofile(message):
  try:
    if message.chat.id != ownerid:
       userx = message.from_user
       username = userx.username
       username = username.replace("_", "\\_")
       await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
    else:
      send = await bot.send_message(message.chat.id,"Finding User Profile")
      getid = str(message.text.split()[1])
      user = await bot.get_chat(getid)
      username = user.username
      username = username.replace("_", "\\_")
      db = client["user"]
      datack = db[getid]
      datafind = await datack.find_one()
      coin = datafind["coin"]
      coin_stx = await command.numtotext(datafind["coin"])
      coin_str = coin_stx.replace(".","\.")
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
      nowtime = int(time.time())
      txt =f"*\[PROFILE \- @{username}\]*\n\n \- Total Coin : ₪ *\\{coin} \[{coin_str}\]*\n \- ID : `{getid}`\n\n \- Prestige Level: *{prestigelvl}*\n \- Prestige Coin: *{prestigecoin}*\n\n*\[MINING STATS\]*\n \- Total Mining : *{totalmine}*\n \- Level : *{lvl}*\n \- XP BAR : *{xp}/{nxtlvlxp}*\n\n*\[OTHER INFO\]*\n \- Next Daily: *{nxttime}*\n \- In *{dailytimeleft}* Second `{timestamp2}`\n\n \- {minetxt}\n \- Auto Mine Level: *{autominelvl}*\n\n*\[MULTIPLIER\]*\n \- Item Multiplier *{itemmulti}x*\n \- XP Multiplier *{xpmulti}x*\n\n*\[INVENTORY\]*\n \- Iron: *{iron}*\n \- Coal: *{coal}*\n \- Silver: *{silver}*\n \- Crimsteel: *{crimsteel}*\n \- Gold: *{gold}*\n \- Mythan: *{mythan}*\n \- Magic: *{magic}*\n\n*\[ITEMS\]*\n \- MineX: *{minex}*\n \- XP Boost: *{xpboost}*\n\n \- Reply This Message With /re To Refresh"
      await bot.edit_message_text(txt,message.chat.id,send.message_id,parse_mode="MarkdownV2")
  except Exception as e: 
    print(str(e))
    await bot.edit_message_text("Invalid Id",message.chat.id,send.message_id,parse_mode="MarkdownV2")
async def refresh(message,getid):
      await bot.edit_message_text("*Refreshing*",message.chat.id,message.reply_to_message.message_id,parse_mode="MarkdownV2")
      user = await bot.get_chat(getid)
      username = user.username
      username = username.replace("_", "\\_")
      db = client["user"]
      datack = db[str(getid)]
      datafind = await datack.find_one()
      coin = datafind["coin"]
      coin_stx = await command.numtotext(datafind["coin"])
      coin_str = coin_stx.replace(".","\.")
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
      nowtime = int(time.time())
      txt =f"*\[PROFILE \- @{username}\]*\n\n \- Total Coin : ₪ *\\{coin} \[{coin_str}\]*\n \- ID : `{getid}`\n\n \- Prestige Level: *{prestigelvl}*\n \- Prestige Coin: *{prestigecoin}*\n\n*\[MINING STATS\]*\n \- Total Mining : *{totalmine}*\n \- Level : *{lvl}*\n \- XP BAR : *{xp}/{nxtlvlxp}*\n\n*\[OTHER INFO\]*\n \- Next Daily: *{nxttime}*\n \- In *{dailytimeleft}* Second `{timestamp2}`\n\n \- {minetxt}\n \- Auto Mine Level: *{autominelvl}*\n\n*\[MULTIPLIER\]*\n \- Item Multiplier *{itemmulti}x*\n \- XP Multiplier *{xpmulti}x*\n\n*\[INVENTORY\]*\n \- Iron: *{iron}*\n \- Coal: *{coal}*\n \- Silver: *{silver}*\n \- Crimsteel: *{crimsteel}*\n \- Gold: *{gold}*\n \- Mythan: *{mythan}*\n \- Magic: *{magic}*\n\n*\[ITEMS\]*\n \- MineX: *{minex}*\n \- XP Boost: *{xpboost}*\n\n \- Reply This Message With /re To Refresh"
      await bot.edit_message_text(txt,message.chat.id,message.reply_to_message.message_id,parse_mode="MarkdownV2")