import time
import asyncio
import commands as command
import admin
import aiofiles
import json
import telebot

from telebot import types
from telebot.types import ForceReply, ReplyKeyboardMarkup
from telebot import formatting as formatx

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def sendmsgtouser_all(call):
   keyboard = types.ForceReply(selective=False,input_field_placeholder="Enter Message")
   await bot.send_message(call.from_user.id,"📨 Send Message", parse_mode="Markdown",reply_markup=keyboard)
async def sendmsgx(message,userid):
  try:
   if message.chat.id == ownerid:
     getid = int(userid)
     print("Hi")
     print(message.text)
     txt = formatx.escape_markdown(message.text)
     print(txt)
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
    e = formatx.escape_markdown(str(e))
    txt = f"Can't Send The Message\nMaybe He Block The Bot\n\n*{e}*"
    await bot.send_message(ownerid,txt,parse_mode="MarkdownV2")
async def sendmsg(message,text):
  try:
    userlist_x = client["user"]
    userlist = await userlist_x.list_collection_names()
    txt = formatx.escape_markdown(text)
    start_time = time.time()
    totaluser = len(userlist)
    send = await bot.send_message(message.chat.id,f"🕒 Sending of the message to {totaluser} users is started!",parse_mode="Markdown")
    progress = await bot.send_message(message.chat.id,f"*Sent: 0 from {totaluser} (0%)\nWaiting: {totaluser}*",parse_mode="Markdown")
    sent = 0
    for item in userlist:
      try:
        user = await bot.get_chat(item)
        sent += 1
        percentage = int(sent/totaluser*100)
        preset = f"*Sent: {sent} from {totaluser} ({percentage}%)\nWaiting: {(totaluser-sent)}*"
        await bot.edit_message_text(preset,message.chat.id,progress.message_id,parse_mode="Markdown")
        try:
         lastpin = user.pinned_message.id
         await bot.unpin_chat_message(item,lastpin)
        except:
          ...
        sendx = await bot.send_message(item,txt,parse_mode="MarkdownV2")
        await bot.pin_chat_message(item,sendx.message_id)
      except telebot.asyncio_helper.ApiTelegramException as e:
        status_code = int(e.result.status)
        e = formatx.escape_markdown(str(e))
        username = user.username
        username = username.replace("_", "\\_")
        await bot.send_message(ownerid,f"*Update For* @{username}\n*{e}*\n*ID:* `{item}`\n/remove",parse_mode='MarkdownV2')
        if status_code == 400:
          break
    end_time = time.time()
    await bot.edit_message_text(f"💥 Sending message to all user is successfully completed!\nIt Took {int((end_time - start_time))} Seconds",message.chat.id,send.message_id,parse_mode="Markdown")
    return await command.send_home_v2(message)
  except telebot.asyncio_helper.ApiTelegramException as e:
    e = formatx.escape_markdown(str(e))
    txt = f"Can't Send The Message\n*{e}*"
    await bot.send_message(ownerid,txt,parse_mode="MarkdownV2")
    return await command.send_home_v2(message)