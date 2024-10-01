import time

import telebot
from telebot.handler_backends import State, StatesGroup
from config import bot_token, emojis
from pg_connector import Postgre
from translator import translate
from replies import start_reply, help_reply
from keyboards import generate_reg_keyboard, generate_word_keyboard, remove_keyboard

bot = telebot.TeleBot(bot_token)
pg_conn = Postgre()


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, start_reply)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, help_reply, parse_mode='HTML')


@bot.message_handler(commands=['progress'])
def progress_message(message):
    progress = pg_conn.count_words(message.from_user.id)
    if progress is None:
        bot.reply_to(message, f'В данный момент твой словарь еще пуст')
    else:
        bot.reply_to(message, f'В данный момент ты изучаешь {progress[0]} слов')


@bot.message_handler(commands=['reg'])
def register_message(message):
    user = pg_conn.find_user(message.from_user.id)
    if user is None:
        bot.send_message(message.chat.id, 'Хотите начать обучение?', reply_markup=generate_reg_keyboard())
    else:
        bot.send_message(message.chat.id, 'Вы уже проходите обучение')


@bot.message_handler(commands=['add_word'])
def add_word_message(message):
    if pg_conn.check_admin(message.from_user.id) is not None:
        new_word = bot.send_message(message.from_user.id, f'Какое {emojis["ru_flag"]} слово хотите добавить?')
        bot.register_next_step_handler(new_word, add_new_word)
    else:
        bot.reply_to(message, 'Только администраторы могут обновлять словарь')


def add_new_word(new_word):
    ru_word = new_word.text.title()
    en_word = translate(ru_word)
    word_id = pg_conn.find_word_id(ru_word)
    if word_id is not None:
        bot.send_message(new_word.chat.id, f'Слово {emojis["ru_flag"]} {ru_word} уже в словаре')
    else:
        if ru_word == en_word:
            bot.send_message(new_word.chat.id, 'Неправильно написано слово, либо я не нашел его перевода в словаре')
        else:
            answers = bot.send_message(new_word.chat.id, f'''Перевод слова {emojis["ru_flag"]} {ru_word}: {emojis["en_flag"]} {en_word}
Напишите через запятую еще 3 неправильных варианта перевода на {emojis["en_flag"]} английском языке''')
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


@bot.message_handler(commands=['word'])
def education(message):
    word_list = pg_conn.select_random_word()
    ru_word = word_list[0]
    en_word = word_list[1]
    buttons = word_list[2]
    choice_kb = generate_word_keyboard(buttons)
    bot.send_message(message.chat.id, f'Выбери перевод слова {emojis["ru_flag"]} {ru_word}', reply_markup=choice_kb)

    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = ru_word
        data['translate_word'] = en_word
        data['other_words'] = buttons


@bot.message_handler(func=lambda message: message.text == f'Дальше {emojis["next"]}')
def next_word(message):
    education(message)


@bot.message_handler(func=lambda message: message.text == f'Добавить слово {emojis["add_word"]}')
def user_add_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        pg_conn.add_word_to_user(message.chat.id, data['target_word'])


@bot.message_handler(func=lambda message: message.text == f'Удалить слово {emojis["del_word"]}')
def user_del_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        pg_conn.del_word_from_user(message.chat.id, data['target_word'])


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    answer = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['translate_word']
        if answer == target_word:
            bot.send_message(message.chat.id, f'Отлично! {emojis["ru_flag"]} {data["target_word"]} -> {emojis["en_flag"]} {data["translate_word"]}',
                             reply_markup=remove_keyboard())
        else:
            bot.send_message(message.chat.id, f'Неправильно, попробуй еще раз вспомнить перевод {data["target_word"]}')


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    match call.data:
        case 'register_yes':
            # Добавление нового пользователя в БД
            pg_conn.add_user(telegram_id=call.message.chat.id, first_name=call.message.chat.first_name, last_name=call.message.chat.last_name)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Вы успешно зарегистрировались {emojis["hearth"]}')
            bot.answer_callback_query(callback_query_id=call.id, text='Successfully registered')
        case 'register_no':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Если захотите зарегистрироваться, введите снова /reg")
            bot.answer_callback_query(callback_query_id=call.id, text='Not registered')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
