import config
import aiofiles
import json
from telebot import  types
import commands as command

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023

async def farm_shop_sell_menu(call, reference):
   keyboard = types.InlineKeyboardMarkup()
   sell_plants = types.InlineKeyboardButton(text='🧺 Sell Plants',callback_data=f'farm_shop plants_sell {reference}')
   sell_seeds = types.InlineKeyboardButton(text='🧺 Sell Seeds',callback_data=f'farm_shop seeds_sell {reference}')
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data=f'farm_shop menu {reference}')
   keyboard.add(sell_plants,sell_seeds)
   keyboard.add(home_button,back_button)
   await bot.edit_message_text("*[FARM SELL SHOP]*\n\n*Select Option*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def sell_seeds_menu(call,reference):
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
   sell_all = datafind['sell_all']
   potato_price = config.potato_seeds
   corn_price = config.corn_seeds
   carrot_price = config.carrot_seeds
   broccoli_price = config.broccoli_seeds
   watermelon_price = config.watermelon_seeds
   if sell_all == 1:
     sell_all_msg = "all_ask"
   else:
     sell_all_msg = "all"
   txt = f"""
*Select Seeds To Sell*

- Current Coin: *{coin}*

*Price Table*
- 🥔 Potato Seeds: {await command.numtotext(potato_price)} || *[{await command.numtotext(datafind['potato_seed'])}]*
- 🌽 Corn Seeds: {await command.numtotext(corn_price)} || *[{await command.numtotext(datafind['corn_seed'])}]*
- 🥕 Carrot Seeds: {await command.numtotext(carrot_price)} || *[{await command.numtotext(datafind['carrot_seed'])}]*
- 🥦 Broccoli Seeds: {await command.numtotext(broccoli_price)} || *[{await command.numtotext(datafind['broccoli_seed'])}]*
- 🍉 Watermelon Seeds: {await command.numtotext(watermelon_price)} || *[{await command.numtotext(datafind['watermelon_seed'])}]*
"""
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text=f'🔙 Back', callback_data=f'farm_shop sell_menu {reference}')
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   all_button = types.InlineKeyboardButton(text=f'Sell All',callback_data=f'farm_seed sell {sell_all_msg} {reference}')
   potato_button = types.InlineKeyboardButton(text=f'🥔 Potato({await command.numtotext(potato)})', callback_data=f'farm_seed_sell potato_seed {reference}') 
   corn_button = types.InlineKeyboardButton(text=f'🌽 Corn({await command.numtotext(corn)})', callback_data=f'farm_seed_sell corn_seed {reference}')  
   carrot_button = types.InlineKeyboardButton(text=f'🥕 Carrot({await command.numtotext(carrot)})', callback_data=f'farm_seed_sell carrot_seed {reference}')    
   broccoli_button = types.InlineKeyboardButton(text=f'🥦 Broccoli({await command.numtotext(broccoli)})', callback_data=f'farm_seed_sell broccoli_seed {reference}')    
   watermelon_button = types.InlineKeyboardButton(text=f'🍉 Watermelon({await command.numtotext(watermelon)})', callback_data=f'farm_seed_sell watermelon_seed {reference}')  
   keyboard.add(potato_button,corn_button,carrot_button)
   keyboard.add(broccoli_button,watermelon_button)
   keyboard.add(all_button)
   keyboard.add(home_button,back_button)
   try:
     await bot.edit_message_text(txt, call.from_user.id, call.message.id, parse_mode="Markdown", reply_markup=keyboard)
   except:
     ...
