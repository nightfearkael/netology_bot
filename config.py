from environs import Env
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

env = Env()
env.read_env()
bot_token = env('bot_token')

db_host = env('db_host')
db_database = env('db_database')
db_user = env('db_user')
db_password = env('db_password')
db_port = env('db_port')

emojis = {
    'ru_flag': u"\U0001F1F7" + u"\U0001F1FA",
    'en_flag': u"\U0001F1FA" + u"\U0001F1F8",
    'hearth': u"\u2764",
    'yes': u"\u2705",
    'no': u"\u274C",
    'wave': u"\U0001F44B",
    'hug': u"\U0001F917",

}

reg_keyboard = InlineKeyboardMarkup()
reg_keyboard.add(InlineKeyboardButton(text=f'{emojis["yes"]} Да', callback_data='register_yes'),
                 InlineKeyboardButton(text=f'{emojis["no"]} Нет', callback_data='register_no'))
