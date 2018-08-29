# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WatchesItem(scrapy.Item):
    retailer = scrapy.Field()
    store_name = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    stock = scrapy.Field()
