from models.base_model import BaseModel


class DailyTransaction(BaseModel):

    table_name = "daily_transaction"

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.id = None
        self.code = None
        self.date = None
        self.volume = None
        self.amount = None
        self.opening_price = None
        self.high_price = None
        self.low_price = None
        self.closing_price = None
        self.price_change = None
        self.tx_count = None

    def create_table(self):

        definition = """
            id SERIAL PRIMARY KEY, 
            code VARCHAR(10),
            date DATE NOT NULL,
            volume BIGINT, 
            amount DECIMAL, 
            opening_price DECIMAL,
            high_price DECIMAL,
            low_price DECIMAL,
            closing_price DECIMAL,
            price_change DECIMAL,
            tx_count INT,
            FOREIGN KEY (code) REFERENCES company_info(code),
            UNIQUE (code, date)
        """

        super().table(definition)

