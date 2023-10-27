import logging
import os

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError

# Generate bot object and
# validation of token
try:
    bot: Bot = Bot(token=os.environ.get('BOT_TOKEN'), parse_mode=ParseMode.HTML)
except TokenValidationError:
    logging.error('Token is invalid or empty')
    exit(1)
