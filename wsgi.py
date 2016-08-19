#!/usr/bin/env python
import os
from bottle import route, default_app, request, abort
import MySQLdb as mysql
import json

#app = bottle.Bottle()

@route('/')
def index():
    return '<strong>Hello World!</strong>'

@route('/env')
def env():
    response_body = ['%s: %s' % (key, value)
                for key, value in sorted(os.environ.items())]
    response_body = '\n'.join(response_body)
    response_body = response_body.encode('utf-8')
    return response_body


@route('/db')
def db():
    try:
        cnx = mysql.connect(user=os.environ["OPENSHIFT_MYSQL_DB_USERNAME"],
                            passwd=os.environ["OPENSHIFT_MYSQL_DB_PASSWORD"],
                            host=os.environ["OPENSHIFT_MYSQL_DB_HOST"],
                            port=int(os.environ["OPENSHIFT_MYSQL_DB_PORT"]),
                            db='biba')
    except BaseException as e:
        print(e)
    return "ok"


@route('/add_comment/:id', method='PUT')
def add_comment(id):
    print("adding comments %s" % id)
    #data = request.body.readline().decode('utf-8')
    data = request.json
    print(data)
    print("grrrreat")
    if not data:
        abort(400, 'No data received')
    if not 'comment' in data:
        abort(400, 'No comment included')
    try:
        db['documents'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@route('/list_comments/:id', method='GET')
def list_comments(id):
    return "listing comments %s" % id
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['documents'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

application=default_app()
#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
