# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import Noveltem


# https://www.jianshu.com/p/7c1a084853d8
class DbnovelSpider(Spider):
    name = 'dbnovel'
    custom_settings = {
        'ITEM_PIPELINES': {
            'cartoon.pipelines.DBNovelPipeline': 1,
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Accept-Language': "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Host": "www.qb5200.tw",
            "Referer": "https://www.qb5200.tw/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    }
    allowed_domains = ['www.qb5200.tw']
    start_urls = ['https://www.qb5200.tw/']

    def parse(self, response):
        sel = Selector(response)
        details = sel.xpath('//*[@class="item"]/div/dl')
        for detail in details:
            item = Noveltem()
            item['title'] = detail.xpath('dt/a/text()').extract_first()
            item['url'] = ''.join(["https://www.qb5200.tw", detail.xpath('dt/a/@href').extract_first().strip()])
            yield scrapy.Request(item['url'],  meta={'item': item}, callback=self.parse_profile)
            # item['profile'] = detail.xpath('dd/text()').extract_first().strip()\
            #     .replace(u'\u3000', u' ').replace(u'\xa0', u' ')

    def parse_profile(self, response):
        item = response.meta['item']
        sel = Selector(response)
        info = sel.xpath('//*[@class="info"]')
        item['profile'] = info.xpath('div[@class="intro"]/text()').extract_first().strip().replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['author'] = info.xpath('div[@class="small"]/span[1]/text()').extract_first().split("：")[-1]
        item['category'] = info.xpath('div[@class="small"]/span[2]/text()').extract_first().split("：")[-1]
        item['status'] = info.xpath('div[@class="small"]/span[3]/text()').extract_first().split("：")[-1]
        item['wordNum'] = info.xpath('div[@class="small"]/span[4]/text()').extract_first().split("：")[-1]
        item['updateTime'] = info.xpath('div[@class="small"]/span[5]/text()').extract_first().split("：")[-1]
        yield item
