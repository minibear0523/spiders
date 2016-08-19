# encoding=UTF-8
from bottle import run, route, get, post, request, response
from spiders.models import db_connect, SpiderRule, create_rules_table
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging


db = db_connect()
Session = sessionmaker(bind=db)

@contextmanager
def session_scoped(Session):
    """Provide a transactional scope around a series of operations"""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@get('/spider_rules')
def spider_rule_list():
    with session_scoped(Session) as session:
        results = session.query(SpiderRule).all()
        return results

@post('/spider_rule')
def create_or_update_spider_rule():
    name = request.json['name']
    start_urls = request.json['start_urls']
    source_type = request.json['source_type']
    data_type = request.json['data_type']
    schedule = request.json['schedule']
    index_name = request.json['index_name']
    type_name = request.json['type_name']
    enable = request.json['enable']
    # Insert a SpiderRule instance into database
    rule = SpiderRule(name=name, start_urls=start_urls, source_type=source_type,
                      data_type=data_type, schedule=schedule, index_name=index_name,
                      type_name=type_name, enable=enable)
    with session_scoped(Session) as session:
        session.add(rule)
        return str(rule.id)

@post('/create_all_database')
def create_all_database():
    result = create_rules_table(db)
    return result

run(host='localhost', port=8090, debug=True)