import config
import random
import commands as command
import slash_command as slash
from telebot import types
import asyncio

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

from slash_command import slash_lock
async def predict_word(prefix):
   prefix = prefix.lower()
   available_item = ["minex", "xpboost","potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   matches = [name for name in available_item if name.startswith(prefix)]
   if matches:
     return matches[0]
   else:
     return False
async def buy(message):
   status = await slash.check_lock(message)
   if status is True:
     return False
   get_commands = message.text.split()
   try:
     item_name = get_commands[1]
   except:
    text = """Please provide the item name\n
```
/buy minex 10
```
*Available Items*
- Minex
- Xpboost
- Potato Seed
- Corn Seed
- Carrot Seed
- Broccoli Seed
- Watermelon Seed

We Will Automatically Complete Your Item Name
```Example
/buy min 10 >> /buy minex 10
/buy xp 20 >> /buy xpboost 20
```
"""
    await bot.reply_to(message,text,parse_mode="Markdown")
    return 
   try:
     item_amount = get_commands[2]
     amount = await command.txttonum(item_amount)
   except:
    text = f"""Please provide the amount\n
```
/buy minex 10
```
"""
    await bot.reply_to(message,text,parse_mode="Markdown")
    return
   seed_item =  ["potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   available_item = ["minex", "xpboost","potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   name = await predict_word(item_name)
   if name is False:
     text = """Please provide the item name\n
```
/buy minex 10
```
*Available Items*
- Minex
- Xpboost
- Potato Seed
- Corn Seed
- Carrot Seed
- Broccoli Seed
- Watermelon Seed

We Will Automatically Complete Your Item Name
```Example
/buy watermelon_se 10 >> /buy watermelon_seed 10
/buy xp 20 >> /buy XPboost 20
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   else:
     # Get User Data
     idx = str(message.from_user.id)
     db = client["user"]
     datack = db[idx]
     datafind = await datack.find_one()
     if datafind is None:
       await bot.reply_to(message,"*User Not Found In Database*",parse_mode="Markdown")
       return 0
     coin = datafind["coin"]
     
     # Get Item Data
     print(name.lower())
     if name.lower() in seed_item:
       price = f"{name.lower()}s"
       item_price = getattr(config, price)
       cost = item_price*amount*config.multi_price
     else:
       price = f"{name.lower()}price"
       item_price = getattr(config, price)
       cost = item_price*amount
     if coin >= cost and str(message.from_user.id) not in slash_lock.pending and amount > 0:
       keyboard = types.InlineKeyboardMarkup()
       confirm_button = types.InlineKeyboardButton(text='Accept',callback_data=f'slash buy {name} {amount}')
       decline_button = types.InlineKeyboardButton(text='Decline',callback_data=f'slash buy decline')
       keyboard.add(decline_button,confirm_button)
       text = f"""
```
Pending Confirmation

BUY {name.upper().replace("_", " ")} {item_amount}
Cost: {await command.numtotext(cost)}
```
"""
       await slash.command_lock(message)
       await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard)
     elif str(message.from_user.id) in slash_lock.pending:
       text = f"""

```
Hold Tight 
```*You are unable to interact with this due to an ongoing command or a minor issue
Please finish any open commands*
"""
       await bot.reply_to(message,text,parse_mode="Markdown") 
     elif coin < cost:
      more = cost - coin
      text = f"""
```
You Need More {await command.numtotext(more)} Coin To Buy {amount} {name.upper().replace("_", " ")}
```
"""
      await bot.reply_to(message,text,parse_mode="Markdown") 
     elif amount <= 0:
      text = f"""
```
You need to provide a real amount
```
"""
      await bot.reply_to(message,text,parse_mode="Markdown") 
async def buy_decline(call):
   status = await slash.is_commander(call)
   if status:
     return False
   else:
     text_z = call.message.text
     text = f"""
```
{text_z.replace("Pending Confirmation","Action Canceled")}
```
   """
     await bot.edit_message_text(text,call.message.chat.id,call.message.id,parse_mode="Markdown")
     await slash.command_unlock(call)
async def buy_accept(call):
   status = await slash.is_commander(call)
   if status:
     return False
   else:
     text_z = call.message.text
     text = f"""
```
{text_z.replace("Pending Confirmation","Action Confirmed")}
```
   """
     command = call.data.split()
     item_name = command[2].lower()
     amount = int(command[3])
     text = await buy_confirm(call,item_name,amount)
     await bot.edit_message_text(text,call.message.chat.id,call.message.id,parse_mode="Markdown")
     await slash.command_unlock(call)
 
async def buy_confirm(call,item_name,amount):
   status = await slash.is_commander(call)
   if status:
     return False
   seed_item =  ["potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   item_amount = datafind[item_name]
   if item_name.lower() in seed_item:
     price = f"{item_name.lower()}s"
     item_price = getattr(config, price)
     cost = item_price*amount*config.multi_price
   else:
     price = f"{item_name.lower()}price"
     item_price = getattr(config, price)
     cost = item_price*amount
   if cost <= coin:
     query = {}
     update = {'$inc': {item_name.lower(): amount,'coin': -cost}}
     await datack.update_one(query, update)
     return f"""
 ```
Action Confirmed

You Have Purchased {await command.numtotext(amount)} {item_name.upper().replace("_", " ")}
Cost: {await command.numtotext(cost)}
```
```
Current Coin: {await command.numtotext(coin-cost)}
Current {item_name.upper()}: {item_amount+amount}
```
"""
   else:
     more = cost - coin
     return f"""
 ```
Action Confirmed

You Need More {await command.numtotext(more)} Coin To Buy {await command.numtotext(amount)} {item_name.upper().replace("_", " ")}"
```
"""