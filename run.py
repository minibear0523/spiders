# encoding=UTF-8
"""
Topic: 爬虫运行函数
Desc: name, start_url, source_type, data_type, index_name, type_name, enable, schedule
"""
import logging, json, os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

Mapping = {
    'hotel': {
        'trip_advisor': 'HotelTripAdvisorSpider'
    },
    'restaurant': {
        'trip_advisor': 'RestaurantTripAdvisorSpider'
    },
    'attraction': {
        'trip_advisor': 'AttractionTripAdvisorSpider'
    }
}


def get_mapping_spider(data_type, source_type):
    return Mapping[data_type][source_type]


def get_spider_rules():
    file_name = 'spider_rules.json'
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'r+') as f:
        rules_str = f.read()
        rules = json.loads(rules_str)
        return rules


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings=settings)
    runner = CrawlerRunner(settings)
    spider_rules = get_spider_rules()
    for rule in spider_rules:
        data_type = rule['data_type']
        source_type = rule['source_type']
        runner.crawl(get_mapping_spider(data_type, source_type), start_url=rule['start_url'],
                     db_name=rule['index_name'])

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
    logging.info('All finished.')
