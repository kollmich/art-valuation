# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VeritasItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price_estimate = scrapy.Field()
    session_date = scrapy.Field()
    price_hammer = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()
    pass
