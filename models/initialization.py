from models.base_model import BaseModel


class Initialization(BaseModel):

    table_name = "initialization"

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.component = None
        self.is_init = None
        self.last_init = None

    def create_table(self):

        definition = """
            component VARCHAR(100) PRIMARY KEY,
            is_init BOOLEAN NOT NULL DEFAULT FALSE,
            last_init TIMESTAMP
        """

        super().table(definition)
