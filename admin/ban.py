import asyncio
import aiofiles
import json
import commands as command
import admin
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
ownerid = 1794942023
async def ban(message):
  try:
    user_id = message.text.split()[1]
    user_id = int(user_id)
    user = await bot.get_chat(user_id)
    username = user.username
    username = username.replace("_", "\\_")
  except:
    text = f"""
```
User Not Found
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  try:
    admin_txt = message.text.split()[2:]
    admin_text_2 = " ".join(admin_txt)
  except Exception as e:
    text = str(e)
    text = f"""
```
Enter Note Also
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  async with aiofiles.open('json_data/ban.json', 'r') as f:
    userlist = json.loads(await f.read())
  if user_id in [item['id'] for item in userlist]:
    text = f"""
```
The User Is Already Banned
Username @{username}
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
  if user_id not in [item['id'] for item in userlist]:
    userlist.append({'id': user_id})
    try:
      text = f"""
```
The User Is Banned Successfully
Username @{username}
Note:
{admin_text_2}
```
"""
      await bot.reply_to(message, text, parse_mode="Markdown")
    except telebot.asyncio_helper.ApiTelegramException as e:
      e = str(e)
      text = f"""
```
[ERROR]
Error: {e}
Username @{username}
```
"""
      await bot.reply_to(message, text, parse_mode="Markdown")
      return 0
    idx = str(user_id)
    db = client["user"]
    datack = db[idx]
    query = {}
    update = {'$set': {'ban': 1}}
    await datack.update_one(query, update)
    await bot.send_message(user_id, f" - Your account has been banned due to violations\n - Blocking the bot will result in the deletion of all your *Game* Data\n\n - Note From *Administration*\n\n*{admin_text_2}*", parse_mode="Markdown")
    async with aiofiles.open('json_data/ban.json', 'w') as f:
      await f.write(json.dumps(userlist))
