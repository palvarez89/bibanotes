#!/usr/bin/env python
import os
from bottle import route, default_app, request, abort
import MySQLdb as mysql
import json
from models import Comentario, Estacion
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database = 'biba'
#app = bottle.Bottle()
connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (os.environ["OPENSHIFT_MYSQL_DB_USERNAME"],
                                                        os.environ["OPENSHIFT_MYSQL_DB_PASSWORD"],
                                                        os.environ["OPENSHIFT_MYSQL_DB_HOST"],
                                                        os.environ["OPENSHIFT_MYSQL_DB_PORT"],
                                                        database)
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

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

#/delete_comment/id


@route('/add_comment/:id', method='PUT')
def add_comment(id):
    print("adding comments %s" % id)
    #data = request.body.readline().decode('utf-8')
    data = request.json
    print(data)
    if not data:
        abort(400, 'No data received')
    if not 'comment' in data:
        abort(400, 'No comment included')
    try:
        comment = data['comment']
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        estacion = get_or_create(session, Estacion, id=id)

        comentario = Comentario(estacion_id=id, comentario=comment)
        session.add(estacion)
        session.add(comentario)
        session.commit()
    except BaseException as e:
        abort(400, str(e))



@route('/list_comments/:id', method='GET')
def list_comments(id):
    print("listing number %s" % id)
    try:
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()
    except BaseException as e:
        abort(400, str(e))
        raise e
    try:
        comments = session.query(Comentario).filter(Comentario.estacion_id == id)
        for instance in comments:
            print(instance.as_dict())
        return json.dumps([r.as_dict() for r in comments])
    except BaseException as e:
        abort(400, str(e))
        raise e

application=default_app()
#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
