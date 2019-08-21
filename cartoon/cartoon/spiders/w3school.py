# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import log
from ..items import W3schoolItem


class W3schoolSpider(Spider):
    name = 'w3school'
    allowed_domains = ['w3school.com.cn']
    start_urls = ['https://www.w3school.com.cn/xml/index.asp']

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
            log.msg("Appending item...", level=9)

        log.msg("Append done.", level=9)
        return items
