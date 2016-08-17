# encoding=UTF-8
import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from .utils import form_index_settings
import pymongo

logger = logging.getLogger(__name__)


class SpiderClosedSyncExtension(object):
    """
    通过elasticsearch进行同步
    """
    Hosts = [{
        'host': '192.168.1.4',
        'port': 9200
    }]

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.es = Elasticsearch(hosts=self.Hosts)


    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("MYEXT_ENABLED"):
            raise NotConfigured
        ext = cls(crawler.settings.get('MONGO_URI'))
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        """
        在爬虫打开的时候, 检测是否已经存在index, 不存在则创建新的用于reindex的index.
        """
        logger.info("Spider has opened.")
        indices_client = self.es.indices
        index_name = spider.__getattribute__('db_name')
        if index_name:
            try:
                # 尝试获取对应index_name的index索引
                existed_mappings = indices_client.get_mapping(index=index_name)
            except NotFoundError:
                # 未找到对应的索引, 则创建索引
                logging.info('Not found index: %s.' % index_name)
                index_settings = form_index_settings()
                result = indices_client.create(index=index_name, body=index_settings)
                if result['acknowledged'] == 'true':
                    logging.info('Index created.')
                else:
                    logging.error('Index create failed, please create the index manually.')
            else:
                # 找到对应索引
                logging.info('Found index: %s' % index_name)
        else:
            logging.error('db_name not configured.')

    def spider_closed(self, spider):
        """
        在爬虫关闭的时候, 将已经储存在mongodb, 并通过mongo-connector同步到elasticsearch的数据进行reindex.
        """
        logger.info("Spider has closed.")