import telebot
import os
import config
import time
import commands as command
import platform
import aiohttp
import dns.resolver
from telebot.async_telebot import *
import motor.motor_asyncio
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
delay = config.leaderboard_uptime_delay
sign = "🔴"
total_update = 0
uptime_start = int(time.time())
leaderboard_data = {}
async def info(call):
   global total_update
   uptime_seconds = int(time.time() - uptime_start)
   days = uptime_seconds // (24 * 3600)
   hours = (uptime_seconds % (24 * 3600)) // 3600
   minutes = (uptime_seconds % 3600) // 60
   seconds = uptime_seconds % 60
   if days > 0:
     uptime_text = f"{days}d:{hours}h:{minutes}m:{seconds}s"
   else:
     uptime_text = f"{hours}h:{minutes}m:{seconds}s"
   system_info = {
    "System": platform.system(),
    "Node": platform.node(),
    "Release": platform.release(),
    "Version": platform.version(),
    "Machine": platform.machine()}
   system_info_string = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
   await bot.answer_callback_query(call.id, text=f"Server Status\nBot Uptime: {uptime_text}\n{system_info_string}",show_alert=True)
async def leadboard_update(message):
  if message.chat.id != ownerid:
     userx = message.from_user
     username = userx.username
     username = username.replace("_", "\\_")
     await bot.send_message(ownerid,f'@{username} *({message.chat.id})* Trying To Run Admin Command',parse_mode="Markdown")
  else:
    start = time.time()
    send = await bot.send_message(message.chat.id,"*UPDATING LEADERBOARD*",parse_mode="Markdown")
    await updateleaderboard()
    await bot.edit_message_text(f"*LEADERBOARD UPDATED*\n{(time.time()-start)} Sec",message.chat.id,send.message_id,parse_mode="Markdown")
async def fetch_user_data(user_id):
    db = client["user"]
    user = await bot.get_chat(user_id)
    username = user.username
    if username:
        username = username.replace("_", "\\_")
    else:
        username = f"User {user_id}"
    collection = db[user_id]
    leaderboard_data_coin = await collection.find().sort('coin', -1).to_list(10)
    leaderboard_data_mine = await collection.find().sort('mymine', -1).to_list(10)
    leaderboard_data_level = await collection.find().sort('level', -1).to_list(10)
    leaderboard_data_prestige = await collection.find().sort('prestige', -1).to_list(10)

    leaderboard_coin_get = [(username, entry.get('coin', 0)) for entry in leaderboard_data_coin]
    leaderboard_mine_get = [(username, entry.get('mymine', 0)) for entry in leaderboard_data_mine]
    leaderboard_level_get = [(username, entry.get('lvl', 0)) for entry in leaderboard_data_level]
    leaderboard_prestige_get = [(username, entry.get('prestige', 0)) for entry in leaderboard_data_prestige]

    return leaderboard_coin_get, leaderboard_mine_get, leaderboard_level_get, leaderboard_prestige_get
async def updateleaderboard():
    leaderboard_coin = []
    leaderboard_mine = []
    leaderboard_level = []
    leaderboard_prestige = []
    start_time = int(time.time())
    global leaderboard_data
    db = client["user"]
    dblist = await db.list_collection_names()
    tasks = [fetch_user_data(user_id) for user_id in dblist]
    results = await asyncio.gather(*tasks)
    for leaderboard_coin_get, leaderboard_mine_get, leaderboard_level_get, leaderboard_prestige_get in results:
        leaderboard_coin.extend(leaderboard_coin_get)
        leaderboard_mine.extend(leaderboard_mine_get)
        leaderboard_level.extend(leaderboard_level_get)
        leaderboard_prestige.extend(leaderboard_prestige_get)
    leaderboard_coin.sort(key=lambda x: x[1], reverse=True)
    leaderboard_mine.sort(key=lambda x: x[1], reverse=True)
    leaderboard_level.sort(key=lambda x: x[1], reverse=True)
    leaderboard_prestige.sort(key=lambda x: x[1], reverse=True)
    leaderboard_text_coin = '*[COIN LEADERBOARD]*\n\n'
    leaderboard_text_mine = '*[TOTAL MINE LEADERBOARD]*\n\n'
    leaderboard_text_level = '*[LEVEL LEADERBOARD]*\n\n'
    leaderboard_text_prestige = '*[PRESTIGE LEADERBOARD]*\n\n'
    top_text = []
    for index_coin, entry_coin in enumerate(leaderboard_coin[:10], start=1):
        username, coin = entry_coin
        coin = await command.numtotext(coin)
        if index_coin == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"Top User || COIN || @{new_username} || {coin}"]
        leaderboard_text_coin += f"*[{index_coin}]* @{username} Coins: *{coin}*\n"
    for index_mine, entry_mine in enumerate(leaderboard_mine[:10], start=1):
        username, mymine = entry_mine
        mymine = await command.numtotext(mymine)
        if index_mine == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"Top User || MINE || @{new_username} || {mymine}"]
        leaderboard_text_mine += f"*[{index_mine}]* @{username} Total Mining: *{mymine}*\n"
    for index_level, entry_level in enumerate(leaderboard_level[:10], start=1):
        username, level = entry_level
        level = await command.numtotext(level)
        if index_level == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"Top User || LEVEL || @{new_username} || {level}"]
        leaderboard_text_level += f"*[{index_level}]* @{username} Level: *{level}*\n"
    for index_prestige, entry_prestige in enumerate(leaderboard_prestige[:10], start=1):
        username, prestige = entry_prestige
        prestige = await command.numtotext(prestige)
        if index_prestige == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"Top User || PRESTIGE || @{new_username} || {prestige}"]
        leaderboard_text_prestige += f"*[{index_prestige}]* @{username} Prestige: *{prestige}*\n"
    top_text_x = random.choice(top_text)
    await bot.set_my_commands([telebot.types.BotCommand("top", f"{top_text_x}"),telebot.types.BotCommand("start", "Start"),telebot.types.BotCommand("leaderboard", "Leaderboard"),
    telebot.types.BotCommand("profile", "View Profile"),
    telebot.types.BotCommand("games", "Available Games"),
    telebot.types.BotCommand("quiz", "Play Trivia"),
    telebot.types.BotCommand("roll", "Roll The Dice"),
    telebot.types.BotCommand("dart", "Throw The Dart"),
    telebot.types.BotCommand("basket", "Throw The Basketball"),
    telebot.types.BotCommand("ball", "Throw The Football"),
    telebot.types.BotCommand("ttc", "Play Tic Tac Toe"),
    telebot.types.BotCommand("info", "Information About Bot"),
    telebot.types.BotCommand("notice", "Notice About Maintenance this text")])
    db = client['leadboard']
    datack = db["data"]
    query = {}
    nowtime = int(time.time())
    leaderboard_data_x = {
            'cointime': nowtime,
            'coin': leaderboard_text_coin,
            'minetime': nowtime,
            'mine': leaderboard_text_mine,
            'leveltime': nowtime,
            'level': leaderboard_text_level,
            'prestigetime': nowtime,
            'prestige': leaderboard_text_prestige}
    leaderboard_data["leaderboard"] = leaderboard_data_x
    updatex = {
        '$set': {
            'cointime': nowtime,
            'coin': leaderboard_text_coin,
            'minetime': nowtime,
            'mine': leaderboard_text_mine,
            'leveltime': nowtime,
            'level': leaderboard_text_level,
            'prestigetime': nowtime,
            'prestige': leaderboard_text_prestige
        }
    }
    await datack.update_one(query, updatex)