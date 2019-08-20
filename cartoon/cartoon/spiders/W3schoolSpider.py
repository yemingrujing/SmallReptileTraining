#!/usr/bin/python
# -*- coding:utf-8 -*-
# https://blog.csdn.net/u012150179/article/details/32911511
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import log
from cartoon.cartoon.items import W3schoolItem
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class W3schoolSpider(Spider):
    """爬取w3school标签"""
    # log.start("log",loglevel='INFO')
    name = "w3school"
    allowed_domains = ["w3school.com.cn"]
    start_urls = [
        "http://www.w3school.com.cn/xml/xml_syntax.asp"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="navsecond"]/div[@id="course"]/ul[1]/li')
        items = []

        for site in sites:
            item = W3schoolItem()

            title = site.xpath('a/text()').extract()
            link = site.xpath('a/@href').extract()
            desc = site.xpath('a/@title').extract()

            item['title'] = [t.encode('utf-8') for t in title]
            item['link'] = [l.encode('utf-8') for l in link]
            item['desc'] = [d.encode('utf-8') for d in desc]
            items.append(item)

            # 记录
            log.msg("Appending item...", level='INFO')

        log.msg("Append done.", level='INFO')
        return items
