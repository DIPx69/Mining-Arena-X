import config
import commands as command
import json
import aiofiles
import asyncio
import time

from telebot import types
from telebot.types import ForceReply, ReplyKeyboardMarkup

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

async def buy_minex(call, reference):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind['coin']
   coin_text = await command.numtotext(coin)
   minex = datafind['minex']
   canbuy = int(coin / config.minexprice)
   buy_1st_txt = str(canbuy) if canbuy > 0 else ""
   buy_2nd_txt = str(int(canbuy/2)) if int(canbuy/2) > 0 else ""
   text = f"""
*[MINEX]*
```
Coin: {coin_text}
``````
Current MineX: {await command.numtotext(minex)}
``````
MineX Price: {await command.numtotext(config.minexprice)}
```━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
   amount_buttons = [types.InlineKeyboardButton(text=str(i), callback_data=f'buy buy_minex {i} {reference}') if i*config.minexprice <= coin else types.InlineKeyboardButton(text="", callback_data=f'buy buy_minex {i} {reference}') for i in [1,2,3,4,5,6,7,8]]
   buy_1st = types.InlineKeyboardButton(text=buy_2nd_txt, callback_data=f'buy buy_minex {int(canbuy/2)} {reference}')
   buy_2nd = types.InlineKeyboardButton(text=buy_1st_txt, callback_data=f'buy buy_minex {canbuy} {reference}')
   buy_custom = types.InlineKeyboardButton(text='📜 Custom', callback_data='buy minex_custom')
   if reference == "inventory":
     reference = "inventory mine"
   minex_back = types.InlineKeyboardButton(text='🔙 Back', callback_data=f'buy menu {reference}')
   keyboard = types.InlineKeyboardMarkup(row_width=8)
   keyboard.add(*amount_buttons)
   keyboard.add(buy_1st, buy_2nd)
   keyboard.add(buy_custom, minex_back)
   await bot.edit_message_text(text, call.from_user.id, call.message.id, parse_mode="Markdown", reply_markup=keyboard)

async def buy_xpboost(call,reference):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   coin_text = await command.numtotext(datafind['coin'])
   xpboost = datafind['xpboost']
   keyboard = types.InlineKeyboardMarkup(row_width=8)
   canbuy = int(coin/config.xpboostprice)
   if canbuy > 0:
     buy_1st_txt = f"{canbuy}"
   else:
     buy_1st_txt = f""
   if int(canbuy/2) > 0:
     buy_2nd_txt = f"{int(canbuy/2)}"
   else:
     buy_2nd_txt = f""
   text = f"""
*[XPBOOST]*
```
Coin: {coin_text}
``````
Current XPBoost: {await command.numtotext(xpboost)}
``````
XPBoost Price: {await command.numtotext(config.xpboostprice)}
```━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
   amount_buttons = [types.InlineKeyboardButton(text=str(i), callback_data=f'buy buy_xpboost {i} {reference}') if i*config.xpboostprice <= coin else types.InlineKeyboardButton(text="", callback_data=f'buy buy_xpboost {i} {reference}') for i in [1,2,3,4,5,6,7,8]]
   buy_1st = types.InlineKeyboardButton(text=f'{buy_2nd_txt}',callback_data=f'buy buy_xpboost {int(canbuy/2)} {reference}')
   buy_2nd = types.InlineKeyboardButton(text=f'{buy_1st_txt}',callback_data=f'buy buy_xpboost {canbuy} {reference}')
   buy_custom = types.InlineKeyboardButton(text='📜 Custom',callback_data='buy xpboost_custom')
   if reference == "inventory":
     reference = "inventory mine"
   xpboost_back = types.InlineKeyboardButton(text='🔙 Back',callback_data=f'buy menu {reference}')
   keyboard.add(*amount_buttons)
   keyboard.add(buy_1st,buy_2nd)
   keyboard.add(buy_custom,xpboost_back)
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def minex_custom(call):
  # await command.update_window(call)
   text = f"""
*[MINEX]*
```
Enter The Amount You Want To Buy
```
"""
   keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter The Amount")
   await bot.send_message(call.from_user.id,text,parse_mode="Markdown",reply_markup=keyboard)

async def xpboost_custom(call):
 #  await command.update_window(call)
   text = f"""
*[XPBOOST]*
```
Enter The Amount You Want To Buy
```
"""
   keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter The Amount")
   await bot.send_message(call.from_user.id,text,parse_mode="Markdown",reply_markup=keyboard)

