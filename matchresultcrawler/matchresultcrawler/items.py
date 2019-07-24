# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchresultcrawlerItem(scrapy.Item):
    date = scrapy.Field()
    week = scrapy.Field()
    season = scrapy.Field()
    league = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()
    home_score_first = scrapy.Field()
    away_score_first = scrapy.Field()
    home_score_final = scrapy.Field()
    away_score_final = scrapy.Field()