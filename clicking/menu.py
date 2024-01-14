import random
import commands as command

from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def main_menu(call):
   keyboard = types.InlineKeyboardMarkup()
   click_button = types.InlineKeyboardButton(text='☝🏻 Click',callback_data='clicking click')
   shop_button = types.InlineKeyboardButton(text='🏪 Shop',callback_data='clicking shop')
   menu_button = types.InlineKeyboardButton(text='✳️ Menu',callback_data='clicking menu')
   back_button = types.InlineKeyboardButton(text='Back',callback_data='main_menu')
   keyboard.add(click_button,shop_button,menu_button)
   keyboard.add(back_button)
   await bot.edit_message_text("*Select Option*",call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)