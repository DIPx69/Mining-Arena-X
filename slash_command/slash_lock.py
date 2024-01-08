import os
import random
import commands as command
import slash_command as slash
import json
import aiofiles
import asyncio
from telebot.async_telebot import *
token = os.getenv("token")
bot = AsyncTeleBot(token)

slash_command = {}
pending = {} 

async def check_lock(message):
   global pending
   if str(message.from_user.id) in pending:
     data = pending[str(message.from_user.id)]
     print(data)
     if data["type"] in ["group", "supergroup"]:
       if data['chat_username'] is not None:
         link = f"https://t.me/{data['chat_username']}/{data['id']}"
         message_link = f"[‎ ]({link})"
       else:
         group_id = int(str(data['chat_id']).replace("-100", "", 1))
         link = f"https://t.me/c/{group_id}/{data['id']}"
         message_link = f"\n[Click Here To See]({link})"
     else:
       message_link = "\n\n*Command Was Executed In Bot Inbox*"
     text = f"""

```
Hold Tight 
```*You are unable to interact with this due to an ongoing command or a minor issue
Please finish any open commands*{message_link}
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return True
   else:
     return False
async def print_log(message):
   global slash_command
   print(message.from_user.username)

async def is_commander(call):
   data = call.json
   if call.message.reply_to_message is None:
     await bot.answer_callback_query(call.id, text=f"This menu is expired because of the deletion of the reply message", show_alert=True)
     return True
   if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
     username = data["message"]["reply_to_message"]["from"]["username"]
     await bot.answer_callback_query(call.id, text=f"This menu is controlled by @{username}\nYou will have to run the original command yourself", show_alert=True)
     return True
   else:
     return False
async def unlock(message):
   global slash_command
   del slash_command[str(message.from_user.id)]

async def lock(message):
   global slash_command
   if str(message.from_user.id) not in slash_command:
     slash_command[str(message.from_user.id)] = {"command": message.text}
     print(slash_command)
     return True
   elif str(message.from_user.id) in slash_command:
     await bot.reply_to(message,"*Anti Spam*",parse_mode="Markdown")
     return False
     
async def command_lock(message):
   global pending
   pending[str(message.from_user.id)] = {
     "type": message.chat.type,
     "chat_id": message.chat.id,
     "chat_username": message.chat.username,
     "user_id": message.from_user.id,
     "id": message.id
   }

async def command_unlock(call):
   global pending
   data = call.json
   user_id = data["message"]["reply_to_message"]["from"]["id"]
   del pending[str(user_id)]

async def command_unlock_message(message):
   global pending
   data = message.json
   user_id = data["reply_to_message"]["from"]["id"]
   del pending[str(user_id)]
   
async def command_timeout(message):
   global pending
   data = message.json
   user_id = data["reply_to_message"]["from"]["id"]
   if str(user_id) in pending:
     text_z = message.text
     text = f"""
```
{text_z.replace("Pending Confirmation","Action Timeout")}
```
   """
     await bot.edit_message_text(text,message.chat.id,message.id,parse_mode="Markdown")
     await command_unlock_message(message)
   else:
     print("not found")