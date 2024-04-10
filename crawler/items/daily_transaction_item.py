import scrapy


class DailyTransactionItem(scrapy.Item):
    code = scrapy.Field()
    date = scrapy.Field()
    volume = scrapy.Field()
    amount = scrapy.Field()
    opening_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    closing_price = scrapy.Field()
    price_change = scrapy.Field()
    tx_count = scrapy.Field()
