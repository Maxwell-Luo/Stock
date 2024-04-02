import scrapy


class CompanyInfoItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    market_category = scrapy.Field()
    industry = scrapy.Field()
