# -*- coding: utf-8 -*-
from scrapy import Item, Field


class HotelItem(Item):
    name = Field()  # 酒店名称
    name_en = Field()  # 酒店英文名称
    source = Field()  # 数据来源: TripAdvisor, Booking
    classes = Field()  # 酒店类型: 例如日式酒店, 豪华酒店
    address = Field()
    locality = Field()  # 地区
    geo_location = Field()  # 酒店坐标: "%lat, %lng"格式
    restaurant = Field()  # 酒店内部的餐饮
    price = Field()  # 价格区间
    network = Field()  # 提供的网络状况
    room_type = Field()  # 提供的房间类型
    activity = Field()  # 提供的活动设施
    service = Field()  # 酒店服务
    special = Field()  # 酒店特色
    review_stars = Field()  # TripAdvisor的评论星级
    review_qty = Field()  # TripAdvisor的评论数
    rank = Field()  # 酒店排名: n/total
    tags = Field()  # 酒店的标签
    stars = Field()  # 酒店星级
    award = Field()  # TripAdvisor的奖项
    url = Field()  # 爬取页面的链接
    update_date = Field()  # 数据更新日期


class RestaurantItem(Item):
    name = Field()
    source = Field()
    classes = Field()  # 菜系
    address = Field()
    geo_location = Field()
    telephone = Field()
    env = Field()  # 餐厅氛围
    open_time = Field()  # 营业时间
    offer_kind = Field()  # 提供的类型: 午餐, 晚餐
    special = Field()  # 餐厅特色
    price = Field()
    level = Field()  # 餐厅评级
    rank = Field()  # 餐厅排名: n/total
    review_stars = Field()  # 评论星级
    review_qty = Field()  # 评论数
    award = Field()  # 奖项
    url = Field()
    update_date = Field()


class AttractionItem(Item):
    name = Field()
    name_en = Field()
    source = Field()
    classes = Field()
    description = Field()
    suggested_duration = Field()  # 建议浏览时间
    address = Field()
    geo_location = Field()
    telephone = Field()
    open_time = Field()
    price = Field()
    rank = Field()
    review_stars = Field()
    review_qty = Field()
    award = Field()
    url = Field()
    update_date = Field()