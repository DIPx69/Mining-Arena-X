import os

import commands as command
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def profile(call):
   keyboard = types.InlineKeyboardMarkup()
   prestige_button = types.InlineKeyboardButton(text='💊 Prestige',callback_data='prestige')
   title_button = types.InlineKeyboardButton(text='📄 Titles',callback_data='title')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
   keyboard.add(title_button)
   keyboard.add(prestige_button,back_button)
   userx = call.from_user
   username = userx.username
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   await command.mine_check(call,datafind)
   coin = await command.numtotext(datafind["coin"])
   lvl = datafind["lvl"]
   totalmine = datafind['mymine']
   xp = datafind['xp']
   prestigelvl = datafind['prestige']
   prestigecoin = datafind['prestigecoin']
   query = {}
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
   if xp >= nxtlvlxp:
      extra = xp-nxtlvlxp
      update = {
    '$inc': {'lvl': +1, 'nxtlvlxp': +50},
    '$set': {'xp': extra}}
      await datack.update_one(query, update)
      await bot.send_message(call.from_user.id,f"*You Have Level Up To {(lvl+1)}*\nAdd *{extra}* XP As Extra XP",parse_mode="Markdown")
   text3 = f"""
```
@{username} - {active_title}
``````Balance
- Coin: {coin}
- ID: {idx}
``````Prestige
- Prestige Level: {prestigelvl}
- Prestige Coin: {prestigecoin}
``````MINING
- Total Mining: {await command.numtotext(totalmine)}
- Level: {lvl}
- XP BAR: {xp}/{nxtlvlxp}
``````GAME
- 🎲[{dice_won}||{dice_lose}||{dice_total}]
- 🎯[{dart_won}||{dart_lose}||{dart_total}]
- 🏀[{basketball_won}||{basketball_lose}||{basketball_total}]
- ⚽[{football_won}||{football_lose}||{football_total}]  
```
"""
   txt2 = f"*[ @{username} - {active_title} ]*\n\n - Coin: *{coin}*\n - ID: `{idx}`\n\n - Prestige Level: *{prestigelvl}*\n - Prestige Coin: *{prestigecoin}* 🪙 \n\n*[MINING STATS]*\n - Total Mining: *{await command.numtotext(totalmine)}*\n - Level: *{lvl}*\n - XP BAR: *{xp}/{nxtlvlxp}*\n\n*[MINI GAME STATS]*  *Win/Lose/Total*\n -   🎲   *[ {dice_won} || {dice_lose} || {dice_total} ]*\n -   🎯   *[ {dart_won} || {dart_lose} || {dart_total} ]*\n -   🏀   *[ {basketball_won} || {basketball_lose} || {basketball_total} ]*\n -   ⚽   *[ {football_won} || {football_lose} || {football_total} ]*\n"
   await bot.edit_message_text(text3,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)