import scrapy


class CompanyInfoItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    market_type = scrapy.Field()
    industry = scrapy.Field()
