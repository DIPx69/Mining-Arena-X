import telebot
import asyncio
import os
import httpx
import html
import random
import threading
import commands as command
from telebot import types
from telebot.types import Dice
from telebot.async_telebot import *
import motor.motor_asyncio
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)
ownerid = 1794942023
chat_timers = {}
poll_track = {}
async def trivia_group(message):
   async with httpx.AsyncClient() as client:
     api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
     response = await client.get(api_url)
   trivia_data = response.json()
   question = html.unescape(trivia_data["results"][0]["question"])
   difficulty = trivia_data["results"][0]["difficulty"].capitalize() 
   category = trivia_data["results"][0]["category"]
   correct_answer = trivia_data["results"][0]["correct_answer"]
   correct_answer_list = [correct_answer]
   incorrect_answers = trivia_data["results"][0]["incorrect_answers"]
   all_answers_raw = correct_answer_list + incorrect_answers
   all_answers_shuffle = correct_answer_list + incorrect_answers
   random.shuffle(all_answers_shuffle)
   all_answers_shuffle_y = []
   all_answers_shuffle_y = []
   for item in all_answers_shuffle:
     all_answers_shuffle_y += [html.unescape(item)]
   correct_answer_id = all_answers_shuffle.index(correct_answer)
   question_main = f"{question}\n\nYou have 10 seconds to answer\n\n\nCategory\n\n{category}"
   keyboard = types.InlineKeyboardMarkup()
   again_button = types.InlineKeyboardButton(text='⁉️ Again',callback_data='again_quiz')
   keyboard.add(again_button)
   pollx = await bot.send_poll(message.chat.id,question_main,correct_option_id = correct_answer_id,options = all_answers_shuffle_y,is_anonymous = False,type = "quiz",allows_multiple_answers= False)
   payload = {"chat_id": message.chat.id,"message_id": pollx.id,"user_id":message.from_user.id,"name":message.from_user.username,"correct_option_id": correct_answer_id}
   poll_track[str(message.from_user.id)] = payload
   await asyncio.sleep(10)
   try:
    keyboard = types.InlineKeyboardMarkup()
    again_button = types.InlineKeyboardButton(text='⁉️ Again',callback_data='again_quiz')
    keyboard.add(again_button)
    await bot.stop_poll(message.chat.id,pollx.id,reply_markup=keyboard)
    del poll_track[str(message.from_user.id)]
   except:
     ...
async def trivia_call(call):
   async with httpx.AsyncClient() as client:
     api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
     response = await client.get(api_url)
   trivia_data = response.json()
   question = html.unescape(trivia_data["results"][0]["question"])
   difficulty = trivia_data["results"][0]["difficulty"].capitalize() 
   category = trivia_data["results"][0]["category"]
   correct_answer = trivia_data["results"][0]["correct_answer"]
   correct_answer_list = [correct_answer]
   incorrect_answers = trivia_data["results"][0]["incorrect_answers"]
   all_answers_raw = correct_answer_list + incorrect_answers
   all_answers_shuffle = correct_answer_list + incorrect_answers
   random.shuffle(all_answers_shuffle)
   all_answers_shuffle_y = []
   for item in all_answers_shuffle:
     all_answers_shuffle_y += [html.unescape(item)]
   correct_answer_id = all_answers_shuffle.index(correct_answer)
   question_main = f"{question}\n\nYou have 10 seconds to answer\n\n\nCategory\n\n{category}"
   keyboard = types.InlineKeyboardMarkup()
   again_button = types.InlineKeyboardButton(text='⁉️ Again',callback_data='again_quiz')
   keyboard.add(again_button)
   pollx = await bot.send_poll(call.message.chat.id,question_main,correct_option_id = correct_answer_id,options = all_answers_shuffle_y,is_anonymous = False,type = "quiz",allows_multiple_answers= False)
   payload = {"chat_id": call.message.chat.id,"message_id": pollx.id,"user_id":call.from_user.id,"name":call.from_user.username,"correct_option_id": correct_answer_id}
   poll_track[str(call.from_user.id)] = payload
   await asyncio.sleep(10)
   try:
    keyboard = types.InlineKeyboardMarkup()
    again_button = types.InlineKeyboardButton(text='⁉️ Again',callback_data='again_quiz')
    keyboard.add(again_button)
    await bot.stop_poll(call.message.chat.id,pollx.id,reply_markup=keyboard)
    del poll_track[str(call.from_user.id)]
   except:
     ...
async def trivia(call):
   keyboard = types.InlineKeyboardMarkup()
   async with httpx.AsyncClient() as client:
     api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
     response = await client.get(api_url)
   trivia_data = response.json()
   question = html.unescape(trivia_data["results"][0]["question"])
   difficulty = trivia_data["results"][0]["difficulty"].capitalize() 
   category = trivia_data["results"][0]["category"]
   correct_answer = trivia_data["results"][0]["correct_answer"]
   correct_answer_list = [correct_answer]
   incorrect_answers = trivia_data["results"][0]["incorrect_answers"]
   all_answers_raw = correct_answer_list + incorrect_answers
   all_answers_shuffle = correct_answer_list + incorrect_answers
   random.shuffle(all_answers_shuffle)
   keyboard_buttons = {}
   for index, answer in enumerate(all_answers_shuffle):
    button_text = f'{html.unescape(answer)}'
    callback_data = f"answer ['{html.unescape(correct_answer)}','{html.unescape(all_answers_shuffle[index])}']"
    keyboard_buttons[f'answer_{index}'] = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
   keyboard_2 = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
   refresh_button = types.InlineKeyboardButton(text='🔄 Refresh',callback_data='trivia')
   keyboard.add(keyboard_buttons["answer_0"],keyboard_buttons["answer_1"])
   keyboard.add(keyboard_buttons["answer_2"],keyboard_buttons["answer_3"])
   keyboard.add(back_button)
   text = f"*{question}*\n\nYou have 10 seconds to answer\nDifficulty\n*{difficulty}*\nCategory\n*{category}*"
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard)
   chat_timers[call.message.chat.id] = True
   print(chat_timers)
   await asyncio.sleep(10)
   if chat_timers[call.message.chat.id]:
     await timeout(call,correct_answer,difficulty,question,category)
async def timeout(call,correct_answer,difficulty,question,category):
   text = f"*{question}*\n\nYou have 10 seconds to answer\nDifficulty\n*{difficulty}*\nCategory\n*{category}*\n\nThe correct answer was *{correct_answer}*"
   keyboard_2 = types.InlineKeyboardMarkup()
   back_button = types.InlineKeyboardButton(text='🔙 Back',callback_data='main_menu')
   refresh_button = types.InlineKeyboardButton(text='🔄 Refresh',callback_data='trivia')
   keyboard_2.add(refresh_button,back_button)
   await bot.edit_message_text(text,call.from_user.id,call.message.id,parse_mode="Markdown",reply_markup=keyboard_2)