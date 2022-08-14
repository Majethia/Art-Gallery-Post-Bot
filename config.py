from telethon import TelegramClient
from telethon import TelegramClient
from pymongo import MongoClient
import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
channel = int(os.environ.get('MAIN_CHANNEL_ID'))
storage = int(os.environ.get('STORAGE_CHANNEL_ID'))
db_url = os.environ.get('MONGO_DB_URL')


client = MongoClient(db_url, tls=True)

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
