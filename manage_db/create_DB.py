import psycopg2
from config import db_host, db_port, db_database, db_user, db_password

connector = psycopg2.connect(host=db_host,
                             database=db_database,
                             port=db_port,
                             user=db_user,
                             password=db_password)

cursor = connector.cursor()

commands = [
'''CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	telegram_id INTEGER NOT NULL,
    first_name VARCHAR(60),
    last_name VARCHAR(60)
);''',
'''CREATE TABLE IF NOT EXISTS admins (
	id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id)
);''',
    '''CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    ru_word VARCHAR(60),
    en_word VARCHAR(60)
);''',
'''CREATE TABLE IF NOT EXISTS choices (
    word_id INTEGER NOT NULL REFERENCES words(id),
    choice1 VARCHAR(60),
    choice2 VARCHAR(60),
    choice3 VARCHAR(60),
    choice4 VARCHAR(60)
);''',
'''CREATE TABLE IF NOT EXISTS user_words (
	user_id INTEGER REFERENCES users(id),
	word_id INTEGER REFERENCES words(id),
	CONSTRAINT user_w PRIMARY KEY (user_id, word_id)
);''', ]


for command in commands:
    cursor.execute(command)
    connector.commit()
