import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


class Pg:
    def __init__(self):
        self.db_params = {
            "host": "localhost",
            "user": "postgres",
            "password": "password",
            "dbname": "postgres"
        }

        self.conn = None

    def connect(self, database_name='', isolation_level=None):

        if self.conn is not None:
            return self.conn

        try:
            if database_name == '':
                self.conn = psycopg2.connect(**self.db_params)
            else:
                self.db_params['dbname'] = database_name
                self.conn = psycopg2.connect(**self.db_params)

            if isolation_level is not None:
                self.conn.set_isolation_level(isolation_level)

        except Exception as err:
            print("Error : ", err)
            self.conn = None
            return self.conn

        return self.conn

    def close_connect(self):
        try:
            self.conn.close()

        except Exception as err:
            print('Exception : ', err)

        self.conn = None

    def command(self, query_str):
        with self.conn.cursor() as cursor:
            cursor.execute(query_str)
            return cursor.fetchall()

