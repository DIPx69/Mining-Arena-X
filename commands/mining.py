import telebot
import asyncio
import os
import config
import dns.resolver
import commands as command
import time
from datetime import datetime, timedelta
from telebot import types
from telebot.async_telebot import *
import motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
async def time_ago(timestamp: int):
   if timestamp < int(time.time()):
     time_ago = int(time.time() - timestamp)
     days = time_ago // (24 * 3600)
     hours = (time_ago % (24 * 3600)) // 3600
     minutes = (time_ago % 3600) // 60
     seconds = time_ago % 60
     if days > 0:
       time_ago = f"{days}d:{hours}h:{minutes}m:{seconds}s"
     elif hours > 0:
       time_ago = f"{hours}h:{minutes}m:{seconds}s"
     elif minutes > 0:
       time_ago = f"{minutes}m:{seconds}s"
     else:
       time_ago = f"{seconds}s"
     return time_ago
async def time_left(timestamp: int):
   if timestamp > int(time.time()):
     time_left = int(timestamp - time.time())
     days = time_left // (24 * 3600)
     hours = (time_left % (24 * 3600)) // 3600
     minutes = (time_left % 3600) // 60
     seconds = time_left % 60
     if days > 0:
       time_left = f"{days}d:{hours}h:{minutes}m:{seconds}s"
     elif hours > 0:
       time_left = f"{hours}h:{minutes}m:{seconds}s"
     elif minutes > 0:
       time_left = f"{minutes}m:{seconds}s"
     else:
       time_left = f"{seconds}s"
   return str(time_left)
async def mine_check(call,datafind):
   keyboard = types.InlineKeyboardMarkup()
   automineon = datafind["automineon"]
   end_time = datafind["end_time"]
   if end_time <= int(time.time()) and automineon == 1:
     end_time_str = await time_ago(end_time)
     txt = f"Your Mining Is Finished {end_time_str} Ago\n\nGo And Claim From   ⛏️ Mining"
     await bot.answer_callback_query(call.id,text=txt,show_alert=True)
async def view_mine(call,name: str):
   name = name.lower() 
   item_name = name.capitalize()
   item_cooldown = getattr(config, f"{name}cooldown") 
   item_minimum_level = getattr(config, f"min{name}lvl") 
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   minexactive = datafind["minexactive"]
   xpboostactive = datafind["xpboostactive"]
   autominelvl = datafind["autominelvl"]
   minex = datafind["minex"]
   xpboost = datafind["xpboost"]
   lvl = datafind["lvl"]
   total_mine = autominelvl*config.mineleft
   end_time = total_mine*item_cooldown
   keyboard = types.InlineKeyboardMarkup()
   minlvl = item_minimum_level
   if lvl >= minlvl:
     if minex <= 0:
       minexactive = 0
     if xpboost <= 0:
       xpboostactive = 0
     if minexactive == 0:
       minex_active = types.InlineKeyboardButton(text=f'MineX[{minex}]', callback_data=f'switch minex {name}')
       minex_status =f"Disabled"
       cooldown = item_cooldown
       now_time = int(time.time())
       end_time_2 = int(end_time + now_time)
     else:
       minex_active = types.InlineKeyboardButton(text=f'・MineX・[{minex}]', callback_data=f'switch minex {name}')
       minex_status =f"Enabled"
       cooldown = item_cooldown/2
       now_time = int(time.time())
       end_time = int(end_time/2)
       end_time_2 = int(end_time + now_time)
     start_button = types.InlineKeyboardButton(text=f'⛏️ START', callback_data=f'start_mine {name}')
     dt = datetime.fromtimestamp(end_time_2)
     dhaka_offset = timedelta(hours=6)  
     dt_dhaka = dt + dhaka_offset
     end_time_str = dt_dhaka.strftime('%I:%M:%S%p')
     if xpboostactive == 0:
       xpboostactive = types.InlineKeyboardButton(text=f'XPBoost[{xpboost}]', callback_data=f'switch xpboost {name}')
       xpboost_status =f"Disabled"
     else:
       xpboostactive = types.InlineKeyboardButton(text=f'・XPBoost・[{xpboost}]', callback_data=f'switch xpboost {name}')
       xpboost_status =f"Enabled"
     end_timer_text = await time_left(end_time_2)
     end_timer_text = f"In *{end_timer_text}*"
     txt = f"*[MINING AREA - {item_name.title()}]*\n\n - Mining Level: *{autominelvl}*\n - Total Mining: *{total_mine}*\n - MineX: *{minex_status}* | Inventory: *{minex}*\n - XPBoost: *{xpboost_status}* | Inventory: *{xpboost}*\n - Cooldown: *{cooldown} Seconds*\n\n - Estimated Ending Time: *{end_time_str}*\n - {end_timer_text}"
     back_button = types.InlineKeyboardButton(text=f'🔙 Back', callback_data='back_mining')
     keyboard.add(minex_active,xpboostactive)
     keyboard.add(start_button)
     keyboard.add(back_button)
     await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
   else:
    await bot.answer_callback_query(call.id,text=f"You Need {minlvl} Level To Access This Area",show_alert= True)

