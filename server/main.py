# encoding=UTF-8
from bottle import route, run, template, Bottle


app = Bottle()




run(app=app, host='localhost', port=8090, debug=True)