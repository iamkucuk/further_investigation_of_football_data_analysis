# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SofifaItem(scrapy.Item):
    name=scrapy.Field()
    date = scrapy.Field()
    basic=scrapy.Field()
    build_up_play=scrapy.Field()
    chance_creation=scrapy.Field()
    defence=scrapy.Field()
    special=scrapy.Field()

