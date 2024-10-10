import psycopg2
from config import db_host, db_port, db_database, db_user, db_password


class Postgre:
    def __init__(self):
        self.db_host = db_host
        self.db_port = db_port
        self.database = db_database
        self.user = db_user
        self.password = db_password
        self.connection = psycopg2.connect(host=self.db_host,
                                           database=self.database,
                                           port=self.db_port,
                                           user=self.user,
                                           password=self.password)
        self.cursor = self.connection.cursor()

    def find_user(self, telegram_id):
        """
        Поиск пользователя в базе по Telegram ID
        :param telegram_id: Telegram ID
        :return: tuple, or None
        """
        table = 'users'
        sql_command = f"SELECT id FROM {table} WHERE telegram_id=(%s)"
        self.cursor.execute(sql_command, (telegram_id, ))
        result = self.cursor.fetchone()
        return result

    def add_user(self, telegram_id, first_name, last_name):
        """
        Добавление пользователя в БД при регистрации
        :param telegram_id: Telegram ID пользователя (из сообщения)
        :param first_name: Имя пользователя (из сообщения)
        :param last_name: Фамилия пользователя (из сообщения)
        :return: None
        """
        table = 'users'
        sql_command = f"INSERT INTO {table}(telegram_id, first_name, last_name) VALUES ((%s), (%s), (%s))"
        self.cursor.execute(sql_command, (telegram_id, first_name, last_name))
        self.connection.commit()

    def add_word(self, ru_word, en_word):
        """
        Добавление нового слова в словарь в таблицу words
        :param ru_word: Русский вариант
        :param en_word: Перевод на английский (переводчиком)
        :return: None
        """
        table = 'words'
        sql_command = f"INSERT INTO {table} (ru_word, en_word) VALUES ((%s), (%s))"
        self.cursor.execute(sql_command, (ru_word, en_word, ))
        self.connection.commit()

    def find_word_id(self, ru_word):
        """
        Поиск id слова по его русскому переводу
        :param ru_word: Русский вариант
        :return: None, если нет, tuple вида (id, ) при успехе
        """
        table = 'words'
        sql_command = f"SELECT id FROM {table} WHERE ru_word=(%s)"
        self.cursor.execute(sql_command, (ru_word, ))
        result = self.cursor.fetchone()
        return result

    def add_choices(self, word_id, choices):
        """
        Добавление вариантов перевода к слову
        :param word_id: ID слова в таблице words
        :param choices: список из 4 вариантов
        :return: None
        """
        table = 'choices'
        sql_command = f'INSERT INTO {table} (word_id, choice1, choice2, choice3, choice4) VALUES ((%s), (%s), (%s), (%s), (%s))'
        self.cursor.execute(sql_command, (word_id, choices[0].strip(), choices[1].strip(), choices[2].strip(), choices[3].strip(), ))
        self.connection.commit()

    def select_random_word(self):
        """
        Запрос случайного слова из таблицы words (основной функционал)
        :return: Список [русское слово, английское слово, [список из 4 вариантов ответа]]
        """
        sql_command = 'SELECT * FROM words ORDER BY RANDOM() LIMIT 1'
        self.cursor.execute(sql_command)
        word = self.cursor.fetchone()
        sql_command = 'SELECT choice1, choice2, choice3, choice4 FROM choices WHERE word_id=(%s)'
        self.cursor.execute(sql_command, (word[0], ))
        choices = self.cursor.fetchone()
        word_list = [word[1], word[2], list(choices)]
        return word_list

    def add_word_to_user(self, telegram_id, ru_word):
        """
        Добавляет строку в таблицу user_words с ID пользователя и ID слова (если пара уже существует - игнорирует)
        :param telegram_id: Telegram ID пользователя (из сообщения)
        :param ru_word: Русское слово
        :return: None
        """
        sql_command = '''WITH user_id AS (
    SELECT id FROM users WHERE telegram_id = (%s)
),
word_id AS (
    SELECT id FROM words WHERE ru_word = (%s)
)
INSERT INTO user_words (user_id, word_id)
SELECT u.id, w.id
FROM user_id u, word_id w
WHERE u.id IS NOT NULL AND w.id IS NOT NULL
ON CONFLICT (user_id, word_id) DO NOTHING;'''
        self.cursor.execute(sql_command, (telegram_id, ru_word, ))
        self.connection.commit()

    def del_word_from_user(self, telegram_id, ru_word):
        """
        Удаляет строку из таблицы user_words с ID пользователя и ID слова (если пары уже не существует - игнорирует)
        :param telegram_id: Telegram ID пользователя (из сообщения)
        :param ru_word: Русское слово
        :return: None
        """
        sql_command = '''WITH user_id AS (
    SELECT id FROM users WHERE telegram_id = (%s)
),
word_id AS (
    SELECT id FROM words WHERE ru_word = (%s)
)
DELETE FROM user_words
WHERE user_id IN (SELECT id FROM user_id) AND word_id IN (SELECT id FROM word_id);'''
        self.cursor.execute(sql_command, (telegram_id, ru_word, ))
        self.connection.commit()

    def count_words(self, telegram_id):
        """
        Считает количество изучаемых слов конкретным пользователем
        :param telegram_id: Telegram ID пользователя (из сообщения)
        :return: tuple (amount, ) или None
        """
        sql_command = '''SELECT COUNT(*)
FROM user_words uw
JOIN users u ON uw.user_id = u.id
WHERE u.telegram_id = (%s)'''
        self.cursor.execute(sql_command, (telegram_id, ))
        result = self.cursor.fetchone()
        return result

    def __del__(self):
        """
        Нужно для завершения сессии подключения к СУБД
        :return: None
        """
        self.connection.close()
