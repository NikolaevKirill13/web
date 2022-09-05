from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from handlers import functions
#from web.database import Database


def faq_keyboard() -> InlineKeyboardMarkup: 
    keyboard = InlineKeyboardMarkup()
    faq = functions.get_faq()
    i = 0
    for title in faq:
        button = InlineKeyboardButton(text = title["title"], callback_data=f"fao_btn{i}")
        i = i + 1
        keyboard.add(button)
    return keyboard

def mute_keyboard(count:int = 0) -> InlineKeyboardMarkup: 
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text = f"{count}", callback_data=f"mute{count}"))
    return keyboard

def welcome_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text = "Нажми на клавишу в течении 60 секунд.", callback_data=f"welcome"))
    return keyboard
