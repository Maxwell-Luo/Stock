import psycopg2
from utils.logger import Logger
from typing import List, Tuple, Any, Union
from psycopg2.extensions import connection


class Pg:
    def __init__(self):
        self.db_params = {
            "host": "localhost",
            "user": "postgres",
            "password": "password",
            "dbname": "postgres"
        }

        self.conn = None
        self.logger = Logger('postgres').get_logger()

    def connect(self, database_name='', isolation_level=None) -> Union[connection, None]:

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

        except Exception as error:
            self.logger.error(error)
            self.conn = None
            return self.conn

        return self.conn

    def close_connect(self):
        try:
            self.conn.close()

        except Exception as error:
            self.logger.error(error)

        self.conn = None

    def command(self, query_str: str) -> Union[List[Tuple[Any, ...]], None, int]:

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query_str)
                if cursor.rowcount:
                    return cursor.fetchall()
                else:
                    return None

        except Exception as error:
            self.conn.rollback()
            self.logger.error(error)
            return None

