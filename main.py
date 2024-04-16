#!/usr/bin/python
# -*- coding: utf-8 -*-

from crawler.crawler import Crawler
from initialize import Initialize

init = Initialize()
init.start()
crawler = Crawler()
crawler.start()
