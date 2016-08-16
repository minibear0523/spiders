# -*- coding: utf-8 -*-
import scrapy


class RestaurantTripAdvisorSpider(scrapy.Spider):
    name = "restaurant_trip_advisor"
    allowed_domains = ["tripadvisor.cn"]
    start_urls = (
        'http://www.tripadvisor.cn/',
    )

    def parse(self, response):
        pass
