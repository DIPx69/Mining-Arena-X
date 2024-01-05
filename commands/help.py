import telebot
import os
import pymongo
import commands as command
import dns.resolver
server = os.getenv("server")
token = os.getenv("token")
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = pymongo.MongoClient(server)
bot = telebot.TeleBot(token)
ownerid = 1794942023
def help(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🔵 Items','🔵 Mining')
    keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,"*Select Option*",parse_mode="Markdown",reply_markup=keyboard)
def automininhelp(message):
    txt = "<b>Mining: Unleash Your Mining Mastery!</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n<u><b>Upgrade:</b></u>\nUsers have the ability to enhance the duration of their  mining by upgrading it\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n<u><b>Server List:</b></u>\nThe user can use the mining feature from other bots. If any bot is full, the text will display a 🔴 symbol, otherwise, it will show a 🟢 symbol.\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n<b><u>What is the reason for using different bots for mining?</u></b>\nUtilizing different bots for mining is an effective approach to prevent latency issues within the main bot. By separating the mining functionality into dedicated bots, the main bot can focus on other tasks without being affected by potential latency problems.\n"
    bot.send_message(message.chat.id,txt,parse_mode="HTML")
    return command.send_home(message)
def itemhelptext(message):
    if message.text =="🔙 Back":
       return help(message)
    if message.text =="🔵 MineX":
       txt ="*MineX: Slash Cooldown, Unleash Power!*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\nThe MineX is a item in Mining Arena that helps miners increase their productivity by reducing cooldown times between mining operations.By integrating with mining equipment and using advanced algorithms, the MineX allows players to mine resources faster, earn more in-game currency, and progress through the game more efficiently\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*NOTE:* When the MineX is active, players will see **_(LOWER COOLDOWN)_** text displayed on their message while mining"
       bot.send_message(message.chat.id,txt,parse_mode="Markdown")
       return command.send_home(message)
    if message.text =="🔵 XPBoost":
       txt ="*XPBoost: Double Your XP, Double Your Fun!*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*XPBoost* is a game-changing item that amplifies your experience points (XP) gains by a whopping *2X*\nWith *XPBoost* in your arsenal, every action you take in the virtual world rewards you with twice the usual amount of XP. Say goodbye to slow progress and hello to rapid advancement as you level up faster than ever before\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*NOTE:* When *XPBoost* is active, a prominent **_(DOUBLE XP)_** message will appear in your mining message, ensuring you never miss a moment of the accelerated experience."
       bot.send_message(message.chat.id,txt,parse_mode="Markdown")
       return command.send_home(message)