async def sell_plants_menu(call,reference):
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
   potato = datafind['potato']
   corn = datafind['corn']
   carrot = datafind['carrot']
   broccoli = datafind['broccoli']
   watermelon = datafind['watermelon']
   sell_all = datafind['sell_all']
   potato_price = config.potato
   corn_price = config.corn
   carrot_price = config.carrot
   broccoli_price = config.broccoli
   watermelon_price = config.watermelon
   if sell_all == 1:
     sell_all_msg = "all_ask"
   else:
     sell_all_msg = "all"
   txt = f"""
*Select Plants To Sell*

- Current Coin: *{coin}*

*Price Table*
- 🥔 Potato: {await command.numtotext(potato_price)} || *[{await command.numtotext(datafind['potato'])}]*
- 🌽 Corn: {await command.numtotext(corn_price)} || *[{await command.numtotext(datafind['corn'])}]*
- 🥕 Carrot: {await command.numtotext(carrot_price)} || *[{await command.numtotext(datafind['carrot'])}]*
- 🥦 Broccoli: {await command.numtotext(broccoli_price)} || *[{await command.numtotext(datafind['broccoli'])}]*
- 🍉 Watermelon: {await command.numtotext(watermelon_price)} || *[{await command.numtotext(datafind['watermelon'])}]*

⚠️ Warning: *Click The Item To Sell All*
"""
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text=f'🔙 Back', callback_data=f'farm_shop sell_menu {reference}')
   home_button = types.InlineKeyboardButton(text=f'🏡 Home', callback_data='main_menu')
   potato_button = types.InlineKeyboardButton(text=f'🥔 Potato({await command.numtotext(potato)})', callback_data=f'farm_sell potato {reference}') 
   corn_button = types.InlineKeyboardButton(text=f'🌽 Corn({await command.numtotext(corn)})', callback_data=f'farm_sell corn {reference}')  
   carrot_button = types.InlineKeyboardButton(text=f'🥕 Carrot({await command.numtotext(carrot)})', callback_data=f'farm_sell carrot {reference}')    
   broccoli_button = types.InlineKeyboardButton(text=f'🥦 Broccoli({await command.numtotext(broccoli)})', callback_data=f'farm_sell broccoli {reference}')    
   watermelon_button = types.InlineKeyboardButton(text=f'🍉 Watermelon({await command.numtotext(watermelon)})', callback_data=f'farm_sell watermelon {reference}')  
   sell_all_button = types.InlineKeyboardButton(text=f'Sell All', callback_data=f'farm_sell {sell_all_msg} {reference}')
   keyboard.add(potato_button,corn_button,carrot_button)
   keyboard.add(broccoli_button,watermelon_button)
   keyboard.add(sell_all_button)
   keyboard.add(home_button,back_button)
   try:
     await bot.edit_message_text(txt, call.from_user.id, call.message.id, parse_mode="Markdown", reply_markup=keyboard)
   except:
     ...

async def sell_plants(call,plants_key,reference,edit=True):
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
   plants_name = plants_key.capitalize()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   item_quantity = datafind[plants_key]
   if item_quantity > 0:
     price = getattr(config, f"{plants_name.lower()}")
     total = item_quantity * price
     total_coin = await command.numtotext(coin + total)
     total_text = await command.numtotext(total)
     query = {}
     update = {'$inc': {'coin': total},"$set":{plants_key: 0}}
     await datack.update_one(query, update)
     item_quantity_str = await command.numtotext(item_quantity)
     await bot.answer_callback_query(call.id,text=f"You Have Sold {item_quantity_str} {icons[plants_name.lower()]}  {plants_name}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}",show_alert=True)
     if edit:
       await command.sell_plants_menu(call,reference)
   else:
     await bot.answer_callback_query(call.id, text=f"You Don't Have Any  {icons[plants_name.lower()]} {plants_name} To Sell", show_alert=True)

async def sell_plants_all(call,reference,edit=False):
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
  coin = datafind["coin"]
  potato = datafind['potato']
  corn = datafind['corn']
  carrot = datafind['carrot'] 
  broccoli = datafind['broccoli']
  watermelon = datafind['watermelon']
  total = 0
  text = ""
  items = {
    "Potato": potato,
    "Corn": corn,
    "Carrot": carrot,
    "Broccoli": broccoli,
    "Watermelon": watermelon}
  updated_items = {}
  for item_name, item_quantity in items.items():
     if item_quantity > 0:
       price_var_name = f"{item_name.lower()}"
       item_price = getattr(config, price_var_name)
       total += item_quantity * item_price
       item_str = await command.numtotext(item_quantity)
       text += f"{item_str} {icons[item_name.lower()]} {item_name}\n"
       updated_items[item_name.lower()] = 0
  query = {}
  total_text = await command.numtotext(total)
  total_coin = await command.numtotext(total+coin)
  if total > 0:
    update = {'$inc': {'coin': total},'$set':updated_items}
    await datack.update_one(query, update)
    await bot.answer_callback_query(call.id,text=f"You Have Sold\n{text}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}", show_alert=True)
    await command.sell_plants_menu(call,reference)
  else:
     await bot.answer_callback_query(call.id,text=f"You Sold Nothing", show_alert=True)
     if edit:
      await command.sell_plants_menu(call,reference)

