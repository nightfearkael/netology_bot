import telebot
from config import bot_token, reg_keyboard
from pg_connector import Postgre

bot = telebot.TeleBot(bot_token)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'hello')


@bot.message_handler(commands=['help'])
def help_message(message):
    reply = '''Список доступных команд: 
/help - 
/reg - 
'''
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['reg'])
def register_message(message):
    pg_conn = Postgre()
    user = pg_conn.find_user(message.from_user.id)
    if user is None:
        bot.send_message(message.chat.id, 'Хотите начать обучение?', reply_markup=reg_keyboard)
    else:
        bot.send_message(message.chat.id, 'Вы уже проходите обучение')




@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    print(call.data)
    print(call.message)
    match call.data:
        case 'register_yes':
            pg_conn = Postgre()
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