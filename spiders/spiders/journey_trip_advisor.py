# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from spiders.items import JourneyItem
from spiders.utils import get_update_time
import re


class JourneyTripAdvisorSpider(Spider):
    name = "journey_trip_advisor"
    db_name = ""
    collection_name = ""
    start_urls = (
        'http://www.tripadvisor.cn/TourismBlog-g294232-Japan.html',
    )

    def parse(self, response):
        for href in response.xpath('//a[@class="title"]/@href').extract():
            url = response.urljoin(href)
            yield Request(url, self.parse_detail)

    def parse_detail(self, response):
        item = JourneyItem()
        item['url'] = response.url
        item['update_date'] = get_update_time()

        # 基本信息
        name = response.xpath('//div[@class="title-text"]/text()').extract()
        if name:
            item['name'] = ''.join(name).strip()
        author_link = response.xpath('//div[@class="strategy-info"]/a/@href').extract()
        if author_link:
            item['author_link'] = response.urljoin(''.join(author_link).strip())
        date_info = response.xpath('//div[@class="strategy-info"]/text()').extract()
        if date_info:
            date_info = ''.join(date_info).strip()
            regx = r'(\d{4}-\d{2}-\d{2})'
            pm = re.search(regx, date_info)
            if pm:
                item['department_date'] = pm.group(0)
            regx = r'\[(\d+)'
            pm = re.search(regx, date_info)
            if pm:
                item['duration'] = pm.group(1)