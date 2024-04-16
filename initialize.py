from models.postgre import Pg
from utils.logger import Logger
import os
import importlib.util
from models.initialization import Initialization
from typing import List
import datetime


class Initialize:

    def __init__(self):
        self.databases_list = ["Stock"]
        self.pg = Pg()
        self.stock_connection = self.pg.connect('Stock')
        self.connection = self.pg.connect()
        self.init = Initialization(self.stock_connection)
        self.log = Logger('init').get_logger()

    def start(self):
        self.check_databases()
        self.check_initialization_table()
        self.check_all_tables()

    def check_databases(self):
        template = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}'"

        for database in self.databases_list:
            command = template.format(database)
            result = self.pg.command(command)

            if not result:
                self.create_database(database)

    def create_database(self, database_name: str):
        template = "CREATE DATABASE {}"
        command = template.format(database_name)
        result = self.pg.command(command)
        self.log.info(f'Create database : {database_name} result : {result}')

    def check_initialization_table(self):
        query = "SELECT EXISTS (SELECT * FROM information_schema.tables WHERE table_name='{}')".format("initialization")
        init_table_exist = self.pg.command(query)

        if not init_table_exist[0][0]:
            self.create_initialization_table()

    def create_initialization_table(self):
        all_tables_name = self.get_all_tables_name()

        self.init.create_table()

        for table_name in all_tables_name:
            self.init.set_data(component=table_name)
            self.init.create()

        self.init.clear_fields()
        self.init.set_data(is_init=True, last_init=datetime.datetime.now())
        self.init.set_conditions(component="initialization")
        self.init.update()

    def check_all_tables(self):
        all_tables_name = self.get_all_tables_name()

        self.init.set_fields("component")
        self.init.set_conditions(is_init=True)
        read_result = self.init.read()
        exclude_init_tables = [module[0] for module in read_result]

        need_init_tables = [table_name for table_name in all_tables_name if table_name not in set(exclude_init_tables)]
        need_init_tables = self.adjust_table_position(need_init_tables)
        self.create_all_tables(need_init_tables)

    def create_all_tables(self, tables_list: List):
        for table_name in tables_list:
            table_class = self.load_class(table_name)
            if table_class:
                instance = table_class(self.stock_connection)

                if hasattr(instance, 'create_table'):
                    instance.create_table()

                if hasattr(instance, 'initial'):
                    instance.initial()

                self.init.clear_fields()
                self.init.set_data(is_init=True, last_init=datetime.datetime.now())
                self.init.set_conditions(component=table_name)
                self.init.update()

    def get_all_tables_name(self) -> List[str]:

        exclude_words = ["__", "postgre", "base_model"]
        return [file[:-3] for file in os.listdir("models") if not any(word in file for word in exclude_words)]

    def load_class(self, module_name: str):
        try:
            module = importlib.import_module(f'models.{module_name}')
            class_name = self.convert_class_name(module_name)
            cls = getattr(module, class_name)
            return cls

        except ImportError as error:
            self.log.error(f"Module {module_name} not found. Exception: {error}")

        except AttributeError as error:
            self.log.error(f"Class {module_name} not found in {module_name}. Exception: {error}")

        return None

    def convert_class_name(self, name: str) -> str:
        return name.title().replace("_", "")

    # Because some tables use REFERENCES, the creation order must be adjusted
    def adjust_table_position(self, tables: List) -> List:
        order = ['company_info', 'daily_transaction']
        result = tables
        for element in order:
            if element in result:
                result.remove(element)
                result.append(element)

        return result

