from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import emojis
import random


def generate_reg_keyboard():
    reg_keyboard = InlineKeyboardMarkup()
    reg_keyboard.add(InlineKeyboardButton(text=f'{emojis["yes"]} Да', callback_data='register_yes'),
                     InlineKeyboardButton(text=f'{emojis["no"]} Нет', callback_data='register_no'))
    return reg_keyboard


def generate_word_keyboard(buttons):
    choices_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    random.shuffle(buttons)
    choices_keyboard.add(*buttons)
    add_word_button = f'Добавить слово {emojis["add_word"]}'
    del_word_button = f'Удалить слово {emojis["del_word"]}'
    next_word_button = f'Дальше {emojis["next"]}'
    choices_keyboard.add(add_word_button, del_word_button, next_word_button)
    return choices_keyboard


def remove_keyboard():
    kb = ReplyKeyboardRemove()
    return kb
