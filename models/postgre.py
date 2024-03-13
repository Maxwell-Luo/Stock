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

        self.connect = None
        self.cursor = None


    def CreateCompanyInfoTable(self):

        sql = '''
        CREATE TABLE IF NOT EXISTS company_info (
            company_code VARCHAR(10) PRIMARY KEY,
            company_name VARCHAR(10) NOT NULL
        );
        '''

        self.__Connect()

        if self.cursor is None:
            exit(1)


    def CreateDailyTransactionsTable(self):

        sql = '''
        CREATE TABLE IF NOT EXISTS daily_transactions (
            id SERIAL PRIMARY KEY, 
            company_code VARCHAR(10),
            date DATE NOT NULL,
            volume BIGINT, 
            amount DECIMAL, 
            opening_price DECIMAL,
            high_price DECIMAL,
            low_price DECIMAL,
            closing_price DECIMAL,
            price_change DECIMAL,
            tx_count INT,
            FOREIGN KEY (company_code) REFERENCES company_info(company_code)
        );
        '''
