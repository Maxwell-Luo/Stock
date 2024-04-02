import scrapy
from ..items.company_info_item import CompanyInfoItem


class CompanyInfoSpider(scrapy.Spider):

    listed_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    otc_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'

    name = 'company_info'
    start_urls = [listed_url, otc_url]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.company_info_pipeline.CompanyInfoPipeline': 300,
        }
    }
    # allowed_domains = ""

    def parse(self, response):

        stock_table = response.xpath("//tr[td[contains(., '股票')]]/following-sibling::tr")

        for info in stock_table:

            code_name = info.xpath('td[1]/text()').get()
            if code_name is None:
                continue

            code_name_list = code_name.split()
            code = code_name_list[0]
            name = code_name_list[1]
            market_category = info.xpath('td[4]/text()').get()
            industry = info.xpath('td[5]/text()').get()

            if industry is None:
                break

            item = CompanyInfoItem()
            item['code'] = code
            item['name'] = name
            item['market_category'] = market_category
            item['industry'] = industry
            yield item


