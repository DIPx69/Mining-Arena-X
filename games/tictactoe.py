from telebot import types
import json
import config
import time
import random
import asyncio
import commands as command

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from commands.set_up import client
from commands.set_up import bot
from games.basketball import bot_rate
ownerid = 1794942023
rooms = {}
async def sign(call):
   get_data = call.data.split()
   get_place_id = get_data[1]
   get_room_id = get_data[2] 
   get_user_id = call.from_user.id
   ## Game  Info
   try:
     get_room_data = rooms[str(call.message.id)]
   except:
     await bot.answer_callback_query(call.id,text=f"The room is either non-existent or has expired\nEach room has a validity of only 5 minutes", show_alert=True)
     return 0
   player_1 = rooms[str(call.message.id)]['allowed'][0]
   player_2 = rooms[str(call.message.id)]['allowed'][1]
   game_user = rooms[str(call.message.id)]['allowed']
   ## Check User
   if str(get_user_id) not in game_user:
     await bot.answer_callback_query(call.id, text=f"You Don't Have Permission", show_alert=True)
     return 0
   if rooms[str(get_room_id)]['board'][int(get_place_id)] == "❌" or rooms[str(get_room_id)]['board'][int(get_place_id)] == "⭕":
     await bot.answer_callback_query(call.id, text=f"Already Picked", show_alert=True)
     return 0
   if get_room_data["current_player"] !=  get_room_data[str(call.from_user.id)]["game_id"]:
     await bot.answer_callback_query(call.id, text=f"It's Not Your Turn", show_alert=True)
     return 0
   player_1_data = get_room_data[str(player_1)]
   player_2_data = get_room_data[str(player_2)]
   ## Player 1 Data 
   player_1_name = player_1_data['player_name']
   player_1_id = player_1_data['player_id']
   player_1_game_id = player_1_data['game_id']
   ## Player 2 Data
   player_2_name = player_2_data['player_name']
   player_2_id = player_2_data['player_id']
   player_2_game_id = player_2_data['game_id']
   get_table_data = rooms[str(get_room_id)]['board']
   players = ["❌", "⭕"]
   my_sign = get_room_data[str(call.from_user.id)]["game_id"]
   rooms[str(get_room_id)]['board'][int(get_place_id)] = get_room_data[str(call.from_user.id)]["player_sign"]
   await send_table_update(call)
