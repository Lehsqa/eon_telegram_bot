import os

from aiogram import Bot
from aiogram.enums import ParseMode

bot = Bot(token=os.environ.get('BOT_TOKEN'), parse_mode=ParseMode.HTML)
