import config
import aiofiles
import json
import commands as command
import asyncio

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023

async def farm_shop_buy_menu(call, reference):
   keyboard = types.InlineKeyboardMarkup()
   buy_plants = types.InlineKeyboardButton(text='🧺 Buy Plants',callback_data=f'farm_shop plants_buy {reference}')
   buy_seeds = types.InlineKeyboardButton(text='🧺 Buy Seeds',callback_data=f'farm_shop seeds_buy {reference}')
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data=f'farm_shop menu {reference}')
   keyboard.add(buy_plants,buy_seeds)
   keyboard.add(home_button,back_button)
   await bot.edit_message_text("*[FARM BUY SHOP]*\n\n*Select Option*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def buy_seeds_menu(call,reference):
   icons = {
    "potato": "🥔",
    "potato_seed": "🥔",
    "corn": "🌽",
    "corn_seed": "🌽",
    "carrot": "🥕",
    "carrot_seed": "🥕",
    "broccoli": "🥦",
    "broccoli_seed": "🥦",
    "watermelon": "🍉",
    "watermelon_seed": "🍉"}
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = await command.numtotext(datafind['coin'])
   potato = datafind['potato_seed']
   corn = datafind['corn_seed']
   carrot = datafind['carrot_seed']
   broccoli = datafind['broccoli_seed']
   watermelon = datafind['watermelon_seed']
   potato_price = config.potato_seeds*config.multi_price
   corn_price = config.corn_seeds*config.multi_price
   carrot_price = config.carrot_seeds*config.multi_price
   broccoli_price = config.broccoli_seeds*config.multi_price
   watermelon_price = config.watermelon_seeds*config.multi_price
   txt = f"""
*Select Seeds To Buy*

- Current Coin: *{coin}*

*Price Table*
- 🥔 Potato Seeds: {await command.numtotext(potato_price)} || *[{await command.numtotext(datafind['potato_seed'])}]*
- 🌽 Corn Seeds: {await command.numtotext(corn_price)} || *[{await command.numtotext(datafind['corn_seed'])}]*
- 🥕 Carrot Seeds: {await command.numtotext(carrot_price)} || *[{await command.numtotext(datafind['carrot_seed'])}]*
- 🥦 Broccoli Seeds: {await command.numtotext(broccoli_price)} || *[{await command.numtotext(datafind['broccoli_seed'])}]*
- 🍉 Watermelon Seeds: {await command.numtotext(watermelon_price)} || *[{await command.numtotext(datafind['watermelon_seed'])}]*

Tips: *Can't Find 💦 Water ?*
*Go To Daily And Claim 💦 Water For Free*
"""
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text=f'🔙 Back', callback_data=f'farm_shop menu {reference}')
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   potato_button = types.InlineKeyboardButton(text=f'🥔 Potato({await command.numtotext(potato)})', callback_data=f'farm_seed_buy potato_seed {reference}') 
   corn_button = types.InlineKeyboardButton(text=f'🌽 Corn({await command.numtotext(corn)})', callback_data=f'farm_seed_buy corn_seed {reference}')  
   carrot_button = types.InlineKeyboardButton(text=f'🥕 Carrot({await command.numtotext(carrot)})', callback_data=f'farm_seed_buy carrot_seed {reference}')    
   broccoli_button = types.InlineKeyboardButton(text=f'🥦 Broccoli({await command.numtotext(broccoli)})', callback_data=f'farm_seed_buy broccoli_seed {reference}')    
   watermelon_button = types.InlineKeyboardButton(text=f'🍉 Watermelon({await command.numtotext(watermelon)})', callback_data=f'farm_seed_buy watermelon_seed {reference}')  
   keyboard.add(potato_button,corn_button,carrot_button)
   keyboard.add(broccoli_button,watermelon_button)
   keyboard.add(home_button,back_button)
   try:
     await bot.edit_message_text(txt, call.from_user.id, call.message.id, parse_mode="Markdown", reply_markup=keyboard)
   except:
     ...
