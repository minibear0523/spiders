# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from spiders.items import HotelItem
from spiders.utils import get_update_time
import re


class HotelTripAdvisorSpider(Spider):
    name = "hotel_trip_advisor"
    db_name = ""
    collection_name = 'hotel'
    start_urls = [
        'http://www.tripadvisor.cn/',
    ]

    def parse(self, response):
        self.logger.info('Hotel List Page URL: %s' % response.url)
        for href in response.xpath('//div[@class="listing_title"]/a/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, self.parse_detail)

        next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[-1].extract())
            yield Request(url, self.parse)

    def parse_detail(self, response):
        self.logger.info('Hotel Detail Page URL: %s' % response.url)
        item = HotelItem()
        # settings相关
        item['source'] = 'TripAdvisor'
        item['update_date'] = get_update_time()
        item['url'] = response.url

        # 酒店名称
        item['name'] = ''.join(response.xpath('//h1[@id="HEADING"]/text()').extract()).strip()
        name_en = response.xpath('//h1[@id="HEADING"]/span[@class="altHead"]/text()')
        if name_en:
            item['name_en'] = ''.join(name_en.extract()).strip()
        else:
            self.logger.warning('[%s] has no English name: %s' % (item['name'], response.url))
        # 酒店类型
        classes_xpath = response.xpath('//div[contains(@class, "popRanking")]/a/text()').extract()
        if classes_xpath:
            item['classes'] = classes_xpath[0].split(' ')[0].split('/')
        else:
            self.logger.warning('[%s] has no classes: %s' % (item['name'], response.url))
        # 酒店地址
        address_list = []
        region = response.xpath('//span[@property="addressRegion"]/text()').extract()
        if region:
            address_list.append(''.join(region).strip())
        locality = response.xpath('//span[@property="addressLocality"]/text()').extract()
        if locality:
            address_list.append(''.join(locality).strip())
            item['locality'] = ''.join(locality).strip()
        street = response.xpath('//span[@property="streetAddress"]/text()').extract()
        if street:
            address_list.append(''.join(street).strip())
        postal_code = response.xpath('//span[@property="postalCode"]/text()').extract()
        if postal_code:
            address_list.append(''.join(postal_code).strip())
        item['address'] = ', '.join(address_list).strip()
        # 地理坐标
        lat = response.xpath('//div[@class="mapContainer"]/@data-lat').extract()
        lng = response.xpath('//div[@class="mapContainer"]/@data-lng').extract()
        if lat and lng:
            item['geo_location'] = ','.join(lat+lng)
        else:
            self.logger.warning('[%s] has no geo location: %s' % (item['name'], response.url))
        # 酒店内设施
        for amenity in response.xpath('//div[contains(@class, "amenity_row")]'):
            key = ''.join(amenity.xpath('./div[@class="amenity_hdr"]/text()').extract()).strip()
            value = amenity.xpath('./div[@class="amenity_lst"]/ul/li/text()').extract()
            if key == u'活动设施':
                activity_lst = []
                for activity in value:
                    if activity.strip():
                        activity_lst.append(activity.strip())
                item['activity'] = activity_lst

            elif key == u'客房类型':
                room_type = []
                for room in value:
                    if room.strip():
                        room_type.append(room.strip())
                item['room_type'] = room_type

            elif key == u'网络':
                network_lst = []
                for network in value:
                    if network.strip():
                        network_lst.append(network.strip())
                item['network'] = network_lst

            elif key == u'服务':
                service_lst = []
                for service in value:
                    if service.strip():
                        service_lst.append(service.strip())
                item['service'] = service_lst

            elif key == u'酒店餐饮':
                restaurant_lst = []
                value = amenity.xpath('.//div[contains(@class, "poi_card easyClear")]/div[@class="description_block"]')
                for restaurant in value:
                    info = {}
                    name = restaurant.xpath('./a[@class="poi_title"]/text()').extract()
                    if name:
                        info['name'] = ''.join(name).strip()
                    url = restaurant.xpath('./a[@class="poi_title"]/@href').extract()
                    if url:
                        info['url'] = response.urljoin(''.join(url).strip())
                    stars = restaurant.xpath('.//span[contains(@class, "rate sprite-rating_s rating_s")]/img/@alt').extract()
                    if stars:
                        regx = r'(\d)'
                        pm = re.search(regx, stars[0])
                        if pm:
                            info['review_stars'] = pm.group(0)
                    qty = restaurant.xpath('.//div[@class="rating"]/a/text()').extract()
                    if qty:
                        regx = r'([\d+|,]+)'
                        pm = re.search(regx, qty[0])
                        if pm:
                            info['review_qty'] = pm.group(0)
                    classes_xpath = restaurant.xpath('.//div[@class="detail_block"]/text()').extract()
                    if classes_xpath:
                        classes = classes_xpath[-1].strip().split(',')
                        info['classes'] = map(lambda x:x.strip(), classes)
                    restaurant_lst.append(info)
                item['restaurant'] = restaurant_lst
        # 价格区间
        price = response.xpath('//span[@property="priceRange"]/text()').extract()
        if price:
            try:
                item['price'] = price[0].strip().split(' ')[0][1:].replace(',','')
            except:
                self.logger('[%s: %s] price parser has wrong: %s' % (item['name'], response.url, price))
        # 酒店特色
        special_lst = []
        for special in response.xpath('//ul[@class="property_tags"]/li/text()').extract():
            if special.strip():
                special_lst.append(special.strip())
        item['special'] = special_lst
        # 评级信息
        review_stars = response.xpath('//img[@property="ratingValue"]/@content').extract()
        if review_stars:
            item['review_stars'] = review_stars[0]
        else:
            self.logger.warning('[%s] has no review stars: %s' % (item['name'], response.url))
        review_qty = response.xpath('//a[@property="reviewCount"]/@content').extract()
        if review_qty:
            item['review_qty'] = review_qty
        else:
            self.logger.warning('[%s] has no reviews: %s' % (item['name'], response.url))
        rank_xpath = response.xpath('//div[contains(@class, "popRanking")]/b[@class="rank"]/text()').extract()
        if rank_xpath:
            regx = r'(\d+)'
            pm = re.search(regx, rank_xpath[0].strip())
            rank = ""
            if pm:
                rank = pm.group(0)
                total_xpath = response.xpath('//div[starts-with(@class, "popRanking")]/a/text()').extract()
                if total_xpath:
                    pm = re.search(regx, total_xpath[0])
                    total = ""
                    if pm:
                        total = pm.group(0)
                        item['rank'] = '/'.join([rank, total])

        # 酒店星级和酒店标签
        stars = response.xpath(u'//img[@title="酒店星级"]/@alt').extract()
        if stars:
            regx = r'(\d\.\d)'
            pm = re.search(regx, stars[0])
            if pm:
                item['stars'] = pm.group(0)
        else:
            self.logger.warning('[%s] has no hotel stars: %s' % (item['name'], response.url))
        tags = []
        for tag in response.xpath('//span[@class="tag"]/text()').extract():
            if tag.strip():
                tags.append(tag)
        item['tags'] = tags

        # 奖项
        award = response.xpath('//a[starts-with(@href, "/TravelersChoice-Hotels")]')
        if award:
            item['award'] = '2016年旅行者之选奖得主'

        yield item
