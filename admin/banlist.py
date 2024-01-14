import asyncio
import aiofiles
import json
import commands as command
import admin
from telebot import types
import time

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def banlist(call):
  keyboard = types.InlineKeyboardMarkup()
  back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='admin_panel')
  keyboard.add(back_button)
  await bot.edit_message_text("Generating User List",call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)
  async with aiofiles.open('json_data/ban.json', 'r') as f:
    userlist = json.loads(await f.read())
  start = time.time()
  all_user = "*BANNED USER LIST*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
  for item in userlist:
    user_id = item['id']     
    chat = await bot.get_chat(user_id)
    username = chat.username
    if username:
     username = username.replace("_", "\\_")
     all_user += f"`{user_id}` : @{username}\n"
    else:
     all_user += f"`{user_id}` : No username"
  end = time.time()
  totaltime = int(end-start)
  all_user += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\nIt Took *{totaltime}* Second To Make This User List"
  await bot.edit_message_text(all_user,call.from_user.id,call.message.id, parse_mode="MarkdownV2",reply_markup=keyboard)