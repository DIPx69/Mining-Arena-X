import asyncio
import commands as command
import admin
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def adminmenu(call):
    keyboard = types.InlineKeyboardMarkup()
    list_button = types.InlineKeyboardButton(text='👤 User List',callback_data='user_list')
    message_to_user_button = types.InlineKeyboardButton(text='💌 Message To User',callback_data='message_to_user')
    message_to_all_user_button = types.InlineKeyboardButton(text='📪 Message To All User',callback_data='message_to_all_user')
    ban_list_button = types.InlineKeyboardButton(text='🚫 Ban List',callback_data='ban_list')
    back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
    keyboard.add(list_button)
    keyboard.add(message_to_user_button,message_to_all_user_button)
    keyboard.add(ban_list_button)
    keyboard.add(back_button)
    await bot.edit_message_text("*Select Option*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)