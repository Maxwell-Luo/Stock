
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.company_info_spider import CompanyInfoSpider

class Crawler:

    def start(self) -> None:
        settings = get_project_settings()
        process = CrawlerProcess(settings=settings)
        process.crawl(CompanyInfoSpider)

        process.start()

