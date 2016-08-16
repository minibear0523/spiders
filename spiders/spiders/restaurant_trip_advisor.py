# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from spiders.items import RestaurantItem
from spiders.utils import get_update_time
import re


class RestaurantTripAdvisorSpider(Spider):
    name = "restaurant_trip_advisor"
    db_name = ""
    collection_name = "restaurant"
    start_urls = [
        "http://www.tripadvisor.cn/Restaurants-g298184-Tokyo_Tokyo_Prefecture_Kanto.html"
    ]

    def parse(self, response):
        self.logger.info('Restaurant List Page URL: %s' % response.url)
        for href in response.xpath('//h3[@class="title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield Request(url, self.parse_restaurant)

        next_page = response.xpath('//div[@class="unified pagination js_pageLinks"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[-1].extract())
            yield Request(url, self.parse)

    def parse_restaurant(self, response):
        pass
