# netology_bot

## create enviroment file .env with:
bot_token = '{place bot token here}'

db_host = '{your database host}'

db_port = '{database port}'

db_database = '{your bot database}'

db_user = '{database user}'

db_password = '{database user's password}'



CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	telegram_id INTEGER NOT NULL,
    first_name VARCHAR(60),
    last_name VARCHAR(60)
);