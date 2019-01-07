#!/usr/bin/env python
import os
from bottle import route, default_app, request, abort, app, template, response, run
import json
from models import Comentario, Estacion
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import bottle
bottle.TEMPLATE_PATH.insert(0,'.')

database = 'biba'

connection_string = os.environ["DATABASE_URL"]

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

#/archive-comment/id
@route('/archive-comment/:id', method='DELETE')
def archive_comment(id):
    ''' Marks a comment as archived.

        Example with curl:

            curl  localhost:8051/archive-comment/4
    '''

    print("listing number %s" % id)
    try:
        engine = create_engine(connection_string, poolclass=NullPool)
        Session = sessionmaker(bind=engine)
        session = Session()
    except BaseException as e:
        abort(400, str(e))
        session.close()
        raise e
    try:
        comment = session.query(Comentario).filter(Comentario.id == id).first()
        comment.archivado = True
        session.commit()
    except BaseException as e:
        abort(400, str(e))
        session.close()
        raise e
    session.close()

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
        engine = create_engine(connection_string, poolclass=NullPool)
        Session = sessionmaker(bind=engine)
        session = Session()

        estacion = get_or_create(session, Estacion, id=id)

        comentario = Comentario(estacion_id=id, comentario=comment)
        session.add(estacion)
        session.add(comentario)
        session.commit()
    except BaseException as e:
        session.close()
        abort(400, str(e))
    session.close()



@route('/list-comments/:id', method='GET')
def list_comments(id):
    ''' Lists all comments of a Estacion:

        Example with curl:

            curl  localhost:8051/list-comments/2
    '''

    print("listing number %s" % id)
    try:
        engine = create_engine(connection_string, poolclass=NullPool)
        Session = sessionmaker(bind=engine)
        session = Session()
    except BaseException as e:
        abort(400, str(e))
        session.close()
        raise e
    try:
        comments = session.query(Comentario).order_by(desc(Comentario.escrito_en)).filter(Comentario.estacion_id == id).filter(Comentario.archivado == False)
        res = [r.as_dict() for r in comments]
        response.content_type = 'application/json'
        session.close()
        return json.dumps(res)
    except BaseException as e:
        abort(400, str(e))
        session.close()
        raise e

application=default_app()

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)
