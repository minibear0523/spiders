# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from spiders.items import AttractionItem
from spiders.utils import get_update_time
import re


class AttractionTripAdvisorSpider(Spider):
    name = "attraction_trip_advisor"
    db_name = ""
    collection_name = "attraction"
    start_urls = [
        "http://www.tripadvisor.cn/Attractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html",
    ]

    def parse(self, response):
        self.logger.info('Attraction List Page URL: %s' % response.url)
        for href in response.xpath('//div[@class="property_title"]/a/@href').extract():
            url = response.urljoin(href)
            yield Request(url, self.parse_attraction)

        next_page = response.xpath('//div[contains(@class, "unified pagination")]/a/@href')
        if next_page:
            url = response.urljoin(next_page[-1].extract())
            yield Request(url, self.parse)

    def parse_attraction(self, response):
        self.logger.info('Attraction Detail URL: %s' % response.url)
        item = AttractionItem()
        # Settings相关
        item['source'] = 'TripAdvisor'
        itme['update_date'] = get_update_time()
        item['url'] = response.url

        # 基本信息
        item['name'] = ''.join(response.xpath('//h1[@id="HEADING"]/text()').extract()).strip()