import config
from telebot import  types
import commands as command
import re
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def shopmenu(call):
    keyboard = types.InlineKeyboardMarkup()
    prestige_button = types.InlineKeyboardButton(text='🔰 Prestige Shop',callback_data='prestige_shop')
    buy_button = types.InlineKeyboardButton(text='🔰 Buy',callback_data='buy menu shop')
    sell_button = types.InlineKeyboardButton(text='🔰 Sell',callback_data='sell menu shop')
    farm_button = types.InlineKeyboardButton(text='👨🏻‍🌾 Farm Shop',callback_data='farm_shop menu shop')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(prestige_button)
    keyboard.add(buy_button,sell_button)
    keyboard.add(farm_button)
    keyboard.add(back_button)
    text = f"""
*[SHOP]*
```
Select Option
```
"""
    await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def prestigeshop(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   prestigecoin = datafind['prestigecoin']
   itemmulti = datafind['itemmulti']
   xpmulti = datafind['xpmulti']
   itemmulti_button = types.InlineKeyboardButton(text='🔰 Item Multiplier', callback_data='itemmulti')
   xpmulti_button = types.InlineKeyboardButton(text='🔰 XP Multiplier', callback_data='xpmulti')
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='shop')
   keyboard.add(itemmulti_button,xpmulti_button)
   keyboard.add(back_button)
   text = f"""
*[PRESTIGE SHOP]*
```
Prestige Coins: {prestigecoin}
- Item Multiplier: {itemmulti}x
- XP Multiplier: {xpmulti}x
``````⚠️
Increase Boost By {config.itemmul}x with Prestige Coin
```
"""
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def itemmulti_use_ask(call):
  old_text = call.message.text
  text_updated = re.sub(r'\[PRESTIGE SHOP\]\s*|Increase Boost By 0.25x with Prestige Coin','', old_text)
  text = f"""
*[ITEM MULTIPLIER]*
```
{text_updated}``````⚠️
Are You Sure ?
```
"""
  keyboard = types.InlineKeyboardMarkup()
  confirm_button = types.InlineKeyboardButton(text='✅ Yes', callback_data='confirm_itemmulti')
  back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='prestige_shop')
  keyboard.add(confirm_button,back_button)
  await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def itemmulti_use(call):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   prestigecoin = datafind['prestigecoin']
   itemmulti = datafind['itemmulti']
   query = {}
   if prestigecoin > 0:
     if itemmulti == 1:
       increased = 1+config.itemmul
       addmulti = {"$inc":{'itemmulti': +config.itemmul,'prestigecoin': -1}}
     else:
      increased = itemmulti + config.itemmul
      addmulti = {"$inc":{'itemmulti': +config.itemmul,'prestigecoin': -1}}
     text = f"""
```
Item Multiplier Increased To {increased}x
```
"""
     await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown")
     await datack.update_one(query,addmulti)
   else:
    text = f"""
```
You Don't Have Any Prestige Coin
```
"""
    await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown")
   return await command.send_home_v2(call.message)
async def xpmulti_use_ask(call):
  old_text = call.message.text
  text_updated = re.sub(r'\[PRESTIGE SHOP\]\s*|Increase Boost By 0.25x with Prestige Coin','', old_text)
  text = f"""
*[XP MULTIPLIER]*
```
{text_updated}``````⚠️
Are You Sure ?
```
"""
  keyboard = types.InlineKeyboardMarkup()
  confirm_button = types.InlineKeyboardButton(text='✅ Yes', callback_data='confirm_xpmulti')
  back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='prestige_shop')
  keyboard.add(confirm_button,back_button)
  await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def xpmulti_use(call):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   prestigecoin = datafind['prestigecoin']
   xpmulti = datafind['xpmulti']
   query = {}
   if prestigecoin > 0:
     if xpmulti == 1:
       increased = 1 + config.xpmul
       addmulti = {"$inc":{'xpmulti': +config.xpmul,'prestigecoin': -1}}
     else:
       increased = xpmulti + config.xpmul
       addmulti = {"$inc":{'xpmulti': +config.xpmul,'prestigecoin': -1}}
     text = f"""
```
XP Multiplier Increased To {increased}x
```
"""
     await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown")
     await datack.update_one(query,addmulti)
   else:
    text = f"""
```
You Don't Have Any Prestige Coin
```
"""
    await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown")
   return await command.send_home_v2(call.message)