async def start_mine(call,name: str):
   name = name.lower() 
   item_cooldown = getattr(config, f"{name}cooldown") 
   item_minimum_level = getattr(config, f"min{name}lvl") 
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   minexactive = datafind["minexactive"]
   xpboostactive = datafind["xpboostactive"]
   autominelvl = datafind["autominelvl"]
   minex = datafind["minex"]
   xpboost = datafind["xpboost"]
   automineon = datafind["automineon"]
   lvl = datafind["lvl"]
   total_mine = autominelvl*config.mineleft
   end_time = total_mine*item_cooldown
   minlvl = item_minimum_level
   query = {}
   if automineon == 1:
     await bot.answer_callback_query(call.id,text="You Are Already Mining",show_alert= True)
   elif lvl < minlvl:
     await bot.answer_callback_query(call.id,text=f"You Need {minlvl} Level To Access This Area",show_alert= True)
   else:
     if minexactive == 1:
       cooldown = item_cooldown/2
       now_time = int(time.time())
       end_time = int(end_time/2)
       end_time_2 = int(end_time + now_time)
       if minex <= 0:
         minexactive = 0
       else:
         minexactive = 1
     else:
       cooldown = item_cooldown
       now_time = int(time.time())
       end_time_2 = int(end_time + now_time)
     if xpboostactive == 1:
       if xpboost <= 0:
         xpboostactive = 0
       else:
         xpboostactive = 1
     update = {"$set":{"automineon":1,"mining_item": name,"minexactive": minexactive,"xpboostactive": xpboostactive,"end_time": end_time_2,"xpboost_on": xpboostactive,"minex_on": minexactive},"$inc": {"minex": -minexactive,"xpboost": -xpboostactive}}
     await datack.update_one(query,update)
     await command.minemenu(call)
     now_time = int(time.time())
     await command.active_miner_add(call,end_time_2)
     await asyncio.sleep(end_time)
     now_time = int(time.time())
     in_active_miner = await command.active_miner_verify(call,now_time)
     if in_active_miner:
       await command.active_miner_remove(call)
       await command.minefinish(call)
async def switch_minex(call,name):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   minex = datafind["minex"]
   minexactive = datafind["minexactive"]
   query = {}
   if minexactive == 1 and minex > 0:
     update = {"$set":{"minexactive": 0}}
     await datack.update_one(query,update)
   elif minexactive == 0 and minex > 0:
     update = {"$set":{"minexactive": 1}}
     await datack.update_one(query,update)
   elif minex <= 0:
      update = {"$set":{"minexactive": 0}}
      await datack.update_one(query,update)
      await bot.answer_callback_query(call.id, text=f"You Have Don't Have Any MineX", show_alert=True)
   await view_mine(call,name)
