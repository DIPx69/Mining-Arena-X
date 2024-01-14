import config
import random
import commands as command
import slash_command as slash
from telebot import types

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot

from slash_command import slash_lock

async def predict_word(prefix):
   prefix = prefix.lower()
   available_item = ["iron", "coal", "silver", "crimsteel", "gold", "mythan", "magic", "potato", "corn", "carrot", "broccoli", "watermelon", "potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   matches = [name for name in available_item if name.startswith(prefix)]
   if matches:
     return matches[0]
   else:
     return False
async def sell(message):
   status = await slash.check_lock(message)
   if status is True:
     return False
   get_commands = message.text.split()
   try:
     item_name = get_commands[1]
   except:
    text = """Please provide the item name\n
```
/sell iron 10
```
*Available Items:*
- Iron
- Coal
- Silver
- Crimsteel
- Gold
- Mythan
- Magic
- Potato
- Corn
- Carrot
- Broccoli
- Watermelon
- Potato Seed
- Corn Seed
- Carrot Seed
- Broccoli Seed
- Watermelon Seed

We Will Automatically Complete Your Item Name
```Example
/sell cri 10 >> /sell crimsteel 10
/sell i 20 >> /sell iron 20
```
"""
    await bot.reply_to(message,text,parse_mode="Markdown")
    return 
   try:
     idx = str(message.from_user.id)
     db = client["user"]
     datack = db[idx]
     datafind = await datack.find_one()
     if datafind is None:
       await bot.reply_to(message,"*User Not Found In Database*",parse_mode="Markdown")
       return 0
     name = await predict_word(item_name)
     item_amount_get = datafind[name]
     item_amount = get_commands[2]
     if item_amount.endswith("%"):
       percentage = int(item_amount.replace("%",""))/100
       item_amount = int(item_amount_get*percentage)
       print(item_amount)
       if item_amount > 0:
         amount = await command.txttonum(str(item_amount))
       else:
         await command.txttonum("error")
     elif item_amount in ["max","all"]:
       amount = item_amount_get 
     elif item_amount in ["half"]:
       amount = int(item_amount_get/2)
     else:
       amount = int(get_commands[2])
     if amount < 0:
       await command.txttonum("error")
   except Exception as e:
    print(str(e))
    if name == False:
      name = "iron"
    text = f"""Please provide the amount\n
```
/sell {name} 10
```
"""
    await bot.reply_to(message,text,parse_mode="Markdown")
    return
   plant_item = ["potato", "corn", "carrot", "broccoli", "watermelon"]
   seed_item =  ["potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   available_item = ["iron", "coal", "silver", "crimsteel", "gold", "mythan", "magic", "potato", "corn", "carrot", "broccoli", "watermelon", "potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   name = await predict_word(item_name)
   if name is False:
     text = """Please provide the item name\n
```
/sell minex 10
```
*Available Items:*
- Iron
- Coal
- Silver
- Crimsteel
- Gold
- Mythan
- Magic
- Potato
- Corn
- Carrot
- Broccoli
- Watermelon
- Potato Seed
- Corn Seed
- Carrot Seed
- Broccoli Seed
- Watermelon Seed

We Will Automatically Complete Your Item Name
```Example 
/sell watermelon_se 10 >> /sell watermelon_seed 10
/sell crim 20 >> /sell crimsteel 20
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   else:
     # Get User Data
     coin = datafind["coin"]
     item_amount = datafind[name]
     
     # Get Item Data
     if name.lower() in plant_item:
       price = f"{name.lower()}"
     elif name.lower() in seed_item:
       price = f"{name.lower()}s"
     else:
       price = f"{name.lower()}price"
     item_price = getattr(config, price)
     total = item_price*amount
     print(item_amount-amount)
     if str(message.from_user.id) not in slash_lock.pending and item_amount-amount >= 0:
       keyboard = types.InlineKeyboardMarkup()
       confirm_button = types.InlineKeyboardButton(text='Accept',callback_data=f'slash sell {name} {amount}')
       decline_button = types.InlineKeyboardButton(text='Decline',callback_data=f'slash sell decline')
       keyboard.add(decline_button,confirm_button)
       text = f"""
```
Pending Confirmation

SELL {name.upper().replace("_", " ")} {amount}
Total Price: {await command.numtotext(total)}
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
     elif item_amount-amount < 0:
       more = amount - item_amount
       text = f"""

```
You Need More {await command.numtotext(more)} {name.upper().replace("_", " ")} To Sell {amount} {name.upper().replace("_", " ")}
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
async def sell_decline(call):
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
async def sell_accept(call):
   data = call.json
   if data["from"]["id"] != data["message"]["reply_to_message"]["from"]["id"]:
     username = data["message"]["reply_to_message"]["from"]["username"]
     await bot.answer_callback_query(call.id, text=f"This menu is controlled by @{username}\nYou will have to run the original command yourself.", show_alert=True)
     return 0
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
     text = await sell_confirm(call,item_name,amount)
     await bot.edit_message_text(text,call.message.chat.id,call.message.id,parse_mode="Markdown")
     await slash.command_unlock(call)
 
async def sell_confirm(call,item_name,amount):
   status = await slash.is_commander(call)
   if status:
     return False
   plant_item = ["potato", "corn", "carrot", "broccoli", "watermelon"]
   seed_item =  ["potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   available_item = ["iron", "coal", "silver", "crimsteel", "gold", "mythan", "magic", "potato", "corn", "carrot", "broccoli", "watermelon", "potato_seed", "corn_seed", "carrot_seed", "broccoli_seed", "watermelon_seed"]
   idx = str(call.from_user.id)
   db = client["user"]
   datack = db[idx]
   datafind = await datack.find_one()
   coin = datafind["coin"]
   item_amount = datafind[item_name]
   if item_name.lower() in plant_item:
     price = f"{item_name.lower()}"
   elif item_name.lower() in seed_item:
     price = f"{item_name.lower()}s"
   else:
     price = f"{item_name.lower()}price"
   item_price = getattr(config, price)
   total = item_price*amount
   if item_amount-amount >= 0:
     query = {}
     update = {'$inc': {item_name.lower(): -amount,'coin': total}}
     await datack.update_one(query, update)
     return f"""
 ```
Action Confirmed

You Have Sold {await command.numtotext(amount)} {item_name.upper().replace("_", " ")}
Total Price: {await command.numtotext(total)}
```
```
Current Coin: {await command.numtotext(coin+total)}
Current {item_name.upper()}: {item_amount-amount}
```
"""
   else:
     more = amount - item_amount
     return f"""
 ```
Action Confirmed

You Need More {await command.numtotext(more)} {item_name.upper().replace("_", " ")} To Sell {await command.numtotext(amount)}
```
"""