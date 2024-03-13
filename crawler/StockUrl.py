

class StockUrl():
    def __init__(self):
        self.stock_number = ''
    def GetDay(self, stock_number, date):
        return 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + date + '&stockNo=' + stock_number
