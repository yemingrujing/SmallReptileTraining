# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class W3schoolItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    link = Field()
    desc = Field()

class Noveltem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    url = Field
    content = Field()
