#!/usr/bin/env python
import os
from bottle import route, default_app, request, abort, app, template
import MySQLdb as mysql
import json
from models import Comentario, Estacion
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import bottle
bottle.TEMPLATE_PATH.insert(0,os.environ['OPENSHIFT_REPO_DIR'])

database = 'biba'

connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (os.environ["OPENSHIFT_MYSQL_DB_USERNAME"],
                                                        os.environ["OPENSHIFT_MYSQL_DB_PASSWORD"],
                                                        os.environ["OPENSHIFT_MYSQL_DB_HOST"],
                                                        os.environ["OPENSHIFT_MYSQL_DB_PORT"],
                                                        database)


from itertools import cycle
docs_exclude = "/api-doc","/api-map"

@route('/api-doc',method=['GET'])
def api_doc():
    ''' Prints HTML docs of the API
    '''
    colors = cycle('#FFFFFF #CCCFDF'.split())
    return template("bottle0_template",colors=colors,routes=app[0].routes)

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


#/archive-comment/id
@route('/archive-comment/:id', method='GET')
def archive_comment(id):
    ''' Marks a comment as archived.

        Example with curl:

            curl  localhost:8051/archive-comment/4
    '''

    print("listing number %s" % id)
    try:
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()
    except BaseException as e:
        abort(400, str(e))
        raise e
    try:
        comment = session.query(Comentario).filter(Comentario.id == id).first()
        comment.archivado = True
        session.commit()
    except BaseException as e:
        abort(400, str(e))
        raise e

@route('/add-comment/:id', method='PUT')
def add_comment(id):
    ''' Adds a comment to a given Estacion.

        Example with curl:

            curl -H 'Content-Type: application/json' -X PUT \
              -d '{"comment":"Estacion esta rota"}' \
              localhost:8051/add-comment/2
    '''

    def get_or_create(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    print("adding comments %s" % id)
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



@route('/list-comments/:id', method='GET')
def list_comments(id):
    ''' Lists all comments of a Estacion:

        Example with curl:

            curl  localhost:8051/list-comments/2
    '''

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
