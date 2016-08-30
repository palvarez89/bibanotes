#!/usr/bin/env python

import datetime
from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator
import pytz

Base = declarative_base()


class UTCDateTime(TypeDecorator):
    """This decorator ensures that timezones will always remain attached to
    datetime fields that are written to/from the database, since mysql does
    NOT support timezones in its datetime fields. In the case that a
    value is provided without a timezone, it will raise an exception to draw
    attention to itself: Engineers should always work with timezoned
    datetime instances.
    """
    impl = DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            # If the value doesn't have a timezone, raise an exception.
            if not value.tzinfo:
                raise RuntimeError("Datetime value without timezone provided,"
                                   " please provide a timezone.")

            # Convert to UTC, then scrub the timezone for storing in MySQL.
            return value.astimezone(pytz.utc).replace(tzinfo=None)

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=pytz.utc)

class Estacion(Base):
    __tablename__ = 'estacion'
    id = Column(Integer, primary_key=True)
    def __init__(self, id):
        self.id = id


class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    comentario = Column(String(1000))
    archivado = Column(Boolean, default=False)
    # Use default=func.now() to set the default written time
    # of a Comentario to be the current time.
    escrito_en = Column(UTCDateTime,
                        default=lambda:
                        datetime.datetime.now(tz=pytz.utc))

    estacion_id = Column(Integer, ForeignKey('estacion.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    estacion = relationship(
        Estacion,
        backref=backref('comentario',
                         uselist=True,
                         cascade='delete,all'))

    def __init__(self, estacion_id, comentario):
        self.estacion_id = estacion_id
        self.comentario = comentario

    def __str__(self):
        return "%s, %s" % (self.estacion_id, self.comentario)

    def as_dict(self):
        d = {}
        d['id']=self.id
        d['comentario']=self.comentario
        d['escrito_en']=self.escrito_en.isoformat()
        d['estacion_id']=self.estacion_id
        return d
