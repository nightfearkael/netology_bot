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

        :param telegram_id:
        :return:
        """
        table = 'users'
        sql_command = f"SELECT id FROM {table} WHERE telegram_id=(%s)"
        self.cursor.execute(sql_command, (telegram_id, ))
        result = self.cursor.fetchone()
        return result

    def add_user(self, telegram_id, first_name, last_name):
        """

        :param telegram_id:
        :param first_name:
        :param last_name:
        :return:
        """
        table = 'users'
        sql_command = f"INSERT INTO {table}(telegram_id, first_name, last_name) VALUES ((%s), (%s), (%s))"
        self.cursor.execute(sql_command, (telegram_id, first_name, last_name))
        self.connection.commit()

    def check_admin(self, telegram_id):
        """

        :param telegram_id:
        :return:
        """
        table = 'admins'
        user_id = self.find_user(telegram_id)
        sql_command = f"SELECT id FROM {table} WHERE user_id=(%s)"
        self.cursor.execute(sql_command, (user_id[0], ))
        result = self.cursor.fetchone()
        return result

    def add_word(self, ru_word, en_word):
        table = 'words'
        sql_command = f"INSERT INTO {table} (ru_word, en_word) VALUES ((%s), (%s))"
        self.cursor.execute(sql_command, (ru_word, en_word, ))
        self.connection.commit()

    def find_word_id(self, ru_word):
        table = 'words'
        sql_command = f"SELECT id FROM {table} WHERE ru_word=(%s)"
        self.cursor.execute(sql_command, (ru_word, ))
        result = self.cursor.fetchone()
        return result

    def add_choices(self, word_id, choices):
        table = 'choices'
        sql_command = f'INSERT INTO {table} (word_id, choice1, choice2, choice3, choice4) VALUES ((%s), (%s), (%s), (%s), (%s))'
        self.cursor.execute(sql_command, (word_id, choices[0].strip(), choices[1].strip(), choices[2].strip(), choices[3].strip(), ))
        self.connection.commit()


    def __del__(self):
        """
        Нужно для завершения сессии подключения к СУБД
        :return: None
        """
        self.connection.close()



