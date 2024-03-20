import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from psycopg2.extensions import connection as Connection

class BaseModel:

    table_name = ""

    def __init__(self, db_connection: Connection):
        self.connection = db_connection

    def table(self, table_name, table_definition):

        try:
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {name} ({definition});").format(
                name=sql.Identifier(table_name),
                definition=sql.SQL(table_definition)
            )
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()

        except Exception as err:
            print(f'Exception : {err}')

    def create(self, data):

        columns = data.keys()
        values = tuple(data.values())

        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders}) RETURNING id;").format(
            table=sql.Identifier(self.table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.fetchone()[0]

    def read(self, conditions=None):

        where_clause = sql.SQL("WHERE {}").format(sql.SQL(' AND ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in conditions)
        ) if conditions else sql.SQL('')

        query = sql.SQL("SELECT * FROM {table} {where};").format(
            table=sql.Identifier(self.table_name),
            where=where_clause
        )
        with self.connection.cursor as cursor:
            cursor.execute(query, tuple(conditions.values()) if conditions else ())
            return cursor.fetchall()


    def update(self, conditions, data):
        set_clause = sql.SQL(', ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in data.keys()
        )

        where_clause = sql.SQL(' AND ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in conditions.keys()
        )

        query = sql.SQL("UPDATE {table} SET {set} WHERE {where};").format(
            table=sql.Identifier(self.table_name),
            set=set_clause,
            where=where_clause
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(data.values()) + tuple(conditions.values()))
            self.connection.commit()
            return cursor.rowcount

    def delete(self, conditions):
        where_clause = sql.SQL(' AND ').join(
            sql.Composed([sql.Identifier(key), sql.SQL('='), sql.Placeholder()]) for key in conditions.keys()
        )

        query = sql.SQL("DELETE FROM {table} WHERE {where};").format(
            table=sql.Identifier(self.table_name),
            where=where_clause
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(conditions.values()))
            self.connection.commit()
            return cursor.rowcount


