#!/usr/bin/env python
import os
from bottle import route, default_app
import models
import psycopg2


database = "biba"
def createDatabase(db_name):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
    except BaseException as e:
        print(e)
        raise
    cur = con.cursor()
    try:
        cur.execute('CREATE DATABASE %s;' % (db_name))
    except BaseException as e:
        if "database exists" in str(e):
            print("DATABASE %s already present" %(db_name))
            pass
        else:
            raise e

def createTables(db_name):
    #connection_string = "postgresql+psycopg2://%s:%s@%s:%s/%s" % ('postgres',
    #                                                              'password',
    #                                                              os.environ["DATABASE_URL"],
    #                                                              "127.0.0.1",
    #                                                              "5432",
    #                                                              db_name)
    DATABASE_URL = os.environ['DATABASE_URL']

    from sqlalchemy import create_engine
    engine = create_engine(DATABASE_URL)
     
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    models.Base.metadata.create_all(engine)


createDatabase(database)
createTables(database)