async def sell_seeds(call,seeds_key,quantity,reference,edit=True):
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
   quantity = int(quantity)
   if quantity <= item_quantity:
     price = getattr(config, f"{seeds_name.lower()}s")
     total = quantity * price
     total_coin = await command.numtotext(coin + total)
     total_text = await command.numtotext(total)
     query = {}
     update = {'$inc': {'coin': total,seeds_key: -quantity}}
     await datack.update_one(query, update)
     item_quantity_str = await command.numtotext(quantity)
     name = seeds_name.replace("_"," ")
     await bot.answer_callback_query(call.id,text=f"You Have Sold {item_quantity_str} {icons[seeds_name.lower()]}  {name.title()}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}",show_alert=True)
     if edit:
       await command.sell_seed(call,seeds_key,reference)
   else:
     name = seeds_name.replace("_"," ")
     await bot.answer_callback_query(call.id, text=f"You Don't Have Any  {icons[seeds_name.lower()]} {name.title()} To Sell", show_alert=True)

async def sell_seeds_all_ask(call,reference):
   keyboard = types.InlineKeyboardMarkup()
   sell_button = types.InlineKeyboardButton(text=f'Confirm',callback_data=f'farm_seed sell xall {reference}')
   back_button = types.InlineKeyboardButton(text=f'Back',callback_data=f'farm_shop seeds_sell {reference}')
   txt = "*Are you sure that you want to sell all seeds ?*\n\n*You have the option to modify this confirmation in the settings*"
   keyboard.add(sell_button,back_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def sell_plants_all_ask(call,reference):
   keyboard = types.InlineKeyboardMarkup()
   sell_button = types.InlineKeyboardButton(text=f'Confirm',callback_data=f'farm_sell xall {reference}')
   back_button = types.InlineKeyboardButton(text=f'Back',callback_data=f'farm_shop plants_sell {reference}')
   txt = "*Are you sure that you want to sell all seeds ?*\n\n*You have the option to modify this confirmation in the settings*"
   keyboard.add(sell_button,back_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def sell_seeds_all(call,reference,edit=False):
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
  coin = datafind["coin"]
  potato = datafind['potato_seed']
  corn = datafind['corn_seed']
  carrot = datafind['carrot_seed'] 
  broccoli = datafind['broccoli_seed']
  watermelon = datafind['watermelon_seed']
  total = 0
  text = ""
  items = {
    "Potato_Seed": potato,
    "Corn_Seed": corn,
    "Carrot_Seed": carrot,
    "Broccoli_Seed": broccoli,
    "Watermelon_Seed": watermelon}
  updated_items = {}
  for item_name, item_quantity in items.items():
     if item_quantity > 0:
       price_var_name = f"{item_name.lower()}s"
       item_price = getattr(config, price_var_name)
       total += item_quantity * item_price
       item_str = await command.numtotext(item_quantity)
       text += f'{item_str} {icons[item_name.lower()]} {item_name.replace("_"," ")}\n'
       updated_items[item_name.lower()] = 0
  query = {}
  total_text = await command.numtotext(total)
  total_coin = await command.numtotext(total+coin)
  if total > 0:
    update = {'$inc': {'coin': total},'$set':updated_items}
    await datack.update_one(query, update)
    await bot.answer_callback_query(call.id,text=f"You Have Sold\n{text}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}", show_alert=True)
    await command.sell_seeds_menu(call,reference)
  else:
     await bot.answer_callback_query(call.id,text=f"You Sold Nothing", show_alert=True)
     if edit:
       await command.sell_seeds_menu(call,reference)
async def sell_plants_all(call,reference,edit=False):
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
  coin = datafind["coin"]
  potato = datafind['potato']
  corn = datafind['corn']
  carrot = datafind['carrot'] 
  broccoli = datafind['broccoli']
  watermelon = datafind['watermelon']
  total = 0
  text = ""
  items = {
    "Potato": potato,
    "Corn": corn,
    "Carrot": carrot,
    "Broccoli": broccoli,
    "Watermelon": watermelon}
  updated_items = {}
  for item_name, item_quantity in items.items():
     if item_quantity > 0:
       price_var_name = f"{item_name.lower()}"
       item_price = getattr(config, price_var_name)
       total += item_quantity * item_price
       item_str = await command.numtotext(item_quantity)
       text += f'{item_str} {icons[item_name.lower()]} {item_name.replace("_"," ")}\n'
       updated_items[item_name.lower()] = 0
  query = {}
  total_text = await command.numtotext(total)
  total_coin = await command.numtotext(total+coin)
  if total > 0:
    update = {'$inc': {'coin': total},'$set':updated_items}
    await datack.update_one(query, update)
    await bot.answer_callback_query(call.id,text=f"You Have Sold\n{text}\n{total_text} Coin Add To Your Account\nTotal Coin: {total_coin}", show_alert=True)
    await command.sell_plants_menu(call,reference)
  else:
     await bot.answer_callback_query(call.id,text=f"You Sold Nothing", show_alert=True)
     if edit:
       await command.sell_plants_menu(call,reference)

async def sell_seed(call,seed_name,reference):
   seed_name_old = seed_name
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   coin_text = await command.numtotext(datafind['coin'])
   seed_quantity = datafind[seed_name]
   keyboard = types.InlineKeyboardMarkup(row_width=8)
   seed_price = getattr(config, f"{seed_name.lower()}s")
   if seed_quantity > 8:
     max_sell = seed_quantity
     max_sell_str = str(max_sell)
   else:
     max_sell = 0
     max_sell_str = ""
   seed_name = seed_name.replace("_"," ")
   txt = f"*[{seed_name.title()}]*\n\n- Coin: *{coin_text}*\n- Current {seed_name.title()}: *{seed_quantity}*\n- {seed_name.title()} Price: *{seed_price}*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*Click The Amount Or Use Custom*\n"
   amount_buttons = [types.InlineKeyboardButton(text=str(i), callback_data=f'farm_seed sell {seed_name_old} {i} {reference}') if seed_quantity >= i else types.InlineKeyboardButton(text="", callback_data=f'farm_seed sell {seed_name_old} {i} {reference}') for i in [1,2,3,4,5,6,7,8]]
   buy_1st = types.InlineKeyboardButton(text=f'{max_sell_str}',callback_data=f'farm_seed sell {seed_name_old} {max_sell} {reference}')
   buy_custom = types.InlineKeyboardButton(text='📜 Custom',callback_data=f'farm_seed sell {seed_name_old} custom')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data=f'farm_shop seeds_sell {reference}')
   keyboard.add(*amount_buttons)
   keyboard.add(buy_1st)
   keyboard.add(buy_custom,back_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)

async def seeds_sell_confirm(message,seed_name,ammout):
   seed_name = f"{seed_name}_seed"
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
   item_ammout = datafind[seed_name]
   item_price = getattr(config, f"{seed_name.lower()}s")
   try:
    ammout = int(ammout)
   except Exception as e:
    print(str(e))
    await asyncio.gather(bot.edit_message_text(f"*You need to provide a real amount*",message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message))
    return 0
   total_coin = ammout*item_price
   if item_ammout-ammout >= 0:
     query = {}
     update = {'$inc': {seed_name: -ammout,'coin': total_coin}}
     seed_name = seed_name.replace("_"," ")
     await asyncio.gather(datack.update_one(query, update),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),bot.edit_message_text(f"You Have Sold *{await command.numtotext(ammout)}* {seed_name.title()}\n*{await command.numtotext(total_coin)}* Coin Add To Your Account\nCurrent Coin: *{await command.numtotext(coin+total_coin)}*\nCurrent {seed_name.title()}: *{item_ammout-ammout}*",message.chat.id,message_id,parse_mode="Markdown"),command.send_home_v2(message))
   else:
     more = ammout-item_ammout
     seed_name = seed_name.replace("_"," ")
     await asyncio.gather(bot.edit_message_text(f"You Need More {await command.numtotext(more)} *{seed_name.title()}* To Sell {ammout}  *{seed_name.title()}*",message.chat.id,message_id,parse_mode="Markdown"),bot.delete_message(message.chat.id,message.reply_to_message.id),bot.delete_message(message.chat.id,message.id),command.send_home_v2(message)) 

async def sell_seeds_custom(call,item_name):
  name = item_name.upper()
  txt = f'*[SELL {name.replace("_"," ")}]*\n\n*Enter The Amount You Want To Sell*'
  keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter The Amount")
  await bot.send_message(call.from_user.id,txt,parse_mode="Markdown",reply_markup=keyboard)