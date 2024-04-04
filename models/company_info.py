from .base_model import BaseModel


class CompanyInfo(BaseModel):

    table_name = "company_info"

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.code = None
        self.name = None
        self.market_type_id = None
        self.industry_id = None
        self.country_id = None

    def create_table(self):

        definition = """
            code VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL, 
            market_type_id SMALLINT,
            industry_id SMALLINT,
            country_id SMALLINT NOT NULL,
            FOREIGN KEY (market_type_id) REFERENCES market_types(id),
            FOREIGN KEY (industry_id) REFERENCES industries(id),
            FOREIGN KEY (country_id) REFERENCES countries(id)
        """

        super().table(definition)
