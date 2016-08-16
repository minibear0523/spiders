# -*- coding: utf-8 -*-
import scrapy


class AttractionTripAdvisorSpider(scrapy.Spider):
    name = "attraction_trip_advisor"
    allowed_domains = ["tripadvisor.cn"]
    start_urls = (
        'http://www.tripadvisor.cn/',
    )

    def parse(self, response):
        pass
