# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import pymongo


class DuplicatesPipeline(object):
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem('Duplicate Item URL: %s' % item['url'])
        else:
            self.urls_seen.add(item['url'])
            return item


class MongoPipeline(object):
    """
    将MONGO_DB和COLLECTION_NAME都放到spider中设置, 可以通过parse链接的方式自动设置.
    """
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[spider.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[spider.collection_name].insert(dict(item))
        return item