async def buy_seed(call,seed_name,reference):
   seed_name_old = seed_name
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   coin_text = await command.numtotext(datafind['coin'])
   seed_quantity = datafind[seed_name]
   keyboard = types.InlineKeyboardMarkup(row_width=8)
   seed_price = getattr(config, f"{seed_name.lower()}s")*config.multi_price
   seed_name = seed_name.replace("_"," ")
   max_buy = int(coin/seed_price)
   txt = f"*[{seed_name.title()}]*\n\n- Coin: *{coin_text}*\n- Current {seed_name.title()}: *{seed_quantity}*\n- {seed_name.title()} Price: *{await command.numtotext(seed_price)}*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*Click The Amount Or Use Custom*\n"
   amount_buttons = [types.InlineKeyboardButton(text=str(i), callback_data=f'farm_seed buy {seed_name_old} {i} {reference}') if i* seed_price <= coin else types.InlineKeyboardButton(text="", callback_data=f'farm_seed buy {seed_name_old} {i} {reference}') for i in [1,2,3,4,5,6,7,8]]
   buy_custom = types.InlineKeyboardButton(text='📜 Custom',callback_data=f'farm_seed buy {seed_name_old} custom')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data=f'farm_shop seeds_buy {reference}')
   keyboard.add(*amount_buttons)
   if max_buy > 8:
     buy_1st = types.InlineKeyboardButton(text=f'{max_buy}',callback_data=f'farm_seed buy {seed_name_old} {max_buy} {reference}')
     keyboard.add(buy_1st)
   keyboard.add(buy_custom,back_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def buy_seeds(call,seeds_key,quantity,reference,edit=True):
   icons = {
    "potato": "🥔",
    "potato_seed": "🥔",
    "corn": "🌽",
    "corn_seed": "🌽",
    "carrot": "🥕",
    "carrot_seed": "🥕",
    "broccoli": "🥦",
    "broccoli_seed": "🥦",
    "watermelon": "🍉",
    "watermelon_seed": "🍉"}
   seeds_name = seeds_key.capitalize()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   item_quantity = datafind[seeds_key]
   ammout = int(quantity)
   item_price = getattr(config, f"{seeds_key.lower()}s")
   totalcost = ammout*item_price*config.multi_price
   totalcost_text = await command.numtotext(totalcost)
   current_coin = await command.numtotext(coin-totalcost)
   name = seeds_name.replace("_"," ")
   if totalcost <= coin:
     query = {}
     update = {'$inc': {seeds_key: ammout,'coin': -totalcost}}
     await asyncio.gather(datack.update_one(query, update),bot.answer_callback_query(call.id,text=f"You Have Purchased {await command.numtotext(ammout)} {icons[seeds_name.lower()]} {name.title()}\n{await command.numtotext(totalcost)} Coin Removed From Your Account\nCurrent Coin: {current_coin}\nCurrent {name.title()}: {item_quantity+ammout}", show_alert=True))
     if reference == "inventory":
       reference = "inventory mine"
     await command.buy_seed(call,seeds_key,reference)
   else:
     more = ((coin - totalcost)*-1)
     await bot.answer_callback_query(call.id,text=f"You Need More {await command.numtotext(more)} Coin To Buy {ammout} {icons[seeds_name.lower()]}  {name.title()}", show_alert=True)
async def buy_seeds_custom(call,item_name):
  name = item_name.title()
  txt = f'*[BUY {name.replace("_"," ")}]*\n\n*Enter The Amount You Want To Buy*'
  keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter The Amount")
  await bot.send_message(call.from_user.id,txt,parse_mode="Markdown",reply_markup=keyboard)

async def seeds_buy_custom(message,seeds_name,ammout):
   icons = {
    "potato": "🥔",
    "potato_seed": "🥔",
    "corn": "🌽",
    "corn_seed": "🌽",
    "carrot": "🥕",
    "carrot_seed": "🥕",
    "broccoli": "🥦",
    "broccoli_seed": "🥦",
    "watermelon": "🍉",
    "watermelon_seed": "🍉"}
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
   print("Hi")
   item_quantity = datafind[f"{seeds_name.lower()}"]
   item_price = price = getattr(config, f"{seeds_name.lower()}s")
   print(ammout)
   try:
    ammout = int(ammout)
   except:
    await asyncio.gather(bot.edit_message_text(f"*You need to provide a real amount*",message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
    return 0
   totalcost = ammout*item_price*config.multi_price
   totalcost_text = await command.numtotext(totalcost)
   current_coin = await command.numtotext(coin-totalcost)
   name = seeds_name.replace("_"," ")
   if ammout > 0:
    if totalcost <= coin:
      query = {}
      update = {'$inc': {seeds_name: ammout,'coin': -totalcost}}
      await asyncio.gather(datack.update_one(query, update),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),bot.edit_message_text(f"You Have Purchased *{await command.numtotext(ammout)}* {icons[seeds_name.lower()]} *{name.title()}*\n*{await command.numtotext(totalcost)}* Coin Removed From Your Account\nCurrent Coin: *{await command.numtotext(coin-totalcost)}*\nCurrent {name.title()}: *{item_quantity+ammout}*",message.chat.id,message_id,parse_mode="Markdown"),command.send_home_v2(message))
    else:
      more = ((coin - totalcost)*-1)
      await asyncio.gather(bot.edit_message_text(f"You Need More *{await command.numtotext(more)}* Coin To Buy *{await command.numtotext(ammout)}* {name.title()}",message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
   else:
     await asyncio.gather(bot.edit_message_text(f"*You need to provide a real amount*",message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message)) 