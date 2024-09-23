from environs import Env

env = Env()
env.read_env()
bot_token = env('bot_token')
