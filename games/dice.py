import telebot
import os
import config
import time
import requests
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
import commands as command
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
ratelimit = os.getenv("ratelimit")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
bot_rate = AsyncTeleBot(ratelimit)
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
     await bot.reply_to(message,"*Choose An Option 1\-6*\nExample `/roll 5 100k`",parse_mode="MarkdownV2")
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
   cooldownx = (cooldown - nowtime)
   cooldownx = cooldownx * -1
   cooldownxx = (config.gamecooldown-cooldownx)-1
   if getcoin <= coin and getvalue in values and cooldownx >= config.gamecooldown and getcoin > 0 and ban == 0:
      nextcooldown = int(time.time())
      update = {'$set': {'gamecooldown': nextcooldown}}
      await userdatack.update_one(query,update)
      send = await bot.reply_to(message,"*🍀 Good Luck!*",parse_mode="Markdown")
      msg = await bot.send_dice(message.chat.id)
      value = msg.dice.value
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
      await userdatack.update_one(query,update)
      txt = f"{emoji} – *{result}*\nYou Have {status} *₪ {txtcoin} Coin*"
      await asyncio.sleep(3)
      await bot.edit_message_text(txt,message.chat.id,send.message_id,parse_mode="Markdown")
   elif ban == 1:
        await bot.reply_to(message,"*You Can't Play Game Since Your Account Is Banned*",parse_mode="Markdown")
   elif getcoin == 0:
        await bot.reply_to(message,"*Bruh Don't Provide Zero Bet lol*",parse_mode="Markdown")
   elif getcoin < 0:
        await bot.reply_to(message,"*Bruh Don't Provide Negetive Bet lol xd*",parse_mode="Markdown")
   elif getcoin > coin:
        await bot.reply_to(message,"*You Don't Have Enough Money To Bet*",parse_mode="Markdown")
   elif getvalue not in values:
        await bot.reply_to(message,"*Choose Value Between 1-6*\nExample /roll 5 69k",parse_mode="Markdown")
   elif cooldownx <= config.gamecooldown:
        await bot.reply_to(message,f"*Try Again In {cooldownxx} Second*",parse_mode="Markdown")
  except Exception as e:
    retry_after = int(e.result.headers['Retry-After'])
    try:
     await bot.delete_message(message.chat.id,send.message_id)
     await bot_rate.send_message(message.chat.id,f"*Rate Limited*\nTry Again After *{retry_after}* Seconds",parse_mode="Markdown")
    except:
     await bot.send_message(message.from_user.id,f"*Rate Limited*\nTry Again After *{retry_after}* Seconds",parse_mode="Markdown")