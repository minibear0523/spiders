# encoding=UTF-8
from bottle import run, route, get, post, request, response
from spiders.models import SpiderRule
from sqlalchemy import create_engine
from spiders.settings import DATABASE


@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=8090, debug=True)