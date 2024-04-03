from .base_model import BaseModel


class MarketTypes(BaseModel):

    table_name = "market_types"

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.id = None
        self.type = None

    def create_table(self):

        definition = """
            id SERIAL PRIMARY KEY,
            type VARCHAR(10) NOT NULL
        """

        super().table(definition)

    def initial(self):

        market_types = ['上市', '上櫃', 'S&P 500', 'NASDAQ', 'DJI', 'SOX']

        for market_type in market_types:

            self.set_data(type=market_type)
            self.create()
