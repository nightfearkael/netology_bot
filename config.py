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

reg_keyboard = InlineKeyboardMarkup()
reg_keyboard.add(InlineKeyboardButton(text='Да', callback_data='register_yes'),
                 InlineKeyboardButton(text='Нет', callback_data='register_no'))