async def switch_xpboost(call,name):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   xpboost = datafind["xpboost"]
   xpboostactive = datafind["xpboostactive"]
   query = {}
   if xpboostactive == 1 and xpboost > 0:
     update = {"$set":{"xpboostactive": 0}}
     await datack.update_one(query,update)
   elif xpboostactive == 0 and xpboost > 0:
     update = {"$set":{"xpboostactive": 1}}
     await datack.update_one(query,update)
   elif xpboost <= 0:
      update = {"$set":{"xpboostactive": 0}}
      await datack.update_one(query,update)
      await bot.answer_callback_query(call.id, text=f"You Have Don't Have Any XPBoost", show_alert=True)
   await view_mine(call,name)
async def minemenu(call,message_id: int=0):
  if message_id == 0:
   message_id = call.message.id
  keyboard = types.InlineKeyboardMarkup()
  idx = str(call.from_user.id)
  db = client["user"]
  datack = db[idx]
  datafind = await datack.find_one()
  automineon = datafind["automineon"]
  lvl = datafind["lvl"]
  mining_item = datafind["mining_item"].upper()
  end_time = datafind["end_time"]
  minex_on = datafind["minex_on"]
  xpboost_on = datafind["xpboost_on"]
  back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='main_menu')
  if lvl >= config.mincoallvl:
    coal_sign = "🟢"
  else:
    coal_sign = "🔴"
  if lvl >= config.minsilverlvl:
    silver_sign = "🟢"
  else:
    silver_sign = "🔴"
  if lvl >= config.mincrimsteellvl:
    crimsteel_sign = "🟢"
  else:
    crimsteel_sign = "🔴"
  if lvl >= config.mingoldlvl:
    gold_sign = "🟢"
  else:
    gold_sign = "🔴"
  if lvl >= config.minmythanlvl:
    mythan_sign = "🟢"
  else:
    mythan_sign = "🔴"
  if lvl >= config.minmagiclvl:
    magic_sign = "🟢"
  else:
    magic_sign = "🔴"
  if automineon == 0:
    iron_button = types.InlineKeyboardButton(text='🟢 Iron', callback_data='view_mine iron')
    coal_button = types.InlineKeyboardButton(text=f'{coal_sign} Coal', callback_data='view_mine coal')
    silver_button = types.InlineKeyboardButton(text=f'{silver_sign} Silver', callback_data='view_mine silver')
    crimsteel_button = types.InlineKeyboardButton(text=f'{crimsteel_sign} Crimsteel', callback_data='view_mine crimsteel')
    gold_button = types.InlineKeyboardButton(text=f'{gold_sign} Gold', callback_data='view_mine gold')
    mythan_button = types.InlineKeyboardButton(text=f'{mythan_sign} Mythan', callback_data='view_mine mythan')
    magic_button = types.InlineKeyboardButton(text=f'{magic_sign} Magic', callback_data='view_mine magic')
    keyboard.add(iron_button,coal_button,silver_button)
    keyboard.add(crimsteel_button)
    keyboard.add(gold_button,mythan_button,magic_button)
    keyboard.add(back_button)
    txt = "*Select A Mining Area*\n*Accessible Area With 🟢 Sign*"
  else:
   if minex_on == 0:
     minex_status = "Disabled"
   else:
     minex_status = "Enabled"
   if xpboost_on == 0:
     xpboost_status = "Disabled"
   else:
     xpboost_status = "Enabled"
   if end_time < int(time.time()):
     end_timer_text = await time_ago(end_time)
     end_timer_text = f"Finished *{end_timer_text}* ago"
     claim_button = types.InlineKeyboardButton(text='🎁 Claim', callback_data='claim_mine')
     keyboard.add(claim_button)
     keyboard.add(back_button)
   else:
    end_timer_text = await time_left(end_time)
    end_timer_text = f"In *{end_timer_text}*"
    refresh_button = types.InlineKeyboardButton(text='🔃 Refresh', callback_data='refresh_mining')
    cancel_button = types.InlineKeyboardButton(text=f'Cancel Mining', callback_data='cancel_ask')
    keyboard.add(refresh_button,cancel_button)
    keyboard.add(back_button)
   dt = datetime.fromtimestamp(end_time)
   dhaka_offset = timedelta(hours=6)  
   dt_dhaka = dt + dhaka_offset
   end_time_str = dt_dhaka.strftime('%I:%M:%S%p')
   txt=f"*[MINING PROGRESS - {mining_item}]*\n\n - Estimated Ending Time: *{end_time_str}*\n - {end_timer_text}\n - MineX: *{minex_status}*\n - XPBoost: *{xpboost_status}*\n"
  await bot.edit_message_text(txt,call.from_user.id,message_id,parse_mode="Markdown",reply_markup=keyboard)
