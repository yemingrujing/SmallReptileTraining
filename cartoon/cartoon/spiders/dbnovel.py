# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector


# https://www.jianshu.com/p/7c1a084853d8
class DbnovelSpider(Spider):
    name = 'dbnovel'
    allowed_domains = ['www.qb5200.tw']
    start_urls = ['https://www.qb5200.tw/']

    def parse(self, response):
        sel = Selector(response)
        items = sel.xpath('//*[@class="item"]/div/dl')
        for item in items:
            print(item)
