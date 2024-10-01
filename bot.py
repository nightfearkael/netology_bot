import telebot
from config import bot_token, reg_keyboard
from pg_connector import Postgre
from translator import translate
import random

bot = telebot.TeleBot(bot_token)
pg_conn = Postgre()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'hello')


@bot.message_handler(commands=['help'])
def help_message(message):
    reply = '''Список доступных команд: 
/help - 
/reg - 
/add_word - 
'''
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['reg'])
def register_message(message):
    user = pg_conn.find_user(message.from_user.id)
    if user is None:
        bot.send_message(message.chat.id, 'Хотите начать обучение?', reply_markup=reg_keyboard)
    else:
        bot.send_message(message.chat.id, 'Вы уже проходите обучение')


@bot.message_handler(commands=['add_word'])
def add_word_message(message):
    if pg_conn.check_admin(message.from_user.id) is not None:
        new_word = bot.send_message(message.from_user.id, 'Какое слово хотите добавить?')
        bot.register_next_step_handler(new_word, add_new_word)
    else:
        bot.reply_to(message, 'Только администраторы могут обновлять словарь')


def add_new_word(new_word):
    ru_word = new_word.text.title()
    en_word = translate(ru_word)
    word_id = pg_conn.find_word_id(ru_word)
    if word_id is not None:
        bot.send_message(new_word.chat.id, 'Слово уже в словаре')
    else:
        if ru_word == en_word:
            bot.send_message(new_word.chat.id, 'Неправильно написано слово, либо я не нашел его перевода в словаре')
        else:
            answers = bot.send_message(new_word.chat.id, f'''Перевод слова {ru_word}: {en_word}
Напишите через запятую еще 3 неправильных варианта перевода на английском языке''')
            bot.register_next_step_handler(answers, add_wrong_answers, ru_word, en_word)


def add_wrong_answers(answers, ru_word, en_word):
    if len(answers.text.split(',')) >= 3:
        choices = answers.text.split(',')[:3]
        choices.append(en_word)
        pg_conn.add_word(ru_word, en_word)
        word_id = pg_conn.find_word_id(ru_word)
        pg_conn.add_choices(word_id[0], choices)
        bot.send_message(answers.chat.id, 'Слово добавлено в словарь')
    else:
        bot.send_message(answers.chat.id, 'Вы ввели недостаточно вариантов')


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    print(call.data)
    print(call.message)
    match call.data:
        case 'register_yes':
            # Добавление нового пользователя в БД
            pg_conn.add_user(telegram_id=call.message.chat.id, first_name=call.message.chat.first_name, last_name=call.message.chat.last_name)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вы успешно зарегистрировались")
            bot.answer_callback_query(callback_query_id=call.id, text='Successfully registered')
        case 'register_no':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Если захотите зарегистрироваться, введите снова /reg")
            bot.answer_callback_query(callback_query_id=call.id, text='Not registered')









bot.polling()