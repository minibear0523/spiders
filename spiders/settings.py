# -*- coding: utf-8 -*-
import os

BOT_NAME = 'spiders'

SPIDER_MODULES = ['spiders.spiders']
NEWSPIDER_MODULE = 'spiders.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spiders.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'spiders.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# MYEXT_ENABLED = True
# EXTENSIONS = {
#    'spiders.extensions.SpiderClosedSyncExtension': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'spiders.pipelines.DuplicatesPipeline': 300,
    'spiders.pipelines.MongoPipeline': 500
}

# MongoDB Settings
MONGO_URI = 'mongodb://localhost:27017'

# Logger Settings
LOG_ENABLE = True
LOG_ENCODINGS = 'utf-8'
LOG_FORMAT = '[%(name)s: %(levelname)s] %(asctime)s: %(message)s'
LOG_DATEFORMAT = '%m-%d %H:%M:%S'
LOG_FILE = '/home/minibear/log/scrapy/spiders.log'

# PostgreSQL Settings
DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': 'localhost',
    'port': '5432',
    'username': 'dbuser',
    'password': '900523',
    'database': 'spiders'
}
# DATABASE = {
#     'drivername': 'postgresql+psycopg2',
#     'host': 'localhost',
#     'port': '5432',
#     'username': 'MiniBear0523',
#     'password': '900523',
#     'database': 'spiders'
# }
