# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WorldfootballItem(scrapy.Item):
    date = scrapy.Field()
    week = scrapy.Field()
    season = scrapy.Field()
    league = scrapy.Field()
    team = scrapy.Field()
    ranking = scrapy.Field()
    win_count = scrapy.Field()
    draw_count = scrapy.Field()
    lose_count = scrapy.Field()
    goals_scored = scrapy.Field()
    goals_against = scrapy.Field()
    dif = scrapy.Field()
    points = scrapy.Field()
