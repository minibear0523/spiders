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

    def __init__(self, start_url, db_name):
        self.db_name = db_name
        self.start_urls = list(start_url)
        super(AttractionTripAdvisorSpider, self).__init__()

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
        item['update_date'] = get_update_time()
        item['url'] = response.url

        # 基本信息
        item['name'] = ''.join(response.xpath('//h1[@id="HEADING"]/text()').extract()).strip()
        name_en = response.xpath('//span[@class="altHead"]/text()').extract()
        if name_en:
            item['name_en'] = name_en[0].strip()
        description = response.xpath('//div[@class="listing_details"]/p/text()').extract()
        if description:
            item['description'] = description[0].strip()
        else:
            self.logger.warning('[%s] has no description: %s' % (item['name'], response.url))
        classes = response.xpath('//div[@class="heading_details"]//div[@class="detail"]/a/text()').extract()
        if classes:
            item['classes'] = ''.join(classes).strip()
        else:
            self.logger.warning('[%s] has no classes: %s' % (item['name'], response.url))
        for detail in response.xpath('//div[@class="details_wrapper"]/div[@class="detail"]'):
            key = ''.join(detail.xpath('.//b/text()').extract()).strip()
            value = ''.join(detail.xpath('./text()').extract()).strip()
            if key == u'建议游览时间：':
                item['suggested_duration'] = value
            elif key == u'收费：':
                item['price'] = value
        address_lst = []
        region = response.xpath('//span[@property="addressRegion"]/text()').extract()
        if region:
            address_lst.append(region[0].strip())
        locality = response.xpath('//span[@property="addressLocality"]/text()').extract()
        if locality:
            address_lst.append(locality[0].strip())
        street = response.xpath('//span[@property="streetAddress"]/text()').extract()
        if street:
            address_lst.append(street[0].strip())
        postal_code = response.xpath('//span[@property="postalCode"]/text()').extract()
        if postal_code:
            address_lst.append(postal_code[0].strip())
        item['address'] = ', '.join(address_lst).strip()
        # 地理坐标
        lat = response.xpath('//div[@class="mapContainer"]/@data-lat').extract()
        lng = response.xpath('//div[@class="mapContainer"]/@data-lng').extract()
        item['geo_location'] = ','.join(lat + lng).strip()

        # 开放时间
        if response.xpath('//div[@id="HOUR_OVERLAY_CONTENTS"]'):
            days = ''.join(response.xpath('//span[@class="days"]/text()').extract()).strip()
            hours = ''.join(response.xpath('//span[@class="hours"]/text()').extract()).strip()
            item['open_time'] = [{days: hours}]

        # 排名
        review_stars = response.xpath('//img[@property="ratingValue"]/@content').extract()
        if review_stars:
            item['review_stars'] = ''.join(review_stars).strip()
        else:
            self.logger.warning('[%s] has no review stars: %s' % (item['name'], response.url))
        review_qty = response.xpath('//a[@property="reviewCount"]/@content').extract()
        if review_qty:
            item['review_qty'] = ''.join(review_qty).strip()
        else:
            self.logger.warning('[%s] has no review qty: %s' % (item['name'], response.url))

        rank_xpath = response.xpath('//div[@class="slim_ranking"]')
        if rank_xpath:
            total = ""
            rank = ""

            total_xpath = ''.join(rank_xpath.xpath('./text()').extract()).strip()
            regx = r'([\d+|,]+)'
            pm = re.search(regx, total_xpath)
            if pm:
                total = pm.group(0)

            result_xpath = rank_xpath.xpath('./b[@class="rank_text wrap"]/span/text()').extract()
            regx = r'([\d+|,]+)'
            pm = re.search(regx, result_xpath[0])
            if pm:
                rank = pm.group(0)
            item['rank'] = '/'.join([rank, total])

        award = response.xpath('//a[starts-with(@href, "/TravelersChoice-Landmarks")]')
        if award:
            item['award'] = '2016年旅行者之选奖获得主'
        else:
            award = response.xpath('//span[@class="taLnk text"]/text()').extract()
            if award:
                item['award'] = ''.join(award).strip()

        yield item