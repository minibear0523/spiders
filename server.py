# encoding=UTF-8
from bottle import run, route, get, post, request, response, app
from beaker.middleware import SessionMiddleware
from spiders.models import db_connect, SpiderRule, create_rules_table
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from cork import Cork
import logging
import json

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('bottle_cork_conf', email_sender='lei.zhang.bupt08@gmail.com', smtp_url='smtp://smtp.magnet.ie')

# alias the authorization decorator with defaults
authorize = aaa.make_auth_decorator(fail_redirect="/login", role="user")

app = app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'diy_travel_session_key!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)


db = db_connect()
Session = sessionmaker(bind=db)

def post_get(name, default=''):
    return request.json.get(name, default)

@post('/api/users/register')
def register():
    """Register a new user"""
    username = post_get('username')
    password = post_get('password')
    email_address = post_get('email_address')
    print 'username: %s\n password: %s\n email_address: %s' % (username, password, email_address)
    aaa.register(username, password, email_address)
    return "check your email"

@get('/api/users/validate_registration/:registration_code')
def validate_registration(registration_code):
    """validate registration code"""
    aaa.validate_registration(registration_code)
    return 'Thanks'

@post('/api/users/login')
def login():
    username = post_get('username')
    password = post_get('password')
    print username, password
    result = aaa.login(username, password)
    print result


@route('/api/users/logout')
def logout():
    aaa.logout(success_redirect='/', fail_redirect='/error')

@post('/api/users/create')
def create_user():
    username = post_get('name')
    password = post_get('password')
    role = post_get('role')
    try:
        aaa.create_user(username, role, password)
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)

@post('/api/users/delete')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)

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
        spider_rule_lst = []
        for spider_rule in results:
            spider_rule_lst.append({
                'id': spider_rule.id,
                'name': spider_rule.name,
                'start_urls': spider_rule.start_urls,
                'source_type': spider_rule.source_type,
                'data_type': spider_rule.data_type,
                'schedule': spider_rule.schedule,
                'index_name': spider_rule.index_name,
                'type_name': spider_rule.type_name,
                'enable': spider_rule.enable
            })
        return json.dumps(spider_rule_lst)

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

def main():
    run(app, quiet=False, reloader=True, debug=True)

if __name__ == '__main__':
    main()