import os
import config
import time

import commands as command
import slash_command as slash

from telebot.async_telebot import *
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

ratelimit = os.getenv("ratelimit")
bot_rate = AsyncTeleBot(ratelimit)
ownerid = 1794942023
async def send_basketball(message):
  try:
   nowtime = int(time.time())
   try:
     getcoin = message.text.split()[1]
     getcoin = await command.txttonum(getcoin)
   except:
     text = f"""
```
Provide a Bet Ammout
``````Example
/basket 100k
```
 """
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   if not (config.min_bet <= getcoin <= config.max_bet):
     text = f"""
```
Minimum Bet: {await command.numtotext(config.min_bet)}
Maximum Bet: {await command.numtotext(config.max_bet)}
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   userdb = client["user"]
   userdatack = userdb[str(message.from_user.id)]
   userdatafind = await userdatack.find_one()
   try:
     cooldown = userdatafind['gamecooldown']
     coin = userdatafind['coin']
     ban = userdatafind['ban']
   except:
     markup = types.InlineKeyboardMarkup(row_width=1)
     text = 'Start @MiningArenaBot'
     url = 'https://t.me/MiningArenaBot?start=start'
     button1 = types.InlineKeyboardButton(text=text, url=url)
     markup.row(button1)
     await bot.reply_to(message,"*You Need Start The Bot*",parse_mode="Markdown",reply_markup=markup)
     return 0
   query = {}
   cooldownx = (cooldown - nowtime)
   cooldownx = cooldownx * -1
   cooldownxx = (config.gamecooldown-cooldownx)-1
   if getcoin <= coin and cooldownx >= config.gamecooldown and getcoin > 0 and ban == 0:
      nextcooldown = int(time.time())
      update = {'$set': {'gamecooldown': nextcooldown}}
      await userdatack.update_one(query,update)
      text = f"""
```
🍀 Good Luck!
```
"""
      send = await bot.reply_to(message,text,parse_mode="Markdown")
      msg = await bot.send_dice(message.chat.id,emoji="🏀")
      value = msg.dice.value
      nextcooldown = int(time.time())
      if value == 5:
         updatecoin = getcoin*3
         coinshow = int(updatecoin)
         txt =f"🤑 SPLAAAAASH\n✅️ You Won  ₪ {await command.numtotext(coinshow)} Coin"
         updatex = {'$inc':{"coin": updatecoin,'basketball_won':1}}
      elif value == 1 or value == 2:
          updatecoin = getcoin*-1
          coinshow = updatecoin*-1
          txt =f"😥 Miss\nYou Lost  ₪ {coinshow} Coin"
          updatex = {'$inc':{"coin": updatecoin,'basketball_lose':1}}
      elif value == 3:
          updatecoin = getcoin*-1
          coinshow = updatecoin*-1
          txt =f"😵 Stuck\nYou Lost  ₪ {await command.numtotext(coinshow)}"
          updatex = {'$inc':{"coin": updatecoin,'basketball_lose':1}}
      elif value == 4:
          updatecoin = getcoin*2
          coinshow = int(updatecoin)
          txt =f"👍 GOOD SHOT\nYou Won  ₪ {await command.numtotext(coinshow)} Coin"
          updatex = {'$inc':{"coin": updatecoin,'basketball_won':1}}
      txt = f"""
```
{txt}
```
"""
      await asyncio.sleep(3)
      await bot.edit_message_text(txt,message.chat.id,send.message_id,parse_mode="Markdown")
      nextcooldown = int(time.time())
      update = {'$set': {'gamecooldown': nextcooldown}}
      updatex.update(update)
      await userdatack.update_one(query,updatex)
   elif ban == 1:
       text = f"""
```
You Can't Play Game Since Your Account Is Banned
```
"""
       await bot.reply_to(message,text,parse_mode="Markdown")
   elif getcoin > coin:
     text = f"""
```
You Don't Have Enough Money To Bet
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
   elif cooldownx <= config.gamecooldown:
       text = f"""
```
Try Again In {cooldownxx} Second
```
"""
       await bot.reply_to(message,text,parse_mode="Markdown")
  except Exception as e:
   print(str(e))
   retry_after = int(e.result.headers['Retry-After'])
   await slash.send_alert(message,retry_after)