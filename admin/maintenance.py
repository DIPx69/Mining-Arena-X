import asyncio
import aiofiles
import json
import commands as command

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def set_text(message):
  async with aiofiles.open('json_data/maintenance.json', 'r') as f:
    maintenance_info = json.loads(await f.read()) 
  try:
   reason_text = message.text.split()[1:]
   reason_text_2 = " ".join(reason_text)
  except:
   await bot.send_message(message.chat.id,f"Enter Set Text",parse_mode="Markdown")
   return 0
  maintenance_info["reason"] = reason_text_2
  await bot.send_message(message.chat.id,f"Bot Maintenance Mode Reason: {reason_text_2}",parse_mode="Markdown")
  async with aiofiles.open('json_data/maintenance.json', 'w') as f:
     await f.write(json.dumps(maintenance_info))
async def maintenance(message):
  async with aiofiles.open('json_data/maintenance.json', 'r') as f:
   maintenance_info = json.loads(await f.read())
  try:
   status_get = message.text.split()[1]
   status_2 = status_get.lower()
   bool_mapping = {"true": True, "false": False}
   status_3 = bool_mapping.get(status_2, False)  
  except:
     status = maintenance_info["status"]
     reason = maintenance_info["reason"]
     await bot.send_message(message.chat.id,f"*[MAINTENANCE MODE]*\nMode: *{status}*\nReason: *{reason}*\nUse /set To Change To Reason Text",parse_mode="Markdown")
     return 0
  try:
   reason_text = message.text.split()[2:]
   reason_text_2 = " ".join(reason_text)
  except:
   await bot.send_message(message.chat.id,f"Enter Note Also",parse_mode="Markdown")
   return 0
  if maintenance_info["status"] == status_3:
   await bot.send_message(message.chat.id,f"Maintenance Mode Is Already *{status_3}*",parse_mode="Markdown")
  else:
    maintenance_info = {"status": status_3,'reason': reason_text_2}
    await bot.send_message(message.chat.id,f"Bot Maintenance Mode Is Now {status_3}\nReason: {reason_text_2}",parse_mode="Markdown")
    async with aiofiles.open('json_data/maintenance.json', 'w') as f:
      await f.write(json.dumps(maintenance_info))