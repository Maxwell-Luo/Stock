import datetime
import json
import scrapy
from ..items.daily_transaction_item import DailyTransactionItem
from models.postgre import Pg
from models.daily_transaction import DailyTransaction
from models.company_info import CompanyInfo
from scrapy import Request
from dateutil.relativedelta import relativedelta
from utils.logger import Logger
from typing import List


class DailyTransactionSpider(scrapy.Spider):

    name = 'daily_transaction'
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.daily_transaction_pipeline.DailyTransactionPipeline': 300,
        }
    }

    def __init__(self):
        super().__init__()
        self.pg = Pg()
        self.connection = self.pg.connect('Stock')
        self.daily_transaction = DailyTransaction(self.connection)
        self.codes = self.get_stock_codes()
        self.max_retry = 3

        self.log = Logger('crawler').get_logger()

    def start_requests(self):

        url_template = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={code}'

        for code in self.codes:
            dates = self.get_start_dates(code)
            for date in dates:
                url = url_template.format(date=date, code=code)
                self.log.info(f"Crawler fetching stock dates and codes : {date} - {code}")
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        result = json.loads(response.text)
        retry_count = response.meta.get('retry_count', 0)

        try:
            if result['stat'] != "OK":
                raise ValueError(result['stat'])

            item = DailyTransactionItem()

            item['code'] = result['title'].split(' ')[1]

            for data in result['data']:
                item['date'] = data[0]
                item['volume'] = data[1]
                item['amount'] = data[2]
                item['opening_price'] = data[3]
                item['high_price'] = data[4]
                item['low_price'] = data[5]
                item['closing_price'] = data[6]
                item['price_change'] = data[7]
                item['tx_count'] = data[8]
                yield item

        except Exception as err:
            self.resubmit_request(retry_count, response, err)

    def get_stock_codes(self):

        company_info = CompanyInfo(self.connection)
        company_info.set_fields('code')
        company_info.set_order('code')
        company_info.set_conditions(market_type_id='1')
        codes = company_info.read()
        return [code[0] for code in codes]

    def get_start_dates(self, code) -> List:

        self.daily_transaction.set_fields('date')
        self.daily_transaction.set_conditions(code=code)
        self.daily_transaction.set_order('date', 'DESC')
        self.daily_transaction.set_limit('1')

        result = self.daily_transaction.read()

        dates = []

        if result:
            current_date = result[0][0]
        else:
            start_date = "20120101"
            current_date = datetime.datetime.strptime(start_date, "%Y%m%d").date()

        today = datetime.date.today()

        while current_date < today:
            dates.append(current_date.strftime("%Y%m%d"))
            current_date = current_date + relativedelta(months=+1)

        return dates

    def resubmit_request(self, retry_count, response, err):

        if retry_count < self.max_retry:
            retry_count += 1
            self.log.warning(f'Resubmit the request({retry_count}): {response.url}. Error: {err}')
            yield Request(response.url, callback=self.parse, dont_filter=True, meta={'retry_count': retry_count})
        else:
            self.log.error(f'Failed to parse {response.url} after after several retries. Exception : {err}')
