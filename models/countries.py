from .base_model import BaseModel


class Countries(BaseModel):

    table_name = "countries"

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.id = None
        self.country = None

    def create_table(self):
        definition = """
            id SERIAL PRIMARY KEY,
            country CHAR(2) NOT NULL
        """

        super().table(definition)

    def initial(self):

        countries = ['TW', 'US']

        for country in countries:
            self.set_data(country=country)
            self.create()
