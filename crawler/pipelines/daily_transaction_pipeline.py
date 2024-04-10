from models.postgre import Pg
from models.daily_transaction import DailyTransaction
from scrapy.exceptions import DropItem


class DailyTransactionPipeline:

    def __init__(self):
        self.pg = Pg()
        self.connection = self.pg.connect('Stock')

    def process_item(self, item, spider):
        code = item['code']
        date = self.convert_to_gregorian(item['date'])

        if item['opening_price'] == "--":
            raise DropItem(f'{date} - {code} : No opening price')

        daily_transaction = DailyTransaction(self.connection)

        volume = item['volume'].replace(",", "")
        amount = item['amount'].replace(",", "")
        opening_price = item['opening_price'].replace(",", "")
        high_price = item['high_price'].replace(",", "")
        low_price = item['low_price'].replace(",", "")
        closing_price = item['closing_price'].replace(",", "")
        price_change = item['price_change'].replace("X", "").replace(",", "")
        tx_count = item['tx_count'].replace(",", "")

        daily_transaction.set_data(
            code=code,
            date=date,
            volume=volume,
            amount=amount,
            opening_price=opening_price,
            high_price=high_price,
            low_price=low_price,
            closing_price=closing_price,
            price_change=price_change,
            tx_count=tx_count
        )

        daily_transaction.create()

        return item

    def convert_to_gregorian(self, minguo_date):
        year, month, day = minguo_date.split('/')

        gregorian_year = int(year) + 1911

        return f"{gregorian_year}/{month}/{day}"

