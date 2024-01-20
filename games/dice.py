import config
import time
import asyncio

from telebot import types

import commands as command
import slash_command as slash

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
from games.basketball import bot_rate
ownerid = 1794942023
async def send_dice(message):
  try:
   dice_emojis = {
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣' }
   nowtime = int(time.time())
   try:
     getvalue = int(message.text.split()[1])
   except:
     text = f"""
```
Choose An Option Between 1\-6
``````Example
/roll 5 100k
```
 """
     await bot.reply_to(message,text,parse_mode="MarkdownV2")
     return 0
   try:
     getcoin = message.text.split()[2]
     getcoin = await command.txttonum(getcoin)
   except:
     text = f"""
```
Provide a Bet Ammout
``````Example
/roll 2 100k
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
   values = [1,2,3,4,5,6]
   cooldownx = nowtime - cooldown
   if getcoin <= coin and getvalue in values and cooldownx >= config.gamecooldown and getcoin > 0 and ban == 0:
      text = f"""
```
🍀 Good Luck!
```
"""
      send = await bot.reply_to(message,text,parse_mode="Markdown")
      msg = await bot.send_dice(message.chat.id)
      value = msg.dice.value
      print(value)
      emoji = dice_emojis.get(value)
      if value % 2 == 0:
         result = "EVEN"
      else:
         result = "ODD"
      if value == getvalue:
         status = "Won"
         updatecoin = getcoin * 5
         txtcoin = updatecoin
         update = {'$inc': {'coin': updatecoin,'dice_won': 1}}
      else:
         status = "Lost"
         updatecoin = getcoin * -1
         txtcoin = getcoin
         update = {'$inc': {'coin': updatecoin,'dice_lose': 1}}
      txt = f"{emoji} – {result}\nYou Have {status} ₪ {await command.numtotext(txtcoin)} Coin"
      txt = f"""
```
{txt}
```
"""
      await asyncio.sleep(3)
      await bot.edit_message_text(txt,message.chat.id,send.message_id,parse_mode="Markdown")
      nextcooldown = int(time.time())
      updatex = {'$set': {'gamecooldown': nextcooldown}}
      update.update(updatex)
      await userdatack.update_one(query,update)
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
   elif getvalue not in values:
     text = f"""
```
Choose An Option Between 1\-6
``````Example
/roll 5 100k
```
 """
   elif cooldownx <= config.gamecooldown:
     cooldown_time = (config.gamecooldown-cooldownx)
     text = f"""
```
Try Again In {cooldown_time} Second
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
  except Exception as e:
   print(str(e))
   retry_after = int(e.result.headers['Retry-After'])
   await slash.send_alert(message,retry_after)