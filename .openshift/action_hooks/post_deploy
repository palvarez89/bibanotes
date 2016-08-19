#!/usr/bin/env python
import os
from bottle import route, default_app
import MySQLdb as mysql

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

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
 
 
Base = declarative_base()
 
 
class Estacion(Base):
    __tablename__ = 'estacion'
    id = Column(Integer, primary_key=True)
 
 
class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    comentario = Column(String(140))
    # Use default=func.now() to set the default written time
    # of a Comentario to be the current time.
    escrito_en = Column(DateTime, default=func.now())
    estacion_id = Column(Integer, ForeignKey('estacion.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    estacion = relationship(
        Estacion,
        backref=backref('comentario',
                         uselist=True,
                         cascade='delete,all'))
 
def createTables(db_name):
    connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (os.environ["OPENSHIFT_MYSQL_DB_USERNAME"],
                                                            os.environ["OPENSHIFT_MYSQL_DB_PASSWORD"],
                                                            os.environ["OPENSHIFT_MYSQL_DB_HOST"],
                                                            os.environ["OPENSHIFT_MYSQL_DB_PORT"],
                                                            db_name)

    from sqlalchemy import create_engine
    engine = create_engine(connection_string)
     
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


createDatabase(database)
createTables(database)
