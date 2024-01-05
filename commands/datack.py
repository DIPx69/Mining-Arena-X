import telebot
import asyncio
import os
import time
import commands as command
from telebot import types
from telebot.types import Dice
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
from dotenv import load_dotenv
load_dotenv()
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
async def datackx(message):
   idx = str(message.chat.id)
   db = client["user"]
   dataadd = db[idx]
   dataaddx = {"coin":50000,"prestige":0,"prestigecoin":0,"minex":0,"xpboost":0,"iron":0,"coal":0,"silver":0,"crimsteel":0,"gold":0,"mythan":0,"magic":0,"mymine":0,"lvl":1,"xp":0,"nxtlvlxp":100,"dailycooldown":int(time.time()),"minecooldown":0,"warn": 0,"mineon": 0,"automineon": 0,"autominelvl": 2,"itemmulti": 1,"xpmulti": 1,"lvlnoti":0,"ban": 0,"gamecooldown": 0,'streaks': 1,'minexactive': 0,'xpboostactive':0,'mining_item':"none",'xpboost_on':0,'minex_on':0,'end_time': 0,"dice_won":0,"dice_lose":0,"dart_won":0,"dart_lose":0,"basketball_won":0,"basketball_lose":0,"football_won":0,"football_lose":0,"title_list":['Noob'],"active_title":"Noob","maximum_automine_lvl": 2,'potato_seed': 0, 'broccoli': 9, 'broccoli_seed': 0, 'carrot': 0, 'carrot_seed': 0, 'corn': 0, 'corn_seed': 0, 'potato': 0, 'tile_1': 0, 'tile_2': 0, 'tile_3': 0, 'tile_4': 0, 'tile_5': 0, 'tile_6': 0, 'tile_7': 0, 'tile_8': 0, 'tile_9': 0, 'tile_name_1': 'None', 'tile_name_2': 'None', 'tile_name_3': 'None', 'tile_name_4': 'None', 'tile_name_5': 'None', 'tile_name_6': 'None', 'tile_name_7': 'None', 'tile_name_8': 'None', 'tile_name_9': 'None', 'watermelon': 0, 'watermelon_seed': 0, 'water': 0,'sell_all':0}
   await dataadd.insert_one(dataaddx)
async def datack(message):
   txt = '*Welcome to Mining Arena (Beta)!!*\n\n🌟 Are you ready to dig deep, overcome challenges, and become a legendary miner? Join the Mining Arena Game now and let the adventure begin!\n\n🏆 Compete with fellow miners in exciting challenges, tournaments(soon), and leaderboard battles. Rise to the top and prove yourself as the ultimate mining champion!\n\n🎁 Daily rewards, special events, and exclusive bonuses await you on your mining journey. Stay alert and seize every opportunity for fame and fortune!\n\n💰 Upgrade your equipment, and strengthen your mining arsenal. As you progress, unlock new areas and uncover the secrets hidden deep within the earth\n\n🌱 Immerse yourself in the art of planting and experience the joy of a bountiful harvest as you cultivate your fields with care 🍉 🌽 🥔 \n\nPlease note that this bot is currently running in the beta phase, which means that the product is still being fine-tuned and optimized. Your valuable feedback and insights will play a crucial role in identifying any potential issues, improving user experience, and refining our offering\n\nAs a beta tester, your valuable contribution to our testing program is greatly appreciated. We are pleased to inform you that your efforts will not go unnoticed, and we have something special in store for you when we officially launch our product\n\nIf you have any questions or need assistance, feel free to reach out to our friendly support team @MiningArenaSupportBot\n\nHappy mining!!!\n\nUpdate Channel @MiningArenaUpdates\nGroup Chat @MiningArenaChats'
   keyboard = types.InlineKeyboardMarkup()
   keyboard_2 = types.InlineKeyboardMarkup()
   start_button = types.InlineKeyboardButton(text='🚀 Generating User Profile',callback_data='gen')
   keyboard.add(start_button)
   userx = message.from_user
   username = userx.username
   if username == None:
     await bot.send_message(message.chat.id,"*Kindly Set a Username From Telegram Profile*",parse_mode="Markdown")
   else:
     username = username.replace("_", "\\_")
     idx = str(message.chat.id)
     txtx =f'@{username} Start The Bot For First Time\n*ID:* `{idx}`'
     db = client["user"]
     dblist = await db.list_collection_names()
     if idx not in dblist:
      send = await bot.send_message(message.chat.id,txt,parse_mode="HTML",reply_markup=keyboard)
      await bot.send_message(ownerid,txtx,parse_mode="Markdown")
      await datackx(message)
      text = '💬 Join Official Group Chat'
      url = 'https://t.me/MiningArenaChats'
      button1 = types.InlineKeyboardButton(text=text, url=url)
      button2 = types.InlineKeyboardButton(text="💬 Join Updates Channel", url="https://t.me/MiningArenaUpdates")
      keyboard_2.add(button1)
      keyboard_2.add(button2)
      await bot.edit_message_text(txt,message.chat.id,send.message_id,parse_mode="Markdown",reply_markup=keyboard_2)