# Cancel Mining Ask
async def cancel_mine_ask(call):
   keyboard = types.InlineKeyboardMarkup()
   text = "*Are You Sure ?*\n\nNote: *Please be informed that once an item is used during a mining operation, it is non refundable*"
   yes_button = types.InlineKeyboardButton(text=f'Yes', callback_data='cancel_mine')
   no_button = types.InlineKeyboardButton(text=f'No', callback_data='mine')
   keyboard.add(yes_button,no_button)
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
# Cancel Mining Button
async def cancel_mine(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   query = {}
   update = {"$set":{"automineon":0,"minex_on":0,"xpboost_on":0}}
   await datack.update_one(query,update)
# Claim Mining Menu
async def claim_mine(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   level = datafind["lvl"]
   minexactive = datafind["minexactive"]
   xpboostactive = datafind["xpboostactive"]
   autominelvl = datafind["autominelvl"]
   automineon = datafind["automineon"]
   xpmulti = datafind['xpmulti']
   itemmulti = datafind['itemmulti']
   lvlnoti = datafind['lvlnoti']
   mining_item = datafind["mining_item"].lower()
   end_time = datafind["end_time"]
   now_time = int(time.time())
   total_mine = autominelvl*config.mineleft
   query = {}
   if automineon == 0 and end_time <= now_time:
     await bot.answer_callback_query(call.id, text=f"You Are Currently Not Mining", show_alert=True)
   else:
     totalamm = 0
     totalxp = 0
     for i in range(1,total_mine+1):
       maxamm = random.randint(1, config.maxiron)
       totalamm += maxamm
       maxxp = random.randint(1, config.maxironxp)
       totalxp += maxxp
     totalamm = int(totalamm*itemmulti)
     totalxp = int(totalxp*xpmulti)
     if xpboostactive == 1:
       totalxp = totalxp*2
       xpboost_on_1 = "[2x]"
     else:
       totalxp = totalxp
       xpboost_on_1 = ""
     update = {"$set":{"automineon":0,"minex_on":0,"xpboost_on":0},"$inc": {mining_item: totalamm,"xp": totalxp,"mymine": total_mine}}
     await datack.update_one(query,update)
     i = 2
     totalup = 0
     start = time.time()
     while i > 0:
      totalxp = totalxp
      datafind = await datack.find_one()
      lvl = datafind['lvl']
      xp = datafind['xp']
      nxtlvlxp = datafind['nxtlvlxp']
      addxp = xp - totalxp
      if addxp < 0:
       extra_xp = totalxp + addxp
      else:
       extra_xp = totalxp
      if xp >= nxtlvlxp:
       totalup += 1
       extra = xp-nxtlvlxp
       update = {"$inc": {"lvl": 1,"nxtlvlxp":50},"$set": {"xp": extra}}
       await datack.update_one(query, update)
       if lvlnoti == 1:
         await bot.send_message(call.from_user.id,f"You Have Level Up To {totalup}")
      else:
       i = 0
     print(time.time()-start)
     restart_button = types.InlineKeyboardButton(text=f'🔃 Restart', callback_data='back_mining')
     sell_button = types.InlineKeyboardButton(text=f'SELL {mining_item.upper()}', callback_data=f'sell no_edit {mining_item}')
     back_button = types.InlineKeyboardButton(text=f'🔙 Back',callback_data='main_menu')
     keyboard.add(restart_button,sell_button)
     keyboard.add(back_button)
     txt = f"*[MINING FINISHED]*\n\n - Mined *{totalamm}* {mining_item.upper()} *[{itemmulti}x]*\n - Level Up *{totalup}* Times *{xpboost_on_1}**[{xpmulti}x]*\n - Add Extra *{extra_xp}* XP\n - Add *{total_mine}* Mine" 
     await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def level_adjust(call):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   maximum_automine_lvl = datafind["maximum_automine_lvl"]
   automineon = datafind["automineon"]
   if automineon == 1:
     await bot.answer_callback_query(call.id,text="You Can't Auto Adjust While Mining",show_alert=True)
     return 0
   else:
     query = {}
     update = {"$set":{"autominelvl": maximum_automine_lvl}}
     await datack.update_one(query,update)
async def upgrade_menu(call):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   await command.mine_check(call,datafind)
   coin = datafind["coin"]
   coin_text = await command.numtotext(datafind["coin"])
   coin_text = coin_text.replace(".","\.")
   coin_text = coin_text.replace("-","\-")
   autominelvl = datafind["autominelvl"]
   maximum_automine_lvl = datafind["maximum_automine_lvl"]
   automineon = datafind["automineon"]
   cost = maximum_automine_lvl*config.autotripprice
   cost_text = await command.numtotext(cost)
   cost_text = cost_text.replace(".","\.")
   keyboard = types.InlineKeyboardMarkup()
   pickaxe_level_req = [config.iron_pickaxe_name,f'||{config.coal_pickaxe_name}|| In {config.mincoallvl} Level',f'||{config.silver_pickaxe_name}|| In {config.minsilverlvl} Level',f'||{config.crimsteel_pickaxe_name}|| In {config.mincrimsteellvl} Level',f'||{config.gold_pickaxe_name}|| In {config.mingoldlvl} Level',f'||{config.mythan_pickaxe_name}|| In {config.minmythanlvl} Level',f'||{config.magic_pickaxe_name}|| In {config.minmagiclvl} Level','||Ultimate Pickaxe|| In 75 Level']
   pickaxe_list = [config.iron_pickaxe_name,config.coal_pickaxe_name,config.silver_pickaxe_name,config.crimsteel_pickaxe_name,config.gold_pickaxe_name,config.mythan_pickaxe_name,config.magic_pickaxe_name,'Ultimate Pickaxe']
   current_pickaxe = pickaxe_list[0]
   next_pickaxe = pickaxe_level_req[1]
   if maximum_automine_lvl >= config.mincoallvl:
     current_pickaxe = pickaxe_list[1]
     next_pickaxe = pickaxe_level_req[2]
   if maximum_automine_lvl >= config.minsilverlvl:
     current_pickaxe = pickaxe_list[2]
     next_pickaxe = pickaxe_level_req[3]
   if maximum_automine_lvl >= config.mincrimsteellvl:
     current_pickaxe = pickaxe_list[3]
     next_pickaxe = pickaxe_level_req[4]
   if maximum_automine_lvl >= config.mingoldlvl:
     current_pickaxe = pickaxe_list[4]
     next_pickaxe = pickaxe_level_req[5]
   if maximum_automine_lvl >= config.minmythanlvl:
     current_pickaxe = pickaxe_list[5]
     next_pickaxe = pickaxe_level_req[6]
   if maximum_automine_lvl >= config.minmagiclvl:
     current_pickaxe = pickaxe_list[6]
     next_pickaxe = pickaxe_level_req[7]
   if maximum_automine_lvl >= 75:
     current_pickaxe = pickaxe_list[7]
     next_pickaxe = "MAXED"
   home_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='main_menu')
   upgrade = types.InlineKeyboardButton(text='⬆️ Upgrade',callback_data='upgrade_automine')
   if autominelvl < maximum_automine_lvl:
     level_adjust_text = "Auto Adjust"
   else:
     level_adjust_text = ""
   if cost <= coin:
     max_text = "💥 MAX 💥"
   else:
     max_text = ""
   max_upgrade = types.InlineKeyboardButton(text=f'{max_text}',callback_data='max')
   level_adjust = types.InlineKeyboardButton(text=f'{level_adjust_text}',callback_data='level_adjust')
   adjustable_lvl = types.InlineKeyboardButton(text=f'Adjust Level',callback_data='adjust 1')
   keyboard.add(max_upgrade,adjustable_lvl,level_adjust)
   keyboard.add(upgrade,home_button)
   txt = f"*\[Pickaxe Upgrade\]*\n \- Current Coin: *{coin_text}*\n\n \- Current Pickaxe: *{current_pickaxe}*\n \- Current Level: *{autominelvl}*\n \- Maximum Level: *{maximum_automine_lvl}*\n \- Next Pickaxe: *{next_pickaxe}*\n\n \- Upgrade Cost: *{cost_text}*\n"
   try:
     await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdownv2",reply_markup=keyboard)
   except:
      ...
async def max_upgrade(call):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   autominelvl = datafind["maximum_automine_lvl"]
   autominelvl_past = datafind["autominelvl"]
   cost = autominelvl*config.autotripprice
   automineon = datafind["automineon"]
   prestige = datafind["prestige"]
   maximum_level = config.max_pickaxe_level+(prestige*config.extra_level_for_prestige)
   total_up = 0
   total_cost = 0
   if automineon == 1:
    await bot.answer_callback_query(call.id,text="You Can't Upgrade While Mining",show_alert=True)
    return False
   if autominelvl >= maximum_level:
     notification = f"Maximum Upgradeable Pickaxe Level Is {maximum_level}\nYou Can Increase It By 50 Through Each Prestige"
     await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     return False
   while coin >= cost and autominelvl < maximum_level:
     total_up += 1
     autominelvl += 1
     cost = autominelvl*config.autotripprice
     coin -= cost
     total_cost += cost
   total_cost_text = await command.numtotext(total_cost)
   notification = f"Pickaxe Max Upgradation Complete\n\nTotal Level Up: {total_up}\nTotal Cost: {total_cost_text}"
   query = {}
   update = {"$inc":{"coin": -total_cost,"maximum_automine_lvl": +total_up},"$set":{"autominelvl": autominelvl}}
   await datack.update_one(query,update)
   await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
   return True
async def upgrade_automine(call):
  idx = str(call.from_user.id)
  db = client["user"]
  datack = db[idx]
  datafind = await datack.find_one()
  coin = datafind["coin"]
  autominelvl = datafind["maximum_automine_lvl"]
  autominelvl_past = datafind["autominelvl"]
  automineon = datafind["automineon"]
  prestige = datafind["prestige"]
  maximum_level = config.max_pickaxe_level+(prestige*config.extra_level_for_prestige)
  cost = autominelvl*config.autotripprice
  pickaxe_list = [config.iron_pickaxe_name,config.coal_pickaxe_name,config.silver_pickaxe_name,config.crimsteel_pickaxe_name,config.gold_pickaxe_name,config.mythan_pickaxe_name,config.magic_pickaxe_name,'Ultimate Pickaxe']
  if cost <= coin and automineon == 0 and autominelvl < maximum_level:
     notification = ""
     if autominelvl == config.mincoallvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[1]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == config.minsilverlvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[2]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == config.mincrimsteellvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[3]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == config.mingoldlvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[4]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == config.minmythanlvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[5]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == config.minmagiclvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[6]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == config.minmagiclvl-1:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[6]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     if autominelvl == 74:
       notification = f"\nYour Pickaxe Upgraded To {pickaxe_list[7]}"
       await bot.answer_callback_query(call.id, text=f"{notification}", show_alert=True)
     query = {}
     update = {
  "$inc": {
    "coin": -cost,
    "maximum_automine_lvl": +1
  },
  "$set": {
    "autominelvl": autominelvl+1
  }
}
     await datack.update_one(query,update)
     autominelvl += 1
     cost = autominelvl*config.autotripprice
     return True
  elif autominelvl >= maximum_level:
    await bot.answer_callback_query(call.id,text=f"Maximum Upgradeable Pickaxe Level Is {maximum_level}\nYou Can Increase It By 50 Through Each Prestige",show_alert=True)
    return False
  elif automineon == 1:
    await bot.answer_callback_query(call.id,text="You Can't Upgrade While Mining",show_alert=True)
    return False
  elif cost > coin:
    await bot.answer_callback_query(call.id, text="You Don't Have Enough Coin", show_alert=True)
    return False