#!/usr/bin/python
# -*- coding: utf-8 -*-

from models.base_model import BaseModel
from models.postgre import Pg

pg = Pg()

pg.check_postgre_status()
pg.initial_database()
exit(1)
crawler = WebCrawler("2303")
day_data = crawler.GetStockDayData("20240301")

crawler.ParseStockDayData(day_data)