async def sell_items_all_ask(call,reference):
   keyboard = types.InlineKeyboardMarkup()
   sell_button = types.InlineKeyboardButton(text=f'Confirm',callback_data=f'sell xall {reference}')
   back_button = types.InlineKeyboardButton(text=f'Back',callback_data=f'sell menu {reference}')
   text = f"""
```
Are you sure that you want to sell all items ?
```
```⚠️
You have the option to modify this confirmation in the settings
```
"""
   keyboard.add(sell_button,back_button)
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def sellmenu(call,reference):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = await command.numtotext(datafind['coin'])
   iron = datafind['iron']
   coal = datafind['coal']
   silver = datafind['silver']
   crimsteel = datafind['crimsteel']
   gold = datafind['gold']
   mythan = datafind['mythan']
   magic = datafind['magic']
   sell_all = datafind['sell_all']
   iron_price = config.ironprice
   coal_price = config.coalprice
   silver_price = config.silverprice
   crimsteel_price = config.crimsteelprice
   gold_price = config.goldprice
   mythan_price = config.mythanprice
   magic_price = config.magicprice
   if sell_all == 1:
     sell_all_msg = "all_ask"
   else:
     sell_all_msg = "xall"
   text = f"""
*Select Item To Sell*
```
Current Coin: {coin}
``` Iron: {iron_price}
Coal: {coal_price}
Silver: {silver_price}
Crimsteel: {crimsteel_price}
Gold: {gold_price}
Mythan: {mythan_price}
Magic: {magic_price}
```⚠️
Warning: Click The Item To Sell All
```
"""
   keyboard = types.InlineKeyboardMarkup()
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   iron_button = types.InlineKeyboardButton(text=f'Iron({await command.numtotext(iron)})', callback_data=f'sell iron {reference}') 
   coal_button = types.InlineKeyboardButton(text=f'Coal({await command.numtotext(coal)})', callback_data=f'sell coal {reference}')  
   silver_button = types.InlineKeyboardButton(text=f'Silver({await command.numtotext(silver)})', callback_data=f'sell silver {reference}')    
   crimsteel_button = types.InlineKeyboardButton(text=f'Crimsteel({await command.numtotext(crimsteel)})', callback_data=f'sell crimsteel {reference}')    
   gold_button = types.InlineKeyboardButton(text=f'Gold({await command.numtotext(gold)})', callback_data=f'sell gold {reference}')  
   mythan_button = types.InlineKeyboardButton(text=f'Mythan({await command.numtotext(mythan)})', callback_data=f'sell mythan {reference}')    
   magic_button = types.InlineKeyboardButton(text=f'Magic({await command.numtotext(magic)})', callback_data=f'sell magic {reference}')
   sell_all_button = types.InlineKeyboardButton(text=f'Sell All', callback_data=f'sell {sell_all_msg} {reference}')
   if reference == "inventory":
     reference = "inventory mine"
   back_button = types.InlineKeyboardButton(text=f'🔙 Back', callback_data=reference)
   keyboard.add(iron_button,coal_button,silver_button)
   keyboard.add(crimsteel_button)
   keyboard.add(gold_button,mythan_button,magic_button)
   keyboard.add(sell_all_button)
   keyboard.add(home_button,back_button)
   try:
     await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
   except:
     ...
async def buymenu(call,reference):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = await command.numtotext(datafind['coin'])
   minex = datafind["minex"]
   xpboost = datafind["xpboost"]
   minex_price = config.minexprice
   xpboost_price = config.xpboostprice
   text = f"""
*Select Item To Buy*
```
Current Coin: {coin}
``````Price
MineX: {await command.numtotext(minex_price)}
XP Boost: {await command.numtotext(xpboost_price)}
```
"""
   keyboard = types.InlineKeyboardMarkup()
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   minex_button = types.InlineKeyboardButton(text=f'MineX({minex})', callback_data=f'buy minex {reference}')    
   xpboost_button = types.InlineKeyboardButton(text=f'XP Boost({xpboost})', callback_data=f'buy xpboost {reference}')  
   if reference == "inventory":
     reference = "inventory mine"
   back_button = types.InlineKeyboardButton(text=f'🔙 Back', callback_data=reference)
   keyboard.add(minex_button,xpboost_button)
   keyboard.add(home_button,back_button)
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)