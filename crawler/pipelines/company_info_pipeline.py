from models.postgre import Pg
from models.company_info import CompanyInfo
from models.industries import Industries
from models.market_types import MarketTypes
from models.countries import Countries


class CompanyInfoPipeline:

    def __init__(self):
        self.industries_dict = None
        self.market_types_dict = None
        self.countries_dict = None
        self.pg = None
        self.connection = None
        self.initial_attr()

    def process_item(self, item, spider):

        company_info = CompanyInfo(self.connection)

        if item['code'].isdigit():
            country_id = self.countries_dict.get('TW')
        else:
            country_id = self.countries_dict.get('US')

        company_info.set_data(
            code=item['code'],
            name=item['name'],
            market_type_id=self.market_types_dict.get(item['market_type']),
            industry_id=self.industries_dict.get(item['industry']),
            country_id=country_id
        )

        company_info.create()

        return item

    # def close_spider(self):
    #     self.pg.close_connect()

    def initial_attr(self):
        self.pg = Pg()
        self.connection = self.pg.connect(database_name='Stock')

        industries = Industries(self.connection)
        industries_list = industries.read()
        self.industries_dict = {industry: industry_id for industry_id, industry in industries_list}

        market_types = MarketTypes(self.connection)
        market_types_list = market_types.read()
        self.market_types_dict = {market_type: market_type_id for market_type_id, market_type in market_types_list}

        countries = Countries(self.connection)
        countries_list = countries.read()
        self.countries_dict = {country: country_id for country_id, country in countries_list}
