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
        table = 'users'
        sql_command = f"SELECT id FROM {table} WHERE telegram_id=(%s)"
        self.cursor.execute(sql_command, (telegram_id, ))
        result = self.cursor.fetchone()
        return result

    def add_user(self, telegram_id, first_name, last_name):
        table = 'users'
        sql_command = f"INSERT INTO {table}(telegram_id, first_name, last_name) VALUES ((%s), (%s), (%s))"
        self.cursor.execute(sql_command, (telegram_id, first_name, last_name))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

