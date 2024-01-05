import telebot
from telebot import types
import os
import json
import config
import time
import random
import motor.motor_asyncio
import commands as command
import dns.resolver
from telebot.async_telebot import *
server = os.getenv("server")
token = os.getenv("token")
ratelimit = os.getenv("ratelimit")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
bot_rate = AsyncTeleBot(ratelimit)
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
     await bot.answer_callback_query(call.id, text=f"Its Not Your Turn", show_alert=True)
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
     else:
      get_opponent = int(message.text.split()[1])
   except:
     await bot.reply_to(message,"*Enter a Valid ID\nExample: /ttc 1794942023\nOr Reply With Message*",parse_mode="Markdown")
     return 0
   if get_opponent == message.from_user.id:
     await bot.reply_to(message,"*You Can't Play Yourself*",parse_mode="Markdown")
     return 0
   try:
     user = await bot.get_chat(get_opponent)
   except:
     await bot.reply_to(message,"*Enter a Valid ID\nExample: /ttc 1794942023\nOr Reply With Message*",parse_mode="Markdown")
     return 0
   keyboard = types.InlineKeyboardMarkup()
   challengers = message.from_user.username
   username = user.username
   if username.lower().endswith('bot'):
     await bot.reply_to(message,"*Reply to a valid message*",parse_mode="Markdown")
     return 0
   text =f"*Pending Confirmation\n\nHey @{username}\n@{challengers} Challenging You To Play Tic Tac Toe*"
   decline = types.InlineKeyboardButton(text="Decline", callback_data=f"decline {int(get_opponent)}")
   accept = types.InlineKeyboardButton(text="Accept", callback_data=f"accept {int(get_opponent)}")
   keyboard.add(decline,accept)
   await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard)
async def send_table(call,opponent):
  requester_id = call.json["message"]["reply_to_message"]["from"]["id"]
  requester_name = call.json["message"]["reply_to_message"]["from"]["username"]
  keyboard = types.InlineKeyboardMarkup()
  room_id = str(call.json["message"]["message_id"])
  try:
    user = await bot.get_chat(opponent)
  except:
     await bot.edit_message_text("*Invalid ID*",call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
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
       'username': my_name
       },
    str(players[int(allowed.index(str(opponent)))]):
     { 
       'username': username
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
  text = f"Room ID: *{room_id}*\n@{player_1_name} *[ {player_1_sign} ]* *VS* @{player_2_name} *[ {player_2_sign} ]*\n\nIts @{current_player_name} Turn\n"
  await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown",reply_markup=keyboard)
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
   if get_room_data["current_player"] == 0:
     get_room_data["current_player"] = 1
   else:
     get_room_data["current_player"] = 0
   current_player_get = get_room_data["current_player"]
   current_player_id = get_room_data['allowed'][int(current_player_get)]
   current_player_name = get_room_data[str(current_player_id)]["player_name"]
   text = f"Room ID: *{call.message.id}*\n@{player_1_name} *[ {player_1_sign} ]* *VS* @{player_2_name} *[ {player_2_sign} ]*\n\nIts @{current_player_name} Turn\n"
   winx = await winner_check(get_room_data['board'])
   board_display = "-------------------\n"
   for i in range(0, 9, 3):
       board_display += f"{board[i]} | {board[i+1]} | {board[i+2]}\n"
       if i < 6:
         board_display += "-------------------\n"
   board_display += "-------------------"
   if winx:
     winner_username = get_room_data[winx]["username"]
     result = f"*Game Has Been Finished*\nRoom ID: *{call.message.id}*\n@{player_1_name} *[ {player_1_sign} ]* *VS* @{player_2_name} *[ {player_2_sign} ]*\n\n@{winner_username} Is Legendary Fighter\n\n{board_display}"
     del rooms[str(call.message.id)]
     await bot.edit_message_text(result,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
   elif "ㅤ" not in get_room_data["board"]:
     result = f"*Game Has Been Finished*\nRoom ID: *{call.message.id}*\n@{player_1_name} *[{player_1_sign}]* *VS* @{player_2_name} *[{player_2_sign}]*\n\nDraw 😒\n\n{board_display}"
     del rooms[str(call.message.id)]
     await bot.edit_message_text(result,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown")
   else:
     await bot.edit_message_text(text,call.json["message"]['chat']['id'],call.json["message"]["message_id"],parse_mode="Markdown",reply_markup=keyboard)