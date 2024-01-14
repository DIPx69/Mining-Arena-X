import commands as command

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
async def title_admin(message):
  try:
   cmd = message.text.split()[1]
  except:
   await bot.send_message(message.chat.id,f"Enter Command list or add or remove",parse_mode="Markdown")
   return 0
  if message.text.split()[1] == "list":
    try:
     cmd = message.text.split()[2]
     getid = str(cmd)
     db = client["user"]
     datack = db[getid]
     datafind = await datack.find_one()
     user = await bot.get_chat(getid)
     username = user.username
     username = username.replace("_", "\\_")
     title_list = datafind["title_list"]
     text = '\n'.join([f"* - [{index+1}]* {title}" for index, title in enumerate(title_list)])
     await bot.send_message(message.chat.id,f"Title List Of @{username}\n{text}",parse_mode="Markdown")
    except:
     await bot.send_message(message.chat.id,f"Enter Account Id",parse_mode="Markdown")
     return 0
  if message.text.split()[1] == "add":
    try:
     cmd = message.text.split()[2]
    except:
     await bot.send_message(message.chat.id,f"Enter Account Id",parse_mode="Markdown")
     return 0
    try:
     title_name_x = message.text.split()[3:]
     title_name = " ".join(title_name_x)
    except:
     await bot.send_message(message.chat.id,f"Enter Title Name",parse_mode="Markdown")
     return 0
    query = {}
    getid = str(cmd)
    db = client["user"]
    datack = db[getid]
    datafind = await datack.find_one()
    title_list = datafind["title_list"]
    user = await bot.get_chat(getid)
    username = user.username
    username = username.replace("_", "\\_")
    if title_name in title_list:
      await bot.send_message(message.chat.id,f"@{username} Have Already Have {title_name} Title",parse_mode="Markdown")
    else:
     update_operation = {"$push": {"title_list": {"$each": [f'{title_name}']}}}
     datack.update_one(query, update_operation)
     await bot.send_message(message.chat.id,f"{title_name} Title Has Been Sent To @{username}",parse_mode="Markdown")
  if message.text.split()[1] == "remove":
    try:
     cmd = message.text.split()[2]
    except:
     await bot.send_message(message.chat.id,f"Enter Account Id",parse_mode="Markdown")
     return 0
    try:
     index_name = message.text.split()[3]
    except:
     await bot.send_message(message.chat.id,f"Enter Title Index Number",parse_mode="Markdown")
     return 0
    query = {}
    getid = str(cmd)
    db = client["user"]
    datack = db[getid]
    datafind = await datack.find_one()
    title_list = datafind["title_list"]
    user = await bot.get_chat(getid)
    username = user.username
    username = username.replace("_", "\\_")
    if int(index_name) > len(title_list):
      await bot.send_message(message.chat.id,f"Enter Valid Title Index Number\nMax Index {len(title_list)}",parse_mode="Markdown")
    else:
     title_name = title_list[int(index_name)-1]
     update_operation = {"$pull": {"title_list": {"$eq": f"{title_name}"}}}
     await datack.update_one(query, update_operation)
     await bot.send_message(message.chat.id,f"{title_name} Has Been Removed From @{username} Title List",parse_mode="Markdown")
async def title_add(message):
   idx = str(message.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   querry = {}
   update_operation = {"$push": {"title_list": {"$each": ['Noob']}}}
   datack.update_one(querry, update_operation)
async def set_title(call,index):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   title_list = datafind["title_list"]
   index_value = int(index)
   get_title = title_list[index_value]
   update_operation = {"$set": {"active_title":get_title}}
   querry = {}
   await datack.update_one(querry, update_operation)
   await title(call)
async def switch_title(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   title_list = datafind["title_list"]
   active_title = datafind["active_title"]
   for index, title in enumerate(title_list):
     title_button = types.InlineKeyboardButton(text=f'[{index+1}] {title_list[index]}',callback_data=f'set {index}')
     keyboard.add(title_button)
   text = '\n'.join([f"* - [{index+1}]* {title}" for index, title in enumerate(title_list)])
   main_text = f"*Available Titles*\nCurrent Active Title: *{active_title}*\n\n{text}\n"
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='title')
   keyboard.add(back_button)
   await bot.edit_message_text(main_text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def switch_title_page(call,page_number):
   print("Line 1")
   get_page_number = int(page_number)
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   title_list = datafind["title_list"]
   title_list_2 = datafind["title_list"]
   active_title = datafind["active_title"]
   title_data = {}
   for page_num, start_index in enumerate(range(0, len(title_list), 6), start=1):
      page = title_list[start_index:start_index + 6]
      json_data = {str(page_num):page}
      title_data[str(page_num)] = page
   total_page = len(title_data)
   title_list = title_data[str(get_page_number)] 
   row_buttons = []
   for i in range(0,len(title_list)):
    title_button = types.InlineKeyboardButton(text=f'[{i+1}] {title_list[i]}',callback_data=f'set {i}')
    row_buttons.append(title_button)
   keyboard.add(*row_buttons)
   text = '\n'.join([f"* - [{title_list_2.index(title)+1}]* {title}" for index, title in enumerate(title_list)])
   main_text = f"*Available Titles*\nCurrent Active Title: *{active_title}*\n\n{text}\n\nPage *{get_page_number}* Of *{total_page}*"
   if get_page_number != total_page:
     next_emoji = "⏭️"
   else:
     next_emoji = ""
   if get_page_number != 1:
     prev_emoji = "⏮️"
   else:
     prev_emoji = ""
   next_button = types.InlineKeyboardButton(text=f'{next_emoji}',callback_data=f'title_switch {get_page_number+1}')
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='title')
   prev_button = types.InlineKeyboardButton(text=f'{prev_emoji}',callback_data=f'title_switch {get_page_number-1}')
   keyboard.add(prev_button,next_button)
   keyboard.add(back_button)
   await bot.edit_message_text(main_text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def title(call):
   keyboard = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='profile')
   switch_button = types.InlineKeyboardButton(text='🔄 Switch Title',callback_data='title_switch 1')
   keyboard.add(switch_button,back_button)
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   title_list = datafind["title_list"]
   active_title = datafind["active_title"]
   text = '\n'.join([f"* - [{index+1}]* {title}" for index, title in enumerate(title_list)])
   main_text = f"*Available Titles*\nCurrent Active Title: *{active_title}*\n\n{text}\n"
   await bot.edit_message_text(main_text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)