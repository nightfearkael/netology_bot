import telebot
from config import bot_token
from pg_connector import Postgre

bot = telebot.TeleBot(bot_token)
pg_conn = Postgre()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'hello')


bot.polling()
