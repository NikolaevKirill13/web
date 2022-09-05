import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import ValidationError
from config.config import TOKEN

MODE = sys.argv[1]

if MODE == 'prod':
    logging.basicConfig(level=logging.INFO)
elif MODE == 'dev':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warn("Type MODE in command line!\n Example:'python main.py dev' or 'python main.py prod'")
    sys.exit(1)
try:
    bot = Bot(token = TOKEN, parse_mode="HTML")
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
except (ValidationError):
    logging.warn("Configure TOKEN in config.py!")
    sys.exit(1)