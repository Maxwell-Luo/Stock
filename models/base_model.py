import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from psycopg2.extensions import connection as Connection


class BaseModel:

    table_name = ""

    def __init__(self, db_connection: Connection):
        self.connection = db_connection
        self.data = None
        self.conditions = None
        self.fields = None

    def table(self, table_definition):

        try:
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {name} ({definition});").format(
                name=sql.Identifier(self.table_name),
                definition=sql.SQL(table_definition)
            )

            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()

        except Exception as err:
            print(f'Exception : {err}')

    def delete_table(self):

        try:
            query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(self.table_name))

            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()

        except Exception as err:
            print(f'Exception : {err}')

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f'{key} is not valid attributes of {type(self).__name__}')

        self.data = {key: value for key, value in self.__dict__.items()
                     if value is not None and key not in ["connection", "data", "conditions"]}

        return self.data

    def set_conditions(self, **kwargs):

        self.conditions = {}

        for key, value in kwargs.items():
            if hasattr(self, key):
                self.conditions[key] = value
            else:
                raise AttributeError(f'{key} is not valid attributes of {type(self).__name__}')

        return self.conditions

    def set_fields(self, *args):

        self.fields = []

        for arg in args:
            if hasattr(self, arg):
                self.fields.append(arg)
            else:
                raise AttributeError(f'{arg} is not valid attributes of {type(self).__name__}')

        return self.fields

    def create(self):

        columns = self.data.keys()
        values = tuple(self.data.values())

        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders}) RETURNING id;").format(
            table=sql.Identifier(self.table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.fetchone()[0]

    def read(self):

        where_clause = sql.SQL("WHERE {}").format(sql.SQL(' AND ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in self.conditions)
        ) if self.conditions else sql.SQL('')

        if self.fields:
            fields_clause = sql.SQL(', ').join(map(sql.Identifier, self.fields))
        else:
            fields_clause = sql.SQL('*')

        query = sql.SQL("SELECT {fields} FROM {table} {where};").format(
            fields=fields_clause,
            table=sql.Identifier(self.table_name),
            where=where_clause
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(self.conditions.values()) if self.conditions else ())
            return cursor.fetchall()

    def update(self):
        set_clause = sql.SQL(', ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in self.data.keys()
        )

        where_clause = sql.SQL(' AND ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in self.conditions.keys()
        )

        query = sql.SQL("UPDATE {table} SET {set} WHERE {where};").format(
            table=sql.Identifier(self.table_name),
            set=set_clause,
            where=where_clause
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(self.data.values()) + tuple(self.conditions.values()))
            self.connection.commit()
            return cursor.rowcount

    def delete(self):
        where_clause = sql.SQL(' AND ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in self.conditions.keys()
        )

        query = sql.SQL("DELETE FROM {table} WHERE {where};").format(
            table=sql.Identifier(self.table_name),
            where=where_clause
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(self.conditions.values()))
            self.connection.commit()
            return cursor.rowcount


