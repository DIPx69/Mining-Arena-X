import telebot
import os
import commands as command
import dns.resolver
from telebot.async_telebot import *
import motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
server = os.getenv("server")
token = os.getenv("token")
client = motor.motor_asyncio.AsyncIOMotorClient(server)
bot = AsyncTeleBot(token)