import commands as command
from telebot import types 

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def settingmenu(call):
   keyboard = types.InlineKeyboardMarkup()
   shop_settings = types.InlineKeyboardButton(text='⚙️ Shop Settings', callback_data='xsettings shop')
   close_button = types.InlineKeyboardButton(text='🚪 Close This Window', callback_data='xsettings close')
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='main_menu')
   keyboard.add(shop_settings)
   keyboard.add(close_button)
   keyboard.add(back_button)
   txt = '*Select Option*'
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def settigs_shop(call):
   keyboard = types.InlineKeyboardMarkup()
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   sell_all = datafind['sell_all']
   if sell_all == 1:
     sell_all = "ON"
     sell_all_change = "OFF"
   else:
     sell_all = "OFF"
     sell_all_change = "ON"
   txt = '*[SHOP SETTINGS]*\n\n'
   txt += f"- Sell All Confirmation: *{sell_all}*"
   change_button = types.InlineKeyboardButton(text=sell_all_change, callback_data='xsettings change sell_all')
   back_button = types.InlineKeyboardButton(text='🔙 Back', callback_data='xsettings main')
   keyboard.add(change_button,back_button)
   await bot.edit_message_text(txt,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
async def switch(call,key):
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   key_name = key
   key = datafind[key]
   if key == 1:
    update_key = 0
   else:
    update_key = 1
   query = {}
   update = {'$set':{key_name: update_key}} 
   await datack.update_one(query,update)
async def close(call):
   await bot.answer_callback_query(call.id,text=f"Read More From Changelog\n\nYou can initiate the `/start` command as many times as you like, but only the most recent one will be effective.", show_alert=True)