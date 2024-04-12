from models.postgre import Pg


class Initialize:

    def __init__(self):
        self.databases_list = ["Stock"]
        self.pg = Pg()

    def __del__(self):
        self.pg.close_connect()

    def start(self):
        self.check_databases()

    def check_databases(self):
        self.pg.connect()
        template = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}'"

        for database in self.databases_list:
            command = template.format(database)
            result = self.pg.command(command)

            if not result:
                self.create_database(database)


    def check_tables(self):
        pass

    def create_database(self, database_name):
        template = "CREATE DATABASE {}"
        command = template.format(database_name)
        result = self.pg.command(command)
        print(result)


    def create_tables(self):
        pass

    def get_all_tables_name(self):
        pass
