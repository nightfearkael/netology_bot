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

CREATE TABLE IF NOT EXISTS admins (
	id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    ru_word VARCHAR(60),
    en_word VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS choices (
    word_id INTEGER NOT NULL REFERENCES words(id),
    choice1 VARCHAR(60),
    choice2 VARCHAR(60),
    choice3 VARCHAR(60),
    choice4 VARCHAR(60)
);