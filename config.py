from environs import Env

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
    'next': u"\u23ED",
    'add_word': u"\u2795",
    'del_word': u"\u2716",
}

