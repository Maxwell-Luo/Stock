
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.company_info_spider import CompanyInfoSpider
from .spiders.daily_transaction_spider import DailyTransactionSpider


class Crawler:

    def start(self):
        settings = get_project_settings()
        process = CrawlerProcess(settings=settings)
        process.crawl(DailyTransactionSpider)

        process.start()

