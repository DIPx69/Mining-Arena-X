import time
import asyncio
import commands as command
import admin
import aiofiles
import json

from telebot import types
from telebot.types import ForceReply, ReplyKeyboardMarkup
from telebot import formatting as formatx

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def sendmsgtouser(call):
   keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter Account ID")
   await bot.send_message(call.from_user.id,"⚠️ Send Your Target Id", parse_mode="Markdown",reply_markup=keyboard)
async def saveid(message):
  getid = message.text
  if getid.isdigit():
    getid = int(message.text)
    filename = 'json_data/sendid.json'
    try:
     user = await bot.get_chat(getid)
     username = user.username
     username = username.replace("_", "\\_")
    except:
      await bot.send_message(message.chat.id,f'User Not Found', parse_mode="Markdown")
      return await sendmsgtouser(message)
    async with aiofiles.open(filename, 'r') as f:
      json_data = await f.read()
      datax = json.loads(json_data)
      datax['id'] = getid
      updated_json_data = json.dumps(datax)
    async with aiofiles.open(filename, 'w') as f:
      await f.write(updated_json_data)
    keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter Message")
    await bot.send_message(message.chat.id,f'💌 Send Me Message\nMessage Will Be Sent To @{username}', parse_mode="Markdown",reply_markup=keyboard)
  else:
   await sendmsgtouser(message)
async def sendmsg_user(message):
  try:
   if message.chat.id == ownerid:
     filename = 'json_data/sendid.json'
     async with aiofiles.open(filename, 'r') as f:
      json_data = await f.read()
      datax = json.loads(json_data)
      getid = datax['id']
     text = message.text
     txt = formatx.escape_markdown(text)
     user = await bot.get_chat(getid)
     username = user.username
     username = username.replace("_", "\\_")
     try:
       lastpin = user.pinned_message.id
       await bot.unpin_chat_message(getid,lastpin)
     except:
        ...
     sendx = await bot.send_message(getid,txt,parse_mode="MarkdownV2")
     await bot.pin_chat_message(getid,sendx.message_id)
     txt += "\n\n*Preview Message*"
     await bot.send_message(message.chat.id,txt,parse_mode="MarkdownV2")
     await bot.send_message(message.chat.id,f"Message Has Been Sent To @{username}",parse_mode="Markdown")
  except telebot.asyncio_helper.ApiTelegramException as e:
    e = str(e)
    e = formatx.escape_markdown(e)
    txt = f"Can't Send The Message\nMaybe He Block The Bot\n\n*{e}*"
    await bot.send_message(ownerid,txt,parse_mode="MarkdownV2")
  return await command.send_home_v2(message)