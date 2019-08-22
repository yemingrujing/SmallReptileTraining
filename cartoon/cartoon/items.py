# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class W3schoolItem(Item):
    title = Field()
    link = Field()
    desc = Field()


class Noveltem(Item):
    collection = table = 'recommend'
    title = Field()
    url = Field()
    profile = Field()
    author = Field()
    category = Field()
    status = Field()
    wordNum = Field()
    updateTime = Field()
