import json
import os
import time
import asyncio
import aiofiles
import commands as command

from telebot import types
from datetime import datetime, timedelta

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

async def add_to_claim_list(call):
  filename = f'json_data/claimed_user.json'
  async with aiofiles.open(filename, 'r') as f:
   claimed_user = json.loads(await f.read())
  claimed_user.append(call.from_user.id)
  async with aiofiles.open(filename, 'w') as f:
   await f.write(json.dumps(claimed_user))
async def count_of_claimer():
  filename = f'json_data/claimed_user.json'
  async with aiofiles.open(filename, 'r') as f:
   claimed_user = json.loads(await f.read())
  return len(claimed_user)
async def claim_reward(message):
  user_id = message.from_user.id
  filename_1 = f'json_data/reward.json'
  async with aiofiles.open(filename_1, 'r') as f:
   reward_data = json.loads(await f.read())
  filename_2 = f'json_data/claimed_user.json'
  async with aiofiles.open(filename_2, 'r') as f:
   claimed_user = json.loads(await f.read())
  text = f"""```Rewards
{reward_data['text']}
```"""
  keyboard = types.InlineKeyboardMarkup()
  if user_id not in claimed_user:
   text += "*Click '🎁 Claim' To Claim*"
   text += f"\n*Total Claimed: {await count_of_claimer()}*"
   note = reward_data['note']
   text += f"\n\n*Developer Note:*\n{note}"
   data = reward_data["data"]
   claim_button = types.InlineKeyboardButton(text='🎁 Claim',callback_data='claim_reward')
   keyboard.add(claim_button)
   message = await bot.send_message(message.chat.id, text,parse_mode="Markdown",reply_markup=keyboard)
   await command.update_window_msg(message)
  else:
   text += "*You Have Already Claimed*"
   text += f"\n*Total Claimed: {await count_of_claimer()}*"
   note = reward_data['note']
   text += f"\n\n*Developer Note:*\n{note}"
   claim_button = types.InlineKeyboardButton(text='🎁 Already Claimed',url="https://t.me/MiningArenaChats")
   keyboard.add(claim_button)
   await bot.send_message(message.chat.id, text,parse_mode="Markdown",reply_markup=keyboard)

async def claim_them(call):
   timestamp = int(time.time())
   idx = str(call.from_user.id)
   filename = f'json_data/reward.json'
   async with aiofiles.open(filename, 'r') as f:
     reward_data = json.loads(await f.read())
   data = reward_data["data"]
   reward = reward_data["text"]
   db = client["user"]
   datafind = db[idx]
   query = {}
   await datafind.update_one(query, data)
   await add_to_claim_list(call)
   text = f"""
*You Have Claimed*
```
{reward}
```Thanks For Staying With Us ❤️
   """
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown")
   await command.send_home_v2(call.message)