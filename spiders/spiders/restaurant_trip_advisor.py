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
    
    def __init__(self, start_url, db_name):
        self.db_name = db_name
        self.start_urls = list(start_url)
        super(RestaurantTripAdvisorSpider, self).__init__()

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
        self.logger.info('Restaurant Detail URL: %s' % response.url)
        item = RestaurantItem()
        # Settings相关
        item['source'] = 'TripAdvisor'
        item['update_date'] = get_update_time()
        item['url'] = response.url

        # 餐厅名称
        item['name'] = ''.join(response.xpath('//h1[@id="HEADING"]/text()').extract()).strip()
        classes_xpath = response.xpath('//div[@class="detail separator"]/a/text()').extract()
        if classes_xpath:
            item['classes'] = map(lambda x: x.strip(), classes_xpath)
        else:
            self.logger.warning('[%s] has no classes: %s' % (item['name'], response.url))
        telephone = response.xpath('//div[@class="fl phoneNumber"]/text()').extract()
        if telephone:
            item['telephone'] = telephone[0].strip()
        else:
            self.logger.warning('[%s] has no telephone: %s' % (item['name'], response.url))
        # 基本信息
        level = []
        for bar in response.xpath('//div[@class="ratingRow wrap"]'):
            info = {}
            key = ''.join(bar.xpath('.//span[@class="text"]/text()').extract()).strip()
            value_xpath = ''.join(bar.xpath('.//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()).strip()
            regx = r'(\d[\.]?\d?)'
            pm = re.search(regx, value_xpath)
            if pm:
                value = pm.group(0)
                level.append({key: value})
            else:
                level.append({key: '无'})
        item['level'] = level
        # 地址
        address_lst = []
        locality = response.xpath('//span[@class="locality"]/text()').extract()
        if locality:
            address_lst.append(locality[0].strip())
        street_address = response.xpath('//span[@class="street-address"]').extract()
        if street_address:
            address_lst.append(street_address[0].strip())
        extended_address = response.xpath('//span[@class="extended-address"]/text()').extract()
        if extended_address:
            address_lst.append(extended_address[0].strip())
        postal_code = response.xpath('//span[@class="postal-code"]/text()').extract()
        if postal_code:
            address_lst.append(postal_code[0].strip())
        item['address'] = ', '.join(address_lst).strip()

        # 地理坐标
        lat = response.xpath('//div[@class="mapContainer"]/@data-lat').extract()
        lng = response.xpath('//div[@class="mapContainer"]/@data-lng').extract()
        item['geo_location'] = ','.join(lat+lng).strip()

        # 详细信息
        for row in response.xpath('//div[@class="row"]')[1:]:
            key = row.xpath('.//div[contains(@class, "title")]/text()').extract()[0].strip()
            value = row.xpath('.//div[contains(@class, "content")]/text()').extract()
            if key == u'参考价格':
                value = row.xpath('.//div[contains(@class, "content")]/span/text()').extract()
                if value:
                    item['price'] = ''.join(value).strip()
                else:
                    self.logger.warning('[%s] has no price: %s' % (item['name'], response.url))
            elif key == u'餐时':
                item['offer_kind'] = map(lambda x:x.strip(), value[0].split(','))
            elif key == u'餐厅特色':
                item['special'] = map(lambda x:x.strip(), value[0].split(','))
            elif key == u'氛围类别':
                item['env'] = map(lambda x:x.strip(), value[0].split(','))
            elif key == u'营业时间':
                open_time = []
                content_list = response.xpath('.//div[contains(@class, "content")]/div[@class="detail"]')
                for content in content_list:
                    info = {}
                    day = content.xpath('./span[@class="day"]/text()').extract()[0].strip()
                    hours = content.xpath('./span[@class="hours"]/div[@class="hoursRange"]/text()').extract()
                    open_time.append({day: map(lambda x:x.strip(), hours)})
                item['open_time'] = open_time

        # 排名信息
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
            pm = re.search(regx,total_xpath)
            if pm:
                total = pm.group(0)

            result_xpath = rank_xpath.xpath('./b[@class="rank_text wrap"]/span/text()').extract()
            regx = r'([\d+|,]+)'
            pm = re.search(regx, result_xpath[0])
            if pm:
                rank = pm.group(0)
            item['rank'] = '/'.join([rank, total])

        award = response.xpath('//a[starts-with(@href, "/TravelersChoice-Restaurants")]')
        if award:
            item['award'] = '2016年旅行者之选奖获得主'
        else:
            award = response.xpath('//span[@class="taLnk text"]/text()').extract()
            if award:
                item['award'] = ''.join(award).strip()

        yield item