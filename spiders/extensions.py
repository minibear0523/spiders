# encoding=UTF-8
import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from elasticsearch import Elasticsearch


logger = logging.getLogger(__name__)


class SpiderClosedSyncExtension(object):
