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

    def __del__(self):
        self.connection.close()
