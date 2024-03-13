import urllib.request
from StockUrl import StockUrl
import json

class WebCrawler():
    def __init__(self, stock_number):
        self.stock_number = stock_number

    # 獲取每月的每日交易狀況
    def GetStockDayData(self, date):

        stock_url = StockUrl()
        url = stock_url.GetDay(self.stock_number, date)
        try:
            response = urllib.request.urlopen(url)

        except:
            print("Unable to get stock day data")
            return ""

        return response.read().decode('utf-8')

    # 逐一解析每日交易欄位數值
    def ParseStockDayData(self, json_data):

        try:
            data = json.loads(json_data)

        except:
            print("Unable to parse json data")
            return

        stat = data["stat"]
        print("狀態 : " + stat)
        if 'OK' != stat:
            print('json data is error data, stat : ', stat)
            return

        title = data['title']
        print('Company : ' , title.split(' ', 2)[2].split(' ', 1)[0])

        print("Date : " + data["date"])

        print("欄位 : ")
        for field in data['fields']:
            print(field, end='\t')


        print('\n')
        for date_date in data['data']:
            for field_data in date_date:
                print(field_data, end='\t')
            print('\n')
