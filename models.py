#!/usr/bin/env python

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

