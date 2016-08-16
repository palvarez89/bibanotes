#!/usr/bin/env python
import os
from bottle import route, default_app
import mysqlclient as mysql

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
    cnx = mysql.connector.connect(user=os.environ[OPENSHIFT_MYSQL_DB_USERNAME],
                                  password=os.environ[OPENSHIFT_MYSQL_DB_PASSWORD],
                                  host=os.environ[OPENSHIFT_MYSQL_DB_HOST],
                                  database='biba')
    return cnx


application=default_app()
#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
