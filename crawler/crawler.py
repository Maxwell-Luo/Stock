
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals

from .spiders.company_info_spider import CompanyInfoSpider
from .spiders.daily_transaction_spider import DailyTransactionSpider


class Crawler:

    def __init__(self):
        self.settings = get_project_settings()
        self.process = CrawlerProcess(settings=self.settings)

    def initial_for_table(self):
        company_info_spider = self.process.create_crawler(CompanyInfoSpider)
        company_info_spider.signals.connect(self.main_crawler, signal=signals.spider_closed)
        self.process.crawl(company_info_spider)

    def main_crawler(self):
        self.process.crawl(DailyTransactionSpider)

    def start(self):
        self.initial_for_table()
        self.process.start()
