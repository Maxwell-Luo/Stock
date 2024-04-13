import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection
from utils.logger import Logger
from typing import Dict, List, Tuple, Any, Union
from psycopg2 import Error


class BaseModel:

    table_name = ""

    def __init__(self, db_connection: connection):
        self.connection = db_connection
        self.data = None
        self.conditions = None
        self.fields = None
        self.order_by = None
        self.order_direction = 'ASC'
        self.returning_fields = None
        self.limit = None
        # clause
        self.set_clause = None
        self.where_clause = None
        self.fields_clause = None
        self.order_by_clause = None
        self.returning_clause = None
        self.limit_clause = None
        # logger
        self.logger = Logger('model').get_logger()

        # When setting up data, exclude the attribute of BaseModel itself
        self.exclude_attr = ("connection",
                             "data",
                             "conditions",
                             "fields",
                             "order_by",
                             "order_direction",
                             "returning_fields",
                             "limit",
                             "set_clause",
                             "where_clause",
                             "fields_clause",
                             "order_by_clause",
                             "returning_clause",
                             "limit_clause",
                             "exclude_attr",
                             "logger")

    def table(self, table_definition: str) -> Union[List[Tuple[Any, ...]], None]:

        try:
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {name} ({definition});").format(
                name=sql.Identifier(self.table_name),
                definition=sql.SQL(table_definition)
            )

            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                return cursor.fetchall()

        except psycopg2.Error as error:
            return self.handle_postgres_error(error)

        except Exception as error:
            return self.handle_exception_error(error)

    def delete_table(self) -> Union[List[Tuple[Any, ...]], None]:

        try:
            query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(self.table_name))

            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                return cursor.fetchall()

        except psycopg2.Error as error:
            return self.handle_postgres_error(error)

        except Exception as error:
            return self.handle_exception_error(error)

    def set_data(self, **kwargs) -> Dict:
        for key, value in kwargs.items():
            setattr(self, self._check_attribute(key), value)

        self.data = {key: value for key, value in self.__dict__.items()
                     if value is not None and key not in self.exclude_attr}

        return self.data

    def set_conditions(self, **kwargs) -> Dict:

        self.conditions = {}

        for key, value in kwargs.items():
            self.conditions[self._check_attribute(key)] = value

        return self.conditions

    def set_fields(self, *args) -> List:

        self.fields = []

        for arg in args:
            self.fields.append(self._check_attribute(arg))

        return self.fields

    def set_order(self, field: str, direction=None) -> str:

        self.order_by = self._check_attribute(field)

        if direction:
            self.order_direction = direction

        return self.order_by

    def set_returning(self, fields: List) -> List:

        self.returning_fields = []

        for field in fields:
            self.returning_fields.append(self._check_attribute(field))

        return self.returning_fields

    def set_limit(self, limit: str) -> str:

        self.limit = limit
        return self.limit

    def create(self) -> Union[int, None]:

        columns = self.data.keys()
        values = tuple(self.data.values())

        self._generate_clause()

        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders}) {returning};").format(
            table=sql.Identifier(self.table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values)),
            returning=self.returning_clause
        )

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
                return cursor.rowcount

        except psycopg2.Error as error:
            return self.handle_postgres_error(error)

        except Exception as error:
            return self.handle_exception_error(error)

    def read(self) -> Union[List[Tuple[Any, ...]], None]:

        self._generate_clause()

        query = sql.SQL("SELECT {fields} FROM {table} {where} {order_by} {limit};").format(
            fields=self.fields_clause,
            table=sql.Identifier(self.table_name),
            where=self.where_clause,
            order_by=self.order_by_clause,
            limit=self.limit_clause
        )

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, tuple(self.conditions.values()) if self.conditions else ())
                return cursor.fetchall()

        except psycopg2.Error as error:
            return self.handle_postgres_error(error)

        except Exception as error:
            return self.handle_exception_error(error)

    def update(self) -> Union[int, None]:

        self._generate_clause()

        query = sql.SQL("UPDATE {table} SET {set} {where} {returning};").format(
            table=sql.Identifier(self.table_name),
            set=self.set_clause,
            where=self.where_clause,
            returning=self.returning_clause
        )
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, tuple(self.data.values()) + tuple(self.conditions.values()))
                self.connection.commit()
                return cursor.rowcount

        except psycopg2.Error as error:
            return self.handle_postgres_error(error)

        except Exception as error:
            return self.handle_exception_error(error)

    def delete(self) -> Union[int, None]:

        self._generate_clause()

        query = sql.SQL("DELETE FROM {table} {where} {returning};").format(
            table=sql.Identifier(self.table_name),
            where=self.where_clause,
            returning=self.returning_clause
        )

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, tuple(self.conditions.values()))
                self.connection.commit()
                return cursor.rowcount

        except psycopg2.Error as error:
            return self.handle_postgres_error(error)

        except Exception as error:
            return self.handle_exception_error(error)

    def _check_attribute(self, attr):
        if hasattr(self, attr):
            return attr
        else:
            raise AttributeError(f'{attr} is not valid attributes of {type(self).__name__}')

    def _generate_clause(self):

        self.set_clause = sql.SQL(', ').join(
            sql.Composed(
                [sql.Identifier(key), sql.SQL('='), sql.Placeholder()]
            ) for key in self.data.keys()
        ) if self.data else sql.SQL('')

        self.where_clause = sql.SQL("WHERE {}").format(
            sql.SQL(' AND ').join(
                sql.Composed(
                    [sql.Identifier(key), sql.SQL('='), sql.Placeholder()]
                ) for key in self.conditions)
        ) if self.conditions else sql.SQL('')

        self.fields_clause = sql.SQL(', ').join(
            map(sql.Identifier, self.fields)
        ) if self.fields else sql.SQL('*')

        self.order_by_clause = sql.SQL("ORDER BY {order_by} {order_direction}").format(
            order_by=sql.Identifier(self.order_by),
            order_direction=sql.SQL(self.order_direction)
        ) if self.order_by else sql.SQL('')

        self.returning_clause = sql.SQL("RETURNING {}").format(
            sql.SQL(', ').join(map(sql.Identifier, self.returning_fields))
        ) if self.returning_fields else sql.SQL('')

        self.limit_clause = sql.SQL("LIMIT {limit}").format(
            limit=sql.SQL(self.limit)
        ) if self.limit else sql.SQL("")

    def handle_postgres_error(self, error: Error) -> None:

        if error.pgcode == "23505":
            self.logger.warning(f"{error.pgcode} : {error}")
        else:
            self.logger.error(f"{error.pgcode} : {error}")

        self.connection.rollback()
        return None

    def handle_exception_error(self, error: Exception) -> None:
        self.logger.error(f"{error}")
        self.connection.rollback()
        return None