async def winner_check(game_data):
    winning_combinations = [
       [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
       if game_data[combo[0]] == game_data[combo[1]] == game_data[combo[2]] != "ㅤ":
           return game_data[combo[0]]
    return False
async def confirmation(message):
   try:
     if message.reply_to_message is not None:
      get_opponent = int(message.reply_to_message.from_user.id)
      coin_index = 1
     else:
      data = message.text.split()
      if int(len(data)) > 1:
       args = message.text.split()[1]
       if args.startswith("@"):
         uid = await command.find_uid(args)
         if uid:
           get_opponent = uid
         else:
           raise ValueError("Username Not Found")
       elif args.isdigit():
         get_opponent = int(message.text.split()[1])
      else:
         raise ValueError("Username Not Found")
      coin_index = 2
   except:
     text = f"""
```
Enter a Valid id
``````Example
/ttc 1794942023
/ttc @DipDey
`````` Or Reply With A Message
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   get_bet = 0
   try:
     get_bet = message.text.split()[coin_index]
     get_bet = await command.txttonum(get_bet)
     bet = True
     if not (config.min_bet <= get_bet <= config.max_bet):
       text = f"""
```
Minimum Bet: {await command.numtotext(config.min_bet)}
Maximum Bet: {await command.numtotext(config.max_bet)}
```
"""
       await bot.reply_to(message,text,parse_mode="Markdown")
       return 0
   except Exception as e:
     bet = False
     pass
   db = client["user"]
   datack = db[str(get_opponent)]
   try:
     datafind = await datack.find_one()
   except:
     text = f"""
```
Are You Sure !!!
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   opponent_coin = datafind['coin']
   datack = db[str(message.from_user.id)]
   datafind = await datack.find_one()
   requester_coin = datafind['coin']
   if opponent_coin < get_bet and bet:
     text = f"""
```
Opponent Don't Have Enough Coin To Bet
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   if requester_coin < get_bet and bet:
     text = f"""
```
You Don't Have Enough Coin To Bet
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   if get_opponent == message.from_user.id:
     text = f"""
```
You Can't Play Yourself
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   try:
     user = await bot.get_chat(get_opponent)
   except:
     text = f"""
```
Enter a Valid id
``````Example
/ttc 1794942023
```
``` Or Reply With A Message
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   keyboard = types.InlineKeyboardMarkup()
   challengers = message.from_user.username
   username = user.username
   if username.lower().endswith('bot'):
     text = f"""
```
Reply To A Valid Message
```
"""
     await bot.reply_to(message,text,parse_mode="Markdown")
     return 0
   if bet:
     bet_text = f"""
``` Bet: {await command.numtotext(get_bet)}
```"""
   else:
    bet_text = ""
   text = f"""
```
Pending Confirmation
``` Hey @{username}
```
@{challengers} Challenging You To Play Tic Tac Toe
``` {bet_text}"""
   decline = types.InlineKeyboardButton(text="Decline", callback_data=f"decline {int(get_opponent)}")
   accept = types.InlineKeyboardButton(text="Accept", callback_data=f"accept {int(get_opponent)} {get_bet}")
   keyboard.add(decline,accept)
   await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard)
async def send_table(call,opponent):
  requester_id = call.json["message"]["reply_to_message"]["from"]["id"]
  requester_name = call.json["message"]["reply_to_message"]["from"]["username"]
  keyboard = types.InlineKeyboardMarkup()
  room_id = str(call.json["message"]["message_id"])
  get_bet = int(call.data.split()[2])
  if get_bet != 0:
   bet = True
  else:
   bet = False
  try:
    user = await bot.get_chat(opponent)
  except:
     text = f"""
```
Invalid ID
```
"""
     await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
     return 0
  username = user.username
  username = username.replace("_", "\_")
  my_name = requester_name.replace("_", "\_")
  players = ["❌", "⭕"]
  current_player = 0
  current_player = random.randint(0, 1)
  board = ["ㅤ"] * 9
  allowed = [f'{str(requester_id)}',f'{str(opponent)}']
  random.shuffle(allowed)
  player_1_sign = players[int(allowed.index(str(requester_id)))]
  player_2_sign = players[int(allowed.index(str(opponent)))]
  room_info = {
    'current_player': current_player,
    "bet": bet,
    "amount": get_bet,
    'board': board,
    'allowed' : allowed,
    str(requester_id): {
        'player_name': my_name,
        'player_id': requester_id,
        'player_sign': players[int(allowed.index(str(requester_id)))],
        'game_id': allowed.index(str(requester_id))
    },
    str(opponent): {
        'player_name': username,
        'player_id': opponent,
        'player_sign': players[int(allowed.index(str(opponent)))],
        'game_id': allowed.index(str(opponent))
    },
    str(players[int(allowed.index(str(requester_id)))]):
     { 
       'username': my_name,
       'player_id': requester_id
       },
    str(players[int(allowed.index(str(opponent)))]):
     { 
       'username': username,
       'player_id': opponent
       }
}
  room_info_str = json.dumps(room_info,indent=1)
  rooms[str(room_id)] = room_info
  for i in range(0, 9, 3):
     row_buttons = []
     for j in range(i, i + 3):
         button_text = board[j]
         callback_data = f'ttc {j} {room_id}'
         button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
         row_buttons.append(button)
     keyboard.add(*row_buttons)
  current_player_get = room_info["current_player"]
  current_player_id = room_info['allowed'][int(current_player_get)]
  current_player_name = room_info[str(current_player_id)]["player_name"]
  player_1 = room_info['allowed'][0]
  player_2 = room_info['allowed'][1]
  player_1_data = room_info[str(player_1)]
  player_2_data = room_info[str(player_2)]
   ## Player 1 Data 
  player_1_name = player_1_data['player_name']
  ## Player 2 Data
  player_2_name = player_2_data['player_name']
  if room_info['bet']:
    bet_text = f"``` Bet: {await command.numtotext(str(room_info['amount']))}```"
  else:
    bet_text = ""
  text = f"""
```
Room ID: {room_id}
``````
[1] @{player_1_name} [ {player_1_sign} ]
``````
[2] @{player_2_name} [ {player_2_sign} ]
```
```
It\'s @{current_player_name}\'s turn.
```{bet_text}
"""
  await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown",reply_markup=keyboard)
  if bet:
    coin_data = {'$inc':{"coin": -get_bet}}
    query = {}
    player_data = client["user"]
    player_1_data = player_data[str(player_1_data['player_id'])]
    player_2_data = player_data[str(player_2_data['player_id'])]
    await asyncio.gather(player_1_data.update_one(query,coin_data),player_2_data.update_one(query,coin_data))
async def send_table_update(call):
   get_room_data = rooms[str(call.message.id)]
   player_1 = rooms[str(call.message.id)]['allowed'][0]
   player_2 = rooms[str(call.message.id)]['allowed'][1]
   player_1_data = get_room_data[str(player_1)]
   player_2_data = get_room_data[str(player_2)]
   ## Player 1 Data 
   player_1_name = player_1_data['player_name']
   player_1_sign = player_1_data['player_sign']
   player_1_id = player_1_data['player_id']
   player_1_game_id = player_1_data['game_id']
   ## Player 2 Data
   player_2_name = player_2_data['player_name']
   player_2_sign = player_2_data['player_sign']
   player_2_id = player_2_data['player_id']
   player_2_game_id = player_2_data['game_id']
   ## Room Config
   room_id = str(call.json["message"]["message_id"])
   board = get_room_data["board"]
   ## Button Declare
   keyboard = types.InlineKeyboardMarkup()
   for i in range(0, 9, 3):
     row_buttons = []
     for j in range(i, i + 3):
         button_text = board[j]
         callback_data = f'ttc {j} {room_id}'
         button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
         row_buttons.append(button)
     keyboard.add(*row_buttons)
   if get_room_data['bet']:
     bet_text = f"``` Bet: {await command.numtotext(str(get_room_data['amount']))}```"
   else:
     bet_text = ""
   if get_room_data["current_player"] == 0:
     get_room_data["current_player"] = 1
   else:
     get_room_data["current_player"] = 0
   current_player_get = get_room_data["current_player"]
   current_player_id = get_room_data['allowed'][int(current_player_get)]
   current_player_name = get_room_data[str(current_player_id)]["player_name"]
   text = f"""
```
Room ID: {room_id}
``````
[1] @{player_1_name} [ {player_1_sign} ]
``````
[2] @{player_2_name} [ {player_2_sign} ]
```
```
It\'s @{current_player_name}\'s turn.
```{bet_text}
"""
   winx = await winner_check(get_room_data['board'])
   board_display = "------------\n"
   for i in range(0, 9, 3):
       board_display += f"{board[i]} | {board[i+1]} | {board[i+2]}\n"
       if i < 6:
         board_display += "------------\n"
   board_display += "------------"
   if winx:
     winner_username = get_room_data[winx]["username"]
     text = f"""
```
Game Has Been Finished
``````
Room ID: {room_id}
``````
[1] @{player_1_name} [ {player_1_sign} ]
``````
[2] @{player_2_name} [ {player_2_sign} ]
``````
@{winner_username} Is Legendary Fighter
``````
{board_display}
```{bet_text}
"""
     await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
     if get_room_data['bet']:
       coin_data = {'$inc':{"coin": get_room_data['amount']*2}}
       query = {}
       player_data = client["user"]
       winner_data = player_data[str(get_room_data[winx]['player_id'])]
       await winner_data.update_one(query,coin_data)
     del rooms[str(call.message.id)]
   elif "ㅤ" not in get_room_data["board"]:
     text = f"""
```
Game Has Been Finished
``````
Room ID: {room_id}
``````
[1] @{player_1_name} [ {player_1_sign} ]
``````
[2] @{player_2_name} [ {player_2_sign} ]
``````
Draw
``````
{board_display}
```{bet_text}
"""
     await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
     if get_room_data['bet']:
       coin_data = {'$inc':{"coin": get_room_data['amount']}}
       query = {}
       player_data = client["user"]
       player_1_data = player_data[str(player_1_game_id)]
       player_2_data = player_data[str(player_2_game_id)]
       await asyncio.gather(player_1_data.update_one(query,coin_data),player_2_data.update_one(query,coin_data))
       del rooms[str(call.message.id)]
   else:
     await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown",reply_markup=keyboard)