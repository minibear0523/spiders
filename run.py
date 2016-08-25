# encoding=UTF-8
"""
Topic: 爬虫运行函数
Desc:
"""
import logging, json
from spiders.spiders import *
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from spiders.models import db_connect, create_rules_table, SpiderRule


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings=settings)
    engine = db_connect()
    create_rules_table(engine=engine)