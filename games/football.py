import config
import time
import commands as command
import slash_command as slash

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
from games.basketball import bot_rate
ownerid = 1794942023
async def send_football(message):
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
/ball 100k
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
      text = f"""
```
🍀 Good Luck!
```
"""
      send = await bot.reply_to(message,text,parse_mode="Markdown")
      msg = await bot.send_dice(message.chat.id,emoji="⚽")
      value = msg.dice.value
      nextcooldown = int(time.time())
      print(value)
      if value == 1:
          updatecoin = getcoin*-1
          coinshow = updatecoin*-1
          txt =f"😬 Miss\nYou Lost  ₪ {await command.numtotext(coinshow)}"
          updatex = {'$inc':{"coin": updatecoin,'football_lose':1}}
      elif value == 2:
          updatecoin = getcoin*-1
          coinshow = updatecoin*-1
          txt =f"🙄 Bounced...\nYou Lost  ₪ {await command.numtotext(coinshow)}"
          updatex = {'$inc':{"coin": updatecoin,'football_lose':1}}
      elif value == 5 or value == 4 or value == 3:
          updatecoin = getcoin*2
          coinshow = getcoin
          txt =f"⚽️ GOOOOAL!\nYou Won ₪ {await command.numtotext(updatecoin)}"
          updatex = {'$inc':{"coin": updatecoin,'football_won':1}}
      await asyncio.sleep(2)
      txt = f"""
```
{txt}
```
"""
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
   retry_after = int(e.result.headers['Retry-After'])
   await slash.send_alert(message,retry_after)