async def minex_buy_confirm(message,ammout):
   filename = f'json_data/active_window.json'
   user_id = message.chat.id
   async with aiofiles.open(filename, 'r') as f:
       window = json.loads(await f.read())
   if window[str(user_id)]['message_id']:
      message_id = window[str(user_id)]['message_id']
   idx = str(message.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   minex = datafind['minex']
   try:
    ammout = int(ammout)
   except:
    text = f"""
```
You need to provide a real amount
```
"""
    await asyncio.gather(bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
    return 0
   totalcost = ammout*config.minexprice
   if ammout > 0:
    if totalcost <= coin:
      query = {}
      update = {'$inc': {'minex': ammout,'coin': -totalcost}}
      text = f"""
```
You Have Purchased {await command.numtotext(ammout)} MineX
``````
{await command.numtotext(totalcost)} Coin Removed From Your Account
``````
Current Coin: {await command.numtotext(coin-totalcost)}
``````
Current MineX: {minex+ammout}
```
"""
      await asyncio.gather(datack.update_one(query, update),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),command.send_home_v2(message))
    else:
      more = ((coin - totalcost)*-1)
      text = f"""
```
You Need More {await command.numtotext(more)} Coin To Buy {await command.numtotext(ammout)} MineX
```
"""
      await asyncio.gather(bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
   else:
     text = f"""
```
You need to provide a real amount
```
"""
     await asyncio.gather(bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message)) 

async def xpboost_buy_confirm(message,ammout):
   filename = f'json_data/active_window.json'
   user_id = message.chat.id
   async with aiofiles.open(filename, 'r') as f:
       window = json.loads(await f.read())
   if window[str(user_id)]['message_id']:
      message_id = window[str(user_id)]['message_id']
   idx = str(message.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   xpboost = datafind['xpboost']
   try:
    ammout = int(ammout)
   except:
     text = f"""
```
You need to provide a real amount
```
"""
     await asyncio.gather(bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
     return 0
   totalcost = ammout*config.xpboostprice
   if ammout > 0:
     if totalcost <= coin:
       query = {}
       update = {'$inc': {'xpboost': ammout,'coin': -totalcost}}
       text = f"""
```
You Have Purchased {await command.numtotext(ammout)} XPBoost
``````
{await command.numtotext(totalcost)} Coin Removed From Your Account
``````
Current Coin: {await command.numtotext(coin-totalcost)}
``````
Current XPBoost: {xpboost+ammout}
```
"""
       await asyncio.gather(datack.update_one(query, update),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),command.send_home_v2(message))
     else:
       more = ((coin - totalcost)*-1)
       text = f"""
```
You Need More {await command.numtotext(more)} Coin To Buy {await command.numtotext(ammout)} XPBoost
```
"""
       await asyncio.gather(bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
   else:
     text = f"""
```
You need to provide a real amount
```
"""
     await asyncio.gather(bot.edit_message_text(text,message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
async def minex_buy(call,reference,ammout):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   minex = datafind['minex']
   ammout = int(ammout)
   totalcost = ammout*config.minexprice
   totalcost_text = await command.numtotext(totalcost)
   current_coin = await command.numtotext(coin-totalcost)
   if totalcost <= coin:
     query = {}
     update = {'$inc': {'minex': ammout,'coin': -totalcost}}
     await asyncio.gather(datack.update_one(query, update),bot.answer_callback_query(call.id,text=f"You Have Purchased {await command.numtotext(ammout)} MineX\n{await command.numtotext(totalcost)} Coin Removed From Your Account\nCurrent Coin: {current_coin}\nCurrent MineX: {minex+ammout}", show_alert=True))
     if reference == "inventory":
       reference = "inventory mine"
     await command.buy_minex(call,reference)
   else:
     more = ((coin - totalcost)*-1)
     await bot.answer_callback_query(call.id,text=f"You Need More {await command.numtotext(more)} Coin To Buy {ammout} MineX", show_alert=True)
async def xpboost_buy(call,reference,ammout):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   xpboost = datafind['xpboost']
   ammout = int(ammout)
   totalcost = ammout*config.xpboostprice
   totalcost_text = await command.numtotext(totalcost)
   current_coin = await command.numtotext(coin-totalcost)
   if totalcost <= coin:
     query = {}
     update = {'$inc': {'xpboost': ammout,'coin': -totalcost}}
     await asyncio.gather(datack.update_one(query, update),bot.answer_callback_query(call.id,text=f"You Have Purchased {ammout} XPBoost\n{await command.numtotext(totalcost)} Coin Removed From Your Account\nCurrent Coin: {current_coin}\nCurrent XPBoost: {xpboost+ammout}", show_alert=True))
     if reference == "inventory":
       reference = "inventory mine"
     await command.buy_xpboost(call,reference)
   else:
     more = ((coin - totalcost)*-1)
     await bot.answer_callback_query(call.id,text=f"You Need More {await command.numtotext(more)} Coin To Buy {ammout} XPBoost", show_alert=True)