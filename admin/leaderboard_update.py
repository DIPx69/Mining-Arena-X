import telebot
import os
import json 
import time
import aiofiles
import dns.resolver
from telebot.async_telebot import *
import motor.motor_asyncio
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
leaderboard_data = {}
mode = False
uptime_start = int(time.time())
async def addToHistory(name:str,mode:str, amount:str):
   async with aiofiles.open("admin/history.json", 'r') as f:
     data = json.loads(await f.read())
   len_history = len(data)
   data = {str(int(key)+1): message for key, message in data.items()}
   data["1"] = {
     "name":name.strip(),
     "mode":mode.strip(),
     "amount":amount.strip(),
     "timestamp": int(time.time())
   }
   sorted_history = sorted(data.items(), key=lambda x: int(x[0]))
   sorted_history_dict = {k: v for k, v in sorted_history}
   if len(sorted_history_dict) >= 16:
     del sorted_history_dict[str(16)]
   async with aiofiles.open("admin/history.json", 'w') as f:
     await f.write(json.dumps(sorted_history_dict))
   return sorted_history_dict
async def numtotext(number):
    abbreviations = [
        (1e12, 'T'),
        (1e9, 'B'),
        (1e6, 'M'),
        (1e3, 'K')
    ]
    for factor, suffix in abbreviations:
        if number >= factor:
            abbreviated = number / factor
            return f"{abbreviated:.2f}{suffix}"
    return str(number)
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

async def request_update(message):
   global mode
   if mode == False:
     mode = True
     await bot.send_message(message.chat.id,"Turned On")
     while True:
       start = time.time()
       print("Leadboard Updating...")
       await updateleaderboard()
       end = time.time() - start
       print(f"Leadboard Updated [ IT TOOK {end:.2f} SECOND ]")
       await asyncio.sleep(60)
   else:
     await bot.send_message(message.chat.id,"Already On")

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
        coin = await numtotext(coin)
        if index_coin == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"COIN || @{new_username} || {coin}"]
        leaderboard_text_coin += f"*[{index_coin}]* @{username} Coins: *{coin}*\n"
    for index_mine, entry_mine in enumerate(leaderboard_mine[:10], start=1):
        username, mymine = entry_mine
        mymine = await numtotext(mymine)
        if index_mine == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"MINE || @{new_username} || {mymine}"]
        leaderboard_text_mine += f"*[{index_mine}]* @{username} Total Mining: *{mymine}*\n"
    for index_level, entry_level in enumerate(leaderboard_level[:10], start=1):
        username, level = entry_level
        level = await numtotext(level)
        if index_level == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"LEVEL || @{new_username} || {level}"]
        leaderboard_text_level += f"*[{index_level}]* @{username} Level: *{level}*\n"
    for index_prestige, entry_prestige in enumerate(leaderboard_prestige[:10], start=1):
        username, prestige = entry_prestige
        prestige = await numtotext(prestige)
        if index_prestige == 1:
          new_username = username.replace("\\_","_")
          top_text += [f"PRESTIGE || @{new_username} || {prestige}"]
        leaderboard_text_prestige += f"*[{index_prestige}]* @{username} Prestige: *{prestige}*\n"
    top_text_x = random.choice(top_text)
    split_top_text = top_text_x.split("||")
    addToHistory_data = await addToHistory(split_top_text[1],split_top_text[0],split_top_text[2])
    await bot.set_my_commands([telebot.types.BotCommand("top", f"{top_text_x}"),telebot.types.BotCommand("start", "Start"),telebot.types.BotCommand("claim","Claim Free Rewards"),telebot.types.BotCommand("buy","Buy Items"),telebot.types.BotCommand("sell","Sell Items"),telebot.types.BotCommand("inventory", "Inventory"),telebot.types.BotCommand("leaderboard", "Leaderboard"),
    telebot.types.BotCommand("profile", "View Profile"),
    telebot.types.BotCommand("games", "Available Games"),
    telebot.types.BotCommand("quiz", "Play Trivia"),
    telebot.types.BotCommand("roll", "Roll The Dice"),
    telebot.types.BotCommand("dart", "Throw The Dart"),
    telebot.types.BotCommand("basket", "Throw The Basketball"),
    telebot.types.BotCommand("ball", "Throw The Football"),
    telebot.types.BotCommand("ttc", "Play Tic Tac Toe"),
    telebot.types.BotCommand("info", "Information About Bot"),
    telebot.types.BotCommand("notice", "Notice About Maintenance")])
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
            'prestige': leaderboard_text_prestige,
            "history":addToHistory_data
        }
    }
    await datack.update_one(query, updatex)