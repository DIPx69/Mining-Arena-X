from commands.set_up import bot
from commands.set_up import client
import config
import random
import commands as command
import slash_command as slash
from telebot import types
import asyncio
import time

import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

async def random_sentence():
  verbs = ["stole", "grabbed", "snagged", "acquired", "swiped", "procured"]
  adjectives = ["a fairly decent", "a sizable", "a substantial", "a good", "an impressive", "a hefty"]
  objects = ["chunk", "portion", "pile", "bundle", "stack", "load"]
  actions = ["with finesse", "effortlessly", "in style", "slyly", "without a trace", "smoothly"]
  random_sentence = f"💰 You {random.choice(verbs)} {random.choice(adjectives)} {random.choice(objects)} {random.choice(actions)}!"
  return random_sentence
async def send_notification(message,victim_id,text):
   print(victim_id)
   await bot.send_message(victim_id,text,parse_mode="Markdown") 
async def caught_random_sentence():
  caught_messages = [
    "You were caught! HAHAHA",
    "Oops, you got caught!",
    "Caught in the act! Better luck next time!",
    "Haha, you've been caught!",
    "Nice try, but you were caught!",
    "Caught red-handed! HAHAHA",
    "Foiled again! You were caught!",
    "No escaping this time, you're caught!",
    "Caught like a pro! Or not.",
    "Guess what? You were caught!",
    "Caught in the web of consequences! HAHAHA",
    "Caught with your hand in the cookie jar!",
    "Caught and exposed! Better cover your tracks next time.",
    "Caught off guard! The element of surprise worked.",
    "You're in the spotlight now—caught in the act!",
    "Caught in the maze of repercussions! HAHAHA",
    "Caught in the crossfire of consequences!",
]

  return random.choice(caught_messages)

async def rob_alert_success(message,amount):
   text = f"""
```
@{message.from_user.id} Robbed You
You Lost:
{await command.numtotext(amount)}
```
"""
   await bot.reply_to(message, text, parse_mode="Markdown")

async def rob(message):
  status = await slash.check_lock(message)
  if status is True:
     return False
  get_commands = message.text.split()
  try:
     if int(len(get_commands)) > 1:
       args = message.text.split()[1]
       if args.startswith("@"):
         uid = await command.find_uid(args)
         if uid:
           getid = uid
           getidx = str(uid)
         else:
           raise ValueError("User Not Found In Database")
       elif args.isdigit():
         getid = int(message.text.split()[1])
         getidx = str(message.text.split()[1])
       else:  
         raise ValueError("User Not Found In Database") 
     else:
       raise ValueError("Kindly Mention User To Rob")
  except Exception as e:     
     print(str(e))
     text = f"""
```
{str(e)}
``````
/rob @DipDey
```
"""
     await bot.reply_to(message, text, parse_mode="Markdown")
     return
  if str(message.from_user.id) == getidx:
    text = f"""
```
You Can't Rob Yourself
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  db = client["user"]
  user_db = db[str(message.from_user.id)]
  user_data = await user_db.find_one()
  rober_cooldown_user = user_data['rober_cooldown']
  current_time = int(time.time())
  minimum_rob = config.minimum_for_rob
  if minimum_rob > user_data['coin']:
    text = f"""
```
You need a minimum of {await command.numtotext(minimum_rob)} on pocket
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  if rober_cooldown_user > current_time:
    time_left = await command.time_left(rober_cooldown_user)
    text = f"""
```
You can't rob any user
Please Wait {time_left}
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  try:
    info = await bot.get_chat_member(message.chat.id,getidx)
    print(info.status)
    if info.status not in ['administrator','member','creator']:
     text = f"""
```
To be robbed,the victim must be a member of this group
```
"""
     await bot.reply_to(message, text, parse_mode="Markdown")
     return 0
  except:
   text = f"""
```
User Not Found In Database
```
"""
   await bot.reply_to(message, text, parse_mode="Markdown")
   return 0
  victim_db = db[getidx]
  victim_data = await victim_db.find_one()
  rob_victim_cooldown = victim_data['rob_victim_cooldown'] 
  current_time = int(time.time())
  minimum_rob = config.minimum_rob
  if minimum_rob > victim_data['coin']:
    text = f"""
```
Victim need a minimum of {await command.numtotext(minimum_rob)} on pocket
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  if rob_victim_cooldown > current_time:
    time_left = await command.time_left(rob_victim_cooldown)
    text = f"""
```
The user was recently a victim of robbery
Please Wait {time_left}
```
"""
    await bot.reply_to(message, text, parse_mode="Markdown")
    return 0
  success_rate = 25
  random_percentage = random.randint(1, 100)
  next_time_rober = int(time.time()) + config.rober_cooldown
  next_time_victim = int(time.time()) + config.rob_victim_cooldown
  
  if message.chat.username is not None:
   group_username = "@" + message.chat.username
  else:
   group_username = "Private Group"
  group_id = message.chat.id
  
  if message.from_user.username is not None:
   rober_username = "@" + message.from_user.username
  else:
   rober_username = "No Username"
  rober_id = message.from_user.id
  
  if random_percentage <= success_rate:
    max_coin_can_be_stolen = user_data['coin'] * 10
    if victim_data["coin"] <= max_coin_can_be_stolen:
      max_coin_can_be_stolen = victim_data["coin"]
    random_stolen_percentage = random.randint(1, 100)
    amount = int((random_stolen_percentage / 100) * max_coin_can_be_stolen)
    rob_percentage = round((amount / victim_data['coin']) * 100,1)
    notification_text = f"""
```
You have been robbed!
``````
{rober_username} ({rober_id}) has stolen {await command.numtotext(amount)} [{rob_percentage}% of your pocket] from you in {group_username} ({group_id})!
```
"""
    text = f"""
```{random_percentage}%
{await random_sentence()}
You managed to get:
₪{await command.numtotext(amount)} [{rob_percentage}% of victims pocket]
```
"""
    await bot.reply_to(message,text,parse_mode="Markdown")
    user_json = {'$inc':{"coin":+amount},"$set":{"rober_cooldown":next_time_rober}}
    victim_json = {'$inc':{"coin":-amount},"$set":{"rob_victim_cooldown":next_time_victim}}
  else:
   random_fine_paid = random.randint(1,25)
   amount = int((random_fine_paid / 100) * user_data['coin'])
   text = f"""
```{random_percentage}%
{await caught_random_sentence()}
You paid victim:
₪{await command.numtotext(amount)} [{random_fine_paid}% of your pocket]

- Current Rob Success Rate Is {success_rate}%
```
"""
   notification_text = f"""
```
You were almost robbed!
``````
{rober_username} ({rober_id}) tried to steal from you in {group_username} ({group_id}), but failed!
You Received:
₪{await command.numtotext(amount)} [{random_fine_paid}% of robers pocket]
```
"""
   await bot.reply_to(message,text,parse_mode="Markdown")
   user_json = {'$inc':{"coin":-amount},"$set":{"rober_cooldown":next_time_rober}}
   victim_json = {'$inc':{"coin":+amount},"$set":{"rob_victim_cooldown":next_time_victim}}
  query = {}
  await asyncio.gather(user_db.update_one(query, user_json),victim_db.update_one(query, victim_json))
  await send_notification(message,int(getidx),notification_text)