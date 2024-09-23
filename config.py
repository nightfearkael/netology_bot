from environs import Env

env = Env()
env.read_env()
bot_token = env('bot_token')

db_host = env('db_host')
db_database = env('db_database')
db_user = env('db_user')
db_password = env('db_password')
db_port = env('db_port')
