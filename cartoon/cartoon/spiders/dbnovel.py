# -*- coding: utf-8 -*-
import scrapy


class DbnovelSpider(scrapy.Spider):
    name = 'dbnovel'
    allowed_domains = ['www.qb5200.tw']
    start_urls = ['http://https://www.qb5200.tw/']

    def parse(self, response):
        pass
