import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql

class BaseModel:
    def __init__(self):
        self.db_params = {
            "host": "localhost",
            "user": "postgres",
            "password": "password",
            "dbname": "postgres"
        }

        self.connect = None
        self.cursor = None

    def Connect(self, database_name='', isolation_level=None):

        if self.connect is not None and self.cursor is not None:
            return

        elif self.connect is not None and self.cursor is None:
            try:
                if isolation_level is None:
                    self.cursor = self.connect.cursor()

                else:
                    self.connect.set_isolation_level(isolation_level)
                    self.cursor = self.connect.cursor()

            except Exception as err:
                print("Error : ", err)
                self.connect = None
                self.cursor = None
                return

        try:
            if database_name == '':
                connect = psycopg2.connect(**self.db_params)
            else:
                self.db_params['dbname'] = database_name
                connect = psycopg2.connect(**self.db_params)

            self.connect = connect

            if isolation_level is None:
                self.cursor = connect.cursor()

            else:
                self.connect.set_isolation_level(isolation_level)
                self.cursor = connect.cursor()

        except Exception as err:
            print("Exception : ", err)
            self.connect = None
            self.cursor = None

    def CloseConnect(self):
        try:
            self.cursor.close()
            self.connect.close()

        except Exception as err:
            print('Exception : ', err)

        self.connect = None
        self.cursor = None

    def CheckPostgreStatus(self):

        self.Connect()

        if self.cursor is None:
            exit(1)

        self.cursor.execute('SELECT version()')

        version = self.cursor.fetchone()

        print('version: ', version)

        self.CloseConnect()


    def CreateDatabase(self, db_name):

        self.Connect(isolation_level=ISOLATION_LEVEL_AUTOCOMMIT)

        if self.cursor is None:
            exit(1)

        self.cursor.execute("SELECT 1 FROM pg_catalog.pg_database "
                            "WHERE datname = %s", (db_name,))

        exists = self.cursor.fetchone()

        if not exists:
            self.cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database {db_name} was created")
        else:
            print(f"Database {db_name} is exist")

        self.CloseConnect()

    def InitialDatabase(self):

        self.CreateDatabase('Stock')
