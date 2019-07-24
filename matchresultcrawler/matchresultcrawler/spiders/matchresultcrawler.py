# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule as rule
from matchresultcrawler.items import MatchresultcrawlerItem
from scrapy.linkextractors import LinkExtractor
import re
from bs4 import BeautifulSoup
import requests

class StatscrawlerSpider(CrawlSpider):
    name = 'matchresultcrawler'
    allowed_domains = ['worldfootball.net']
    base_url = "https://www.worldfootball.net/"

    league_url_names = ["eng-premier-league",
                        "bel-eerste-klasse-a",
                        "fra-ligue-1",
                        "bundesliga",
                        "ita-serie-a",
                        "ned-eredivisie",
                        "pol-ekstraklasa",
                        "por-primeira-liga",
                        "sco-premiership",
                        "esp-primera-division",
                        "sui-super-league"]

    links = []
    for league in league_url_names:
        links.append(base_url + "schedule/" + league)

    start_urls = links
    # rules = (
    #     rule(LinkExtractor(restrict_css=(".luecke+ td a")), follow=True, callback="parse"), # for weeks
    #     rule(LinkExtractor(restrict_css=(".with-border td:nth-child(1) a")), follow=True, callback="parse"),
    # )

    def parse(self, response):
        table_list = []
        res = response.css("div.data > table.standard_tabelle")[0].css("tr")
        date_selector = ""
        for i, row_selector in enumerate(res):
            row_list = []
            for i, col_selector in enumerate(row_selector.css("td")):
                if i == 3:
                    continue
                elif i == 0:
                    if not col_selector.css("td::text"):
                        col_selector = date_selector
                    else:
                        col_selector = col_selector.css("td::text")
                        date_selector = col_selector
                elif i == 1:
                    col_selector = col_selector.css("td::text")
                elif i < 6:
                    col_selector = col_selector.css("td > a::text")
                else:
                    continue
                row_list.append(col_selector.get())
            table_list.append(row_list)

        time_text = response.css("div#navi > div.breadcrumb > h1::text").get()

        re1='.*?'	# Non-greedy match on filler
        re2='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'	# Year 1
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(time_text)
        season = 2000
        if m:
            season=int(m.group(1))
        if season < 2005:
            return

        week = time_text[time_text.index("»", time_text.index(str(season))) + 2 : -7]
        league = time_text[: time_text.index(str(season)) - 1].replace("» ", "")
        date = ""
        
        re1='(\\d+)'	# Integer Number 1
        re2='.*?'	# Non-greedy match on filler
        re3='(\\d+)'	# Integer Number 2
        re4='.*?'	# Non-greedy match on filler
        re5='(\\d+)'	# Integer Number 3
        re6='.*?'	# Non-greedy match on filler
        re7='(\\d+)'	# Integer Number 4
        rg = re.compile(re1+re2+re3+re4+re5+re6+re7,re.IGNORECASE|re.DOTALL)

        for temp_list in table_list:
            print(temp_list)
            item = MatchresultcrawlerItem()
            item["week"] = int(week)
            item["season"] = season
            item["league"] = league
            if temp_list[0] != "\u00a0":
                date = temp_list[0]
            item["date"] = date
            item["home_team"] = temp_list[2]
            item["away_team"] = temp_list[3]

            m = rg.search(temp_list[4])
            if m:
                int1=m.group(1)
                int2=m.group(2)
                int3=m.group(3)
                int4=m.group(4)
                
                item["home_score_first"] = int3
                item["away_score_first"] = int4
                    
                item["home_score_final"] = int1
                item["away_score_final"] = int2
            yield item

        seasonPageButton = response.css(".with-border td:nth-child(1) a")
        weekPageButton = response.css(".luecke+ td a")
        base_url = "https://www.worldfootball.net/"

        if weekPageButton:
            yield scrapy.Request(base_url + weekPageButton.css("a::attr(href)").get(),callback=self.parse)
        else:
            yield scrapy.Request(base_url + seasonPageButton.css("a::attr(href)").get(),callback=self.parse)