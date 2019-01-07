#!/usr/bin/env python
import os
from bottle import route, default_app
import models

database = "biba"
def createDatabase(db_name):
    try:
        con = mysql.connect(user=os.environ["OPENSHIFT_MYSQL_DB_USERNAME"],
                            passwd=os.environ["OPENSHIFT_MYSQL_DB_PASSWORD"],
                            host=os.environ["OPENSHIFT_MYSQL_DB_HOST"],
                            port=int(os.environ["OPENSHIFT_MYSQL_DB_PORT"]))
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
    connection_string = "postgresql+psycopg2://%s:%s@%s:%s/%s" % ('postgres',
                                                                  'password',
                                                                  os.environ["DATABASE_URL"],
                                                                  "127.0.0.1",
                                                                  "5432",
                                                                  db_name)

    from sqlalchemy import create_engine
    engine = create_engine(connection_string)
     
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    models.Base.metadata.create_all(engine)


createDatabase(database)
createTables(database)
