import json
import aiofiles

import commands as command
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

async def active_miner_add(call,times):
  filename = f'json_data/active_miner.json'
  async with aiofiles.open(filename, 'r') as f:
   active_miner = json.loads(await f.read())
  active_miner[str(call.from_user.id)] = {"time":times}
  async with aiofiles.open(filename, 'w') as f:
   await f.write(json.dumps(active_miner))
async def active_miner_remove(call):
  filename = f'json_data/active_miner.json'
  async with aiofiles.open(filename, 'r') as f:
   active_miner = json.loads(await f.read())
  del active_miner[str(call.from_user.id)]
  async with aiofiles.open(filename, 'w') as f:
   await f.write(json.dumps(active_miner))
async def active_miner_verify(call,thistime):
  filename = f'json_data/active_miner.json'
  async with aiofiles.open(filename, 'r') as f:
   active_miner = json.loads(await f.read())
  if str(call.from_user.id) in active_miner:
    times = active_miner[str(call.from_user.id)]["time"]
    if times in (thistime, thistime - 1, thistime - 2):
      return True
    else:
      return False
  else:
    return False
# Command Duplication Verify 
async def command_verify(call):
   user_id = int(call.from_user.id)
   message_id = int(call.message.message_id)
   filename = f'json_data/active_window.json'
   async with aiofiles.open(filename, 'r') as f:
     window = json.loads(await f.read())
   print(window)
   if window[str(user_id)]["message_id"] != message_id:
     message_text = "Oops! Running the same command again? Only the latest one works. Please use the newest command. Thank you!"
     await bot.answer_callback_query(call.id,text=f"Command Duplication\n\n{message_text}", show_alert=True)
     return 0
async def update_window(call):
    filename = f'json_data/active_window.json'
    async with aiofiles.open(filename, 'r') as f:
       userwindow = json.loads(await f.read())
    userwindow[str(call.from_user.id)] = {
     "userid": call.from_user.id,
     "message_id": call.message.message_id,
     "name": call.from_user.username
       }
    async with aiofiles.open(filename, 'w') as f:
        await f.write(json.dumps(userwindow))
async def update_window_msg(message):
    filename = f'json_data/active_window.json'
    async with aiofiles.open(filename, 'r') as f:
     userwindow = json.loads(await f.read())
    userwindow[str(message.chat.id)] = {
            "userid": message.chat.id,
            "message_id": message.id,
            "name": message.chat.username
        }
    async with aiofiles.open(filename, 'w') as f:
       await f.write(json.dumps(userwindow))
async def removeid(call):
    user_id = int(call.from_user.id)
    filename = f'json_data/active_window.json'
    async with aiofiles.open(filename, 'r') as f:
       window = json.loads(await f.read())
    try:
     if str(user_id) in window:
        window.remove(str(user_id))
    except:
      ...
    async with aiofiles.open(filename, 'w') as f:
       await f.write(json.dumps(window))