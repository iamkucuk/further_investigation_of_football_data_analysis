import scrapy
from scrapy.spiders import CrawlSpider,Rule as rule
from sofifa.items import SofifaItem
from scrapy.linkextractors import LinkExtractor
import re

class SofifaSpider(CrawlSpider):
    name='sofifa.com'
    allowed_domains=['sofifa.com']
    start_urls=["https://sofifa.com/teams?type=all&lg%5B0%5D=4&lg%5B1%5D=13&lg%5B2%5D=16&lg%5B3%5D=19&lg%5B4%5D=31&lg"
                "%5B5%5D=10&lg%5B6%5D=66&lg%5B7%5D=308&lg%5B8%5D=50&lg%5B9%5D=53&lg%5B10%5D=189&version=%2Fteams"
                "%3Ftype%3Dall%26lg%255B0%255D%3D4%26lg%255B1%255D%3D13%26lg%255B2%255D%3D16%26lg%255B3%255D%3D19"
                "%26lg%255B4%255D%3D31%26lg%255B5%255D%3D10%26lg%255B6%255D%3D66%26lg%255B7%255D%3D308%26lg%255B8"
                "%255D%3D50%26lg%255B9%255D%3D53%26lg%255B10%255D%3D189%26v%3D19%26e%3D159453%26set%3Dtrue&showCol"
                "%5B0%5D=ti&showCol%5B1%5D=oa&showCol%5B2%5D=at&showCol%5B3%5D=md&showCol%5B4%5D=df&showCol%5B5%5D=tb"
                "&showCol%5B6%5D=bs&showCol%5B7%5D=bd&showCol%5B8%5D=bp&showCol%5B9%5D=bps&showCol%5B10%5D=cc&showCol"
                "%5B11%5D=cp&showCol%5B12%5D=cs&showCol%5B13%5D=cps&showCol%5B14%5D=da&showCol%5B15%5D=dm&showCol"
                "%5B16%5D=dw&showCol%5B17%5D=dd&showCol%5B18%5D=dp&showCol%5B19%5D=ip&showCol%5B20%5D=ps&showCol%5B21"
                "%5D=sa&showCol%5B22%5D=ta&v=19&e=159481&set=true&offset=0",]

    rules = (
        # rule(LinkExtractor(allow=(),restrict_css=(r'div#content-target > table.table > tbody')),callback="",follow=False),
        rule(LinkExtractor(allow=(), restrict_css=(r'div.pagination')), follow=True, callback="tableParser"),

    )

    def tableParser(self, response):
        date_string = response.css("title::text").get()[14:-7]
        team_list = []
        team_response = response.css('table > tbody > tr')
        for team_selector in team_response:
            row_list = []
            for col_selector in team_selector.css("td.col"):
                if "span" in col_selector.get():
                    col_selector = col_selector.css("span::text")
                else:
                    col_selector = col_selector.css("td.col::text")
                row_list.append(col_selector.get())
            team_list.append(row_list)


        for temp_list in team_list:
            item = SofifaItem()
            item["date"] = date_string
            item["basic"] = temp_list[:6]
            item["build_up_play"] = temp_list[6:10]
            item["chance_creation"] = temp_list[10:14]
            item["defence"] = temp_list[14:18]
            item["special"] = temp_list[18:]

            yield item

        acc_dates=response.css("#content-target > form > .sumo.redirect > optgroup ")
        addres="https://sofifa.com"
        for opt_selector in acc_dates:
            links=opt_selector.css("option::attr(value)").getall()
            for link in links:
                yield scrapy.Request(url=addres + link,callback=self.tableParser)






