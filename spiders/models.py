# encoding=UTF-8
"""
Topic:
Desc:
"""
from datetime import datetime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
# from spiders.settings import DATEBASE


Base = declarative_base()

class SpiderRule(Base):
    """自定义爬虫的爬取规则"""
    __tablename__ = 'spider_rule'

    id = Column(Integer, primary_key=True)
    # 规则名称
    name = Column(String(50))
    # 开始URL列表
    start_urls = Column(String(100))
    # 用来源标识不同的spider
    source_type = Column(String(30))
    # 标识不同的数据类型, 例如hotel, restaurant, attraction, shopping等
    data_type = Column(String(30))
    # crontab定时规则
    schedule = Column(String(200))
    # 规则是否生效
    enable = Column(Boolean